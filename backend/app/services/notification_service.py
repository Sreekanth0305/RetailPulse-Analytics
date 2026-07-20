from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.notification import Notification


def create_notification(
    db: Session,
    company_id: int,
    title: str,
    message: str
):

    notification = Notification(
        company_id=company_id,
        title=title,
        message=message,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification

# -----------------------------
# Get Notifications
# -----------------------------
def get_notifications(
    db: Session,
    company_id: int
):

    return (
        db.query(Notification)
        .filter(Notification.company_id == company_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


# -----------------------------
# Mark Notification As Read
# -----------------------------
def mark_notification_as_read(
    db: Session,
    company_id: int,
    notification_id: int
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.company_id == company_id
        )
        .first()
    )

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read."
    }


# -----------------------------
# Delete Notification
# -----------------------------
def delete_notification(
    db: Session,
    company_id: int,
    notification_id: int
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.company_id == company_id
        )
        .first()
    )

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    db.delete(notification)

    db.commit()

    return {
        "message": "Notification deleted successfully."
    }