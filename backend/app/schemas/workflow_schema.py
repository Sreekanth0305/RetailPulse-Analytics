from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


class WorkflowCreateRequest(BaseModel):

    request_type: str

    related_record: Optional[str] = None

    requested_changes: Optional[dict] = None

    reason: str

    priority: str = "Normal"


class WorkflowCommentRequest(BaseModel):

    comment: Optional[str] = None


class WorkflowStatusRequest(BaseModel):

    comment: Optional[str] = None


class WorkflowConfigRequest(BaseModel):

    request_type: str

    approver_role: str

    approval_required: bool = True

    allow_self_approval: bool = False

    is_active: bool = True