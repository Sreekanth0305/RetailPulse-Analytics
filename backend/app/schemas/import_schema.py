from pydantic import BaseModel
from typing import Any


class ImportPreviewResponse(BaseModel):

    import_id: int

    import_type: str

    filename: str

    total_records: int

    valid_records: int

    invalid_records: int

    duplicate_records: int

    columns: list[str]

    preview: list[dict[str, Any]]


class ImportProcessResponse(BaseModel):

    import_id: int

    status: str

    total_records: int

    successful_records: int

    failed_records: int

    duplicate_records: int


class ImportHistoryResponse(BaseModel):

    id: int

    import_type: str

    filename: str

    uploaded_by: int

    total_records: int

    successful_records: int

    failed_records: int

    duplicate_records: int

    status: str

    created_at: Any