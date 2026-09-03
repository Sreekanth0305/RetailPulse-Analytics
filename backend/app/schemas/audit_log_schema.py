from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =========================================================
# Create Audit Log
# =========================================================

class AuditLogCreate(BaseModel):

    action: str

    resource_type: Optional[str] = None

    resource_id: Optional[int] = None

    description: Optional[str] = None

    before_values: Optional[dict] = None

    after_values: Optional[dict] = None

    ip_address: Optional[str] = None

    user_agent: Optional[str] = None

    status: Optional[str] = "Success"


# =========================================================
# Audit Log Response
# =========================================================

class AuditLogResponse(BaseModel):

    id: int

    company_id: int

    user_id: int

    action: str

    resource_type: Optional[str] = None

    resource_id: Optional[int] = None

    description: Optional[str] = None

    before_values: Optional[dict] = None

    after_values: Optional[dict] = None

    ip_address: Optional[str] = None

    user_agent: Optional[str] = None

    status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )