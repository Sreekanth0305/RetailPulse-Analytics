from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):

    id: int

    company_id: int

    user_id: int | None

    type: str | None

    title: str

    message: str

    priority: str | None

    resource_type: str | None

    resource_id: int | None

    is_read: bool

    created_at: datetime

    read_at: datetime | None

    expires_at: datetime | None

    deduplication_key: str | None

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):

    items: list[NotificationResponse]

    total: int

    page: int

    limit: int

    total_pages: int