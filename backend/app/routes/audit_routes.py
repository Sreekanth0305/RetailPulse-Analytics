from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.audit_log_schema import AuditLogResponse, AuditLogCreate

from app.services.audit_service import get_audit_logs, create_audit_log


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get(
    "/",
    response_model=list[AuditLogResponse]
)
def fetch_audit_logs(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_audit_logs(
        db,
        current_user.company_id
    )

@router.post("/")
def add_audit_log(

    audit: AuditLogCreate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return create_audit_log(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        action=audit.action,

        entity_name=audit.entity_name,

        ip_address=audit.ip_address,

        browser=audit.browser

    )