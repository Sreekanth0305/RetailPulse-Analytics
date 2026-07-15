from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.audit_log_schema import AuditLogResponse

from app.services.audit_service import get_audit_logs


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