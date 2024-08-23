from lancedb.pydantic import LanceModel, Vector


class KnowledgeModel(LanceModel):
    file_name: str
    raw_text: str
    text_page: int
    vector: Vector(1536)
    file_id: str
    is_deleted: bool
    is_deprecated: bool
