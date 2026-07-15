from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

from app.models.user import User


def create_audit_log(
    db: Session,
    company_id: int,
    user_id: int,
    action: str,
    ip_address: str = "",
    browser: str = ""
):

    log = AuditLog(
        company_id=company_id,
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        browser=browser
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

def get_audit_logs(
    db: Session,
    company_id: int
):

    logs = (
        db.query(AuditLog, User.name)
        .join(User, AuditLog.user_id == User.id)
        .filter(AuditLog.company_id == company_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    result = []

    for log, user_name in logs:

        result.append({

            "id": log.id,
            "action": log.action,
            "ip_address": log.ip_address,
            "browser": log.browser,
            "created_at": log.created_at,
            "user_name": user_name

        })

    return result