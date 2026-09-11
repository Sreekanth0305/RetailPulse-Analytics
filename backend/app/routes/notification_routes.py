from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.services.notification_service import (
    get_notifications,
    get_unread_count,
    mark_notification_as_read,
    mark_all_notifications_as_read,
    delete_notification
)

from app.schemas.notification_schema import NotificationListResponse

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =========================================================
# GET NOTIFICATIONS
# =========================================================

@router.get(
    "/",
    response_model=NotificationListResponse
)
def get_all_notifications(
    page: int = Query(
        1,
        ge=1
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100
    ),
    is_read: bool | None = Query(
        None
    ),
    notification_type: str | None = Query(
        None
    ),
    priority: str | None = Query(
        None
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_notifications(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        page=page,
        limit=limit,
        is_read=is_read,
        notification_type=notification_type,
        priority=priority
    )


# =========================================================
# GET UNREAD COUNT
# =========================================================

@router.get("/unread-count")
def get_notifications_unread_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_unread_count(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id
    )


# =========================================================
# MARK ONE NOTIFICATION AS READ
# =========================================================

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return mark_notification_as_read(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        notification_id=notification_id
    )


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================

@router.patch("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return mark_all_notifications_as_read(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id
    )


# =========================================================
# DELETE NOTIFICATION
# =========================================================

@router.delete("/{notification_id}")
def delete_notification_api(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return delete_notification(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        notification_id=notification_id
    )