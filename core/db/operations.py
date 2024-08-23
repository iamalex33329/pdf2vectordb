import lancedb
from pathlib import Path

from core.db.models import KnowledgeModel


def connect_to_db():
    home = Path.home()
    db_path = home / 'collection/lancedb/DocumentsVectorDatabase'
    return lancedb.connect(db_path)


def create_or_open_table(db, table_name):
    return db.create_table(table_name, schema=KnowledgeModel.to_arrow_schema(), exist_ok=True)


def add_entries_to_table(table, entries):
    table.add(entries)


def update_entries(table, conditions, updates):
    table.update(where=conditions, values=updates)


def find_existing_entry(table, file_name, file_id):
    return table.to_pandas().query(f"file_name == '{file_name}' and file_id == '{file_id}'")


def find_entries_with_file_name(table, file_name):
    return table.to_pandas().query(f"file_name == '{file_name}'")
