from pydantic import BaseModel
from datetime import datetime

class AuditLogCreate(BaseModel):

    action: str

    entity_name: str | None = ""

    ip_address: str | None = ""

    browser: str | None = ""


class AuditLogResponse(BaseModel):

    id: int

    entity_name: str | None

    action: str

    ip_address: str | None

    browser: str | None

    created_at: datetime

    user_name: str

    class Config:

        from_attributes = True