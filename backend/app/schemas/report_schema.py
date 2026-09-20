from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):

    report_type: str

    generated_at: datetime

    filters: dict

    items: list[dict]

    total: int

    page: int

    limit: int

    total_pages: int


class ReportHistoryResponse(BaseModel):

    id: int

    company_id: int

    user_id: int

    report_type: str

    filters: str | None

    export_format: str | None

    status: str

    error_message: str | None

    generated_at: datetime

    class Config:
        from_attributes = True


class ReportHistoryListResponse(BaseModel):

    items: list[ReportHistoryResponse]

    total: int

    page: int

    limit: int

    total_pages: int