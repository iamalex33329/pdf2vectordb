import streamlit as st
import sys
import uuid
import hashlib
from core.pdf_processor import extract_pdf_content
from core.embedding_generator import generate_embeddings
from core.db.operations import connect_to_db, create_or_open_table, add_entries_to_table, update_entries, find_existing_entry, find_entries_with_file_name
from utils.file_utils import get_upload_dir, save_uploaded_file, get_file_info, delete_file

from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))


def mark_existing_files_as_deprecated(file_name, new_file_id):
    db = connect_to_db()
    table = create_or_open_table(db, 'knowledge_base')
    update_entries(table, f"file_name = '{file_name}' AND file_id != '{new_file_id}'", {"is_deprecated": True})


def mark_file_as_deleted(file_name):
    db = connect_to_db()
    table = create_or_open_table(db, 'knowledge_base')
    update_entries(table, f"file_name = '{file_name}' AND is_deleted = False",
                   {"is_deleted": True})


def check_and_restore_deleted_file(file_name, new_file_id):
    db = connect_to_db()
    table = create_or_open_table(db, 'knowledge_base')
    deleted_entry = find_entries_with_file_name(table, file_name).query("is_deleted == True")
    if not deleted_entry.empty:
        update_entries(table, f"file_name = '{file_name}' AND file_id = '{deleted_entry.iloc[0]['file_id']}'",
                       {"is_deleted": False, "file_id": new_file_id, "is_deprecated": False})
        return True
    return False


def cleanup_deleted_files(days_threshold=30):
    # 目前，我們沒有辦法根據刪除時間來清理文件
    # 這個函數可以保留，但目前不會執行任何操作
    pass


def update_or_add_entries(file_name, new_file_id, entries):
    db = connect_to_db()
    table = create_or_open_table(db, 'knowledge_base')
    existing_entries = find_entries_with_file_name(table, file_name)
    if not existing_entries.empty:
        mark_existing_files_as_deprecated(file_name, new_file_id)
        existing_entry = find_existing_entry(table, file_name, new_file_id)
        if not existing_entry.empty:
            update_entries(table, f"file_name = '{file_name}' AND file_id = '{new_file_id}'",
                           {"is_deleted": False, "is_deprecated": False})
            return False
    for entry in entries:
        entry["is_deprecated"] = False
        entry["is_deleted"] = False
    add_entries_to_table(table, entries)
    return True


def rollback_version(file_name, version_id):
    db = connect_to_db()
    table = create_or_open_table(db, 'knowledge_base')
    update_entries(table, f"file_name = '{file_name}' AND is_deleted = False", {"is_deprecated": True})
    update_entries(table, f"file_name = '{file_name}' AND file_id = '{version_id}'", {"is_deprecated": False})


st.set_page_config(page_title="PDF Upload and Vector Storage App", layout="wide")

st.title("PDF Upload and Vector Storage App")

st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = str(uuid.uuid4())

with st.sidebar:
    st.header("File Upload Area")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"],
                                      accept_multiple_files=True,
                                      key=st.session_state.uploader_key)

    if st.button("Process and Store Files"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file)
                pdf_content = extract_pdf_content(file_path)
                embeddings = generate_embeddings(pdf_content)

                with open(file_path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

                entries = []
                for page_num, (text, embedding) in enumerate(zip(pdf_content, embeddings), start=1):
                    entry = {
                        "file_name": uploaded_file.name,
                        "raw_text": text,
                        "text_page": page_num,
                        "vector": embedding,
                        "file_id": file_hash,
                        "is_deleted": False,
                        "is_deprecated": False,
                    }
                    entries.append(entry)

                if update_or_add_entries(uploaded_file.name, file_hash, entries):
                    st.success(f"Successfully processed and stored new file: {uploaded_file.name}")
                else:
                    st.success(f"Successfully updated existing file: {uploaded_file.name}")

            st.session_state.uploader_key = str(uuid.uuid4())
            st.rerun()
        else:
            st.warning("Please select files before processing")


st.header("Uploaded Files")
st.write('---')

all_files = list(get_upload_dir().glob('*'))
all_file_infos = [get_file_info(file) for file in all_files]

if all_file_infos:
    for file_info in all_file_infos:
        cols = st.columns([2, 1, 1, 2, 1])
        with cols[0]:
            st.write(f"**{file_info['Name']}**")
        with cols[1]:
            st.write(f"Type: {file_info['Type']}")
        with cols[2]:
            st.write(f"Size: {file_info['Size (KB)']} KB")
        with cols[3]:
            st.write(f"Uploaded: {file_info['Upload Date']}")
        with cols[4]:
            if st.button("Delete", key=file_info['Name']):
                if delete_file(file_info['Name']):
                    mark_file_as_deleted(file_info['Name'])
                    st.success(f"Successfully deleted file: {file_info['Name']}")
                    st.rerun()
                else:
                    st.warning(f"Failed to delete file: {file_info['Name']}")
else:
    st.info("No files have been uploaded yet")

# cleanup_deleted_files()
