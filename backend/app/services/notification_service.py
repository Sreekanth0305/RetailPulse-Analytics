from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.notification import Notification

from app.models.user import User

from app.services.audit_service import create_audit_log

def get_notification_recipients(
    db: Session,
    company_id: int,
    notification_type: str
):
    if notification_type in {
        "Stockout Risk",
        "Low Stock",
        "Import Completed",
        "Import Failed",
        "System Alert"
    }:
        allowed_roles = {
            "Super Admin",
            "Company Admin"
        }

    elif notification_type in {
        "Sales Alert",
        "Overstock"
    }:
        allowed_roles = {
            "Super Admin",
            "Company Admin",
            "Analyst"
        }

    else:
        allowed_roles = {
            "Super Admin",
            "Company Admin"
        }

    return (
        db.query(User)
        .filter(
            User.company_id == company_id,
            User.status == "Active",
            User.role.in_(allowed_roles)
        )
        .all()
    )

# =========================================================
# CREATE NOTIFICATION
# =========================================================

def create_notification(
    db: Session,
    company_id: int,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    priority: str = "Medium",
    resource_type: str | None = None,
    resource_id: int | None = None,
    deduplication_key: str | None = None,
    expires_in_days: int | None = 30
):
    """
    Create a notification for one specific user.

    Notifications are isolated by:
    - company_id
    - user_id

    Duplicate notifications can be prevented using
    deduplication_key.
    """

    # -----------------------------------------------------
    # DUPLICATE PREVENTION
    # -----------------------------------------------------

    if deduplication_key:

        existing_notification = (
            db.query(Notification)
            .filter(
                Notification.company_id == company_id,
                Notification.user_id == user_id,
                Notification.deduplication_key == deduplication_key,
                Notification.is_read.is_(False)
            )
            .first()
        )

        if existing_notification:
            return existing_notification

    # -----------------------------------------------------
    # EXPIRY
    # -----------------------------------------------------

    expires_at = None

    if expires_in_days is not None:
        expires_at = datetime.utcnow() + timedelta(
            days=expires_in_days
        )

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------

    notification = Notification(
        company_id=company_id,
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        priority=priority,
        resource_type=resource_type,
        resource_id=resource_id,
        is_read=False,
        read_at=None,
        expires_at=expires_at,
        deduplication_key=deduplication_key
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification

# -----------------------------------------------------
# CREATE ROLE BASED NOTIFICATION
# -----------------------------------------------------

def create_role_based_notifications(
    db: Session,
    company_id: int,
    notification_type: str,
    title: str,
    message: str,
    priority: str = "Medium",
    resource_type: str | None = None,
    resource_id: int | None = None,
    deduplication_key: str | None = None,
    expires_in_days: int | None = 30
):
    recipients = get_notification_recipients(
        db=db,
        company_id=company_id,
        notification_type=notification_type
    )

    created_notifications = []

    for user in recipients:
        user_deduplication_key = None

        if deduplication_key:
            user_deduplication_key = (
                f"{deduplication_key}:user:{user.id}"
            )

        notification = create_notification(
            db=db,
            company_id=company_id,
            user_id=user.id,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            resource_type=resource_type,
            resource_id=resource_id,
            deduplication_key=user_deduplication_key,
            expires_in_days=expires_in_days
        )

        created_notifications.append(notification)

    return created_notifications


# =========================================================
# GET NOTIFICATIONS
# =========================================================

def get_notifications(
    db: Session,
    company_id: int,
    user_id: int,
    page: int = 1,
    limit: int = 20,
    is_read: bool | None = None,
    notification_type: str | None = None,
    priority: str | None = None
):
    """
    Get notifications belonging only to the logged-in user
    and their company.

    Supports:
    - pagination
    - read/unread filtering
    - type filtering
    - priority filtering
    """

    # -----------------------------------------------------
    # REMOVE EXPIRED NOTIFICATIONS FROM ACTIVE RESULTS
    # -----------------------------------------------------

    query = (
        db.query(Notification)
        .filter(
            Notification.company_id == company_id,
            (
                (Notification.user_id == user_id)
                | (Notification.user_id.is_(None))
            )
        )
    )

    # -----------------------------------------------------
    # EXPIRY FILTER
    # -----------------------------------------------------

    query = query.filter(
        (Notification.expires_at.is_(None)) |
        (Notification.expires_at > datetime.utcnow())
    )

    # -----------------------------------------------------
    # READ / UNREAD FILTER
    # -----------------------------------------------------

    if is_read is not None:
        query = query.filter(
            Notification.is_read == is_read
        )

    # -----------------------------------------------------
    # TYPE FILTER
    # -----------------------------------------------------

    if notification_type:
        query = query.filter(
            Notification.type == notification_type
        )

    # -----------------------------------------------------
    # PRIORITY FILTER
    # -----------------------------------------------------

    if priority:
        query = query.filter(
            Notification.priority == priority
        )

    # -----------------------------------------------------
    # TOTAL COUNT
    # -----------------------------------------------------

    total = query.count()

    # -----------------------------------------------------
    # PAGINATION
    # -----------------------------------------------------

    offset = (page - 1) * limit

    notifications = (
        query
        .order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": notifications,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (
            (total + limit - 1) // limit
            if limit > 0
            else 0
        )
    }


# =========================================================
# GET UNREAD COUNT
# =========================================================

def get_unread_count(
    db: Session,
    company_id: int,
    user_id: int
):
    """
    Return the unread notification count for the
    authenticated user.
    """

    count = (
        db.query(Notification)
        .filter(
            Notification.company_id == company_id,
            (
                (Notification.user_id == user_id)
                | (Notification.user_id.is_(None))
            ),
            Notification.is_read.is_(False),
            (
                Notification.expires_at.is_(None)
                | (
                    Notification.expires_at > datetime.utcnow()
                )
            )
        )
        .count()
    )

    return {
        "unread_count": count
    }


# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================

def mark_notification_as_read(
    db: Session,
    company_id: int,
    user_id: int,
    notification_id: int
):
    """
    Mark one notification as read.

    The notification must belong to both:
    - the authenticated company
    - the authenticated user
    """

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.company_id == company_id,
            (
                (Notification.user_id == user_id)
                | (Notification.user_id.is_(None))
            )
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    # -----------------------------------------------------
    # UPDATE ONLY IF CURRENTLY UNREAD
    # -----------------------------------------------------

    if not notification.is_read:

        before_values = {
            "is_read": notification.is_read,
            "read_at": notification.read_at
        }

        notification.is_read = True
        notification.read_at = datetime.utcnow()

        db.commit()
        db.refresh(notification)

        # -------------------------------------------------
        # AUDIT NOTIFICATION READ ACTION
        # -------------------------------------------------

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="NOTIFICATION_READ",
            resource_type="Notification",
            resource_id=notification.id,
            description=(
                f"Marked notification #{notification.id} as read"
            ),
            before_values=before_values,
            after_values={
                "is_read": notification.is_read,
                "read_at": notification.read_at
            },
            status="Success"
        )

    return notification


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================

def mark_all_notifications_as_read(
    db: Session,
    company_id: int,
    user_id: int
):
    """
    Mark all unread notifications belonging to the
    authenticated user as read.
    """

    notifications = (
        db.query(Notification)
        .filter(
            Notification.company_id == company_id,
            Notification.user_id == user_id,
            Notification.is_read.is_(False)
        )
        .all()
    )

    current_time = datetime.utcnow()

    for notification in notifications:

        notification.is_read = True
        notification.read_at = current_time

    db.commit()

    updated_count = len(notifications)

    # -----------------------------------------------------
    # AUDIT MARK-ALL-AS-READ ACTION
    # -----------------------------------------------------

    if updated_count > 0:

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="NOTIFICATIONS_READ_ALL",
            resource_type="Notification",
            resource_id=None,
            description=(
                f"Marked {updated_count} notification(s) as read"
            ),
            before_values={
                "unread_count": updated_count
            },
            after_values={
                "unread_count": 0
            },
            status="Success"
        )

    return {
        "message": "All notifications marked as read.",
        "updated_count": updated_count
    }


# =========================================================
# DELETE NOTIFICATION
# =========================================================

def delete_notification(
    db: Session,
    company_id: int,
    user_id: int,
    notification_id: int
):
    """
    Delete a notification belonging to the authenticated
    user and company.

    This is retained for compatibility with your existing
    notification UI.
    """

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.company_id == company_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    # -----------------------------------------------------
    # SAVE VALUES BEFORE DELETE FOR AUDIT
    # -----------------------------------------------------

    before_values = {
        "type": notification.type,
        "title": notification.title,
        "message": notification.message,
        "priority": notification.priority,
        "resource_type": notification.resource_type,
        "resource_id": notification.resource_id,
        "is_read": notification.is_read,
        "created_at": notification.created_at
    }

    deleted_notification_id = notification.id

    db.delete(notification)
    db.commit()

    # -----------------------------------------------------
    # AUDIT NOTIFICATION DELETE ACTION
    # -----------------------------------------------------

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="NOTIFICATION_DELETE",
        resource_type="Notification",
        resource_id=deleted_notification_id,
        description=(
            f"Deleted notification #{deleted_notification_id}"
        ),
        before_values=before_values,
        after_values=None,
        status="Success"
    )

    return {
        "message": "Notification deleted successfully."
    }