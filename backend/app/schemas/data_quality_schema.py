from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DataQualityIssueStatusUpdate(BaseModel):
    status: str
    resolution_note: Optional[str] = None


class DataQualityIssueResponse(BaseModel):
    id: int
    issue_type: str
    severity: str
    module: str
    affected_record: Optional[str]
    description: str
    detected_at: datetime
    status: str
    resolved_at: Optional[datetime]
    resolved_by: Optional[int]
    resolution_note: Optional[str]

    class Config:
        from_attributes = True