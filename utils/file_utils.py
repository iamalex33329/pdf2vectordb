from pathlib import Path
import os
import datetime
import mimetypes


def get_upload_dir():
    home = Path.home()
    upload_dir = home / 'collection/uploaded_files'
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_uploaded_file(uploaded_file):
    upload_dir = get_upload_dir()
    file_path = upload_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def get_file_info(file_path):
    stats = os.stat(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    return {
        "Name": file_path.name,
        "Type": mime_type or "Unknown",
        "Size (KB)": round(stats.st_size / 1024, 2),
        "Upload Date": datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    }


def delete_file(file_name):
    file_path = get_upload_dir() / file_name
    if file_path.exists():
        os.remove(file_path)
        return True
    return False
