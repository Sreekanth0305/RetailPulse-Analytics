from pydantic import BaseModel
from datetime import datetime


class AuditLogResponse(BaseModel):

    id: int

    action: str

    ip_address: str | None

    browser: str | None

    created_at: datetime

    user_name: str

    class Config:

        from_attributes = True