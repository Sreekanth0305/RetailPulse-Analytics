from datetime import datetime

from pydantic import BaseModel


class ScheduledReportCreate(BaseModel):

    report_type: str

    filters: dict | None = None

    frequency: str

    execution_time: str

    recipients: list[str]

    export_format: str


class ScheduledReportUpdate(BaseModel):

    report_type: str | None = None

    filters: dict | None = None

    frequency: str | None = None

    execution_time: str | None = None

    recipients: list[str] | None = None

    export_format: str | None = None

    is_active: bool | None = None


class ScheduledReportResponse(BaseModel):

    id: int

    company_id: int

    user_id: int

    report_type: str

    filters: str | None

    frequency: str

    execution_time: str

    recipients: str

    export_format: str

    is_active: bool

    last_run_at: datetime | None

    last_run_status: str | None

    last_error_message: str | None

    next_run_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduledReportListResponse(BaseModel):

    items: list[ScheduledReportResponse]

    total: int

    page: int

    limit: int

    total_pages: int