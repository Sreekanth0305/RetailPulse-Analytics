from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.config.jwt import get_current_user

from app.services.notification_service import (
    get_notifications,
    mark_notification_as_read,
    delete_notification
)

from app.schemas.notification_schema import NotificationResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# -----------------------------
# Get All Notifications
# -----------------------------
@router.get(
    "/",
    response_model=list[NotificationResponse]
)
def get_all_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_notifications(
        db,
        current_user.company_id
    )


# -----------------------------
# Mark As Read
# -----------------------------
@router.put("/{notification_id}")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return mark_notification_as_read(
        db,
        current_user.company_id,
        notification_id
    )


# -----------------------------
# Delete Notification
# -----------------------------
@router.delete("/{notification_id}")
def delete_notification_api(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return delete_notification(
        db,
        current_user.company_id,
        notification_id
    )