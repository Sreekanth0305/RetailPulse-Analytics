from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.config.database import get_db
from app.config.jwt import get_current_user, require_admin

from app.schemas.audit_log_schema import (
    AuditLogResponse,
    AuditLogCreate
)

from app.services.audit_service import (
    get_audit_logs,
    create_audit_log,
    get_audit_log_by_id,
    export_audit_logs_csv,
    export_audit_logs_pdf,
    clear_audit_logs
)


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


# =========================================================
# GET AUDIT LOGS
# =========================================================

@router.get(
    "/",
    response_model=dict
)
def fetch_audit_logs(

    current_user=Depends(require_admin),

    db: Session = Depends(get_db),

    user_id: Optional[int] = Query(
        default=None
    ),

    action: Optional[str] = Query(
        default=None
    ),

    resource_type: Optional[str] = Query(
        default=None
    ),

    status: Optional[str] = Query(
        default=None
    ),

    search: Optional[str] = Query(
        default=None
    ),

    date_from: Optional[str] = Query(
        default=None
    ),

    date_to: Optional[str] = Query(
        default=None
    ),

    sort_order: str = Query(
        default="desc"
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=25,
        ge=1,
        le=100
    )
):

    return get_audit_logs(

        db=db,

        company_id=current_user.company_id,

        user_id=user_id,

        action=action,

        resource_type=resource_type,

        status=status,

        search=search,

        date_from=date_from,

        date_to=date_to,

        sort_order=sort_order,

        page=page,

        limit=limit
    )


# =========================================================
# CREATE AUDIT LOG
# =========================================================

@router.post(
    "/",
    response_model=AuditLogResponse
)
def add_audit_log(

    audit: AuditLogCreate,

    current_user=Depends(require_admin),

    db: Session = Depends(get_db)
):

    return create_audit_log(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        action=audit.action,

        resource_type=audit.resource_type or "",

        resource_id=audit.resource_id,

        description=audit.description or "",

        ip_address=audit.ip_address or "",

        user_agent=audit.user_agent or "",

        status=audit.status or "SUCCESS",

        before_values=audit.before_values,

        after_values=audit.after_values
    )

@router.get("/export/csv")
def export_audit_logs_csv_file(
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),

    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    sort_order: str = Query("desc")
):

    csv_content = export_audit_logs_csv(
        db=db,
        company_id=current_user.company_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        status=status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        sort_order=sort_order
    )

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=audit_logs.csv"
        }
    )

@router.get("/export/pdf")
def export_audit_logs_pdf_file(
    current_user=Depends(require_admin),
    db: Session = Depends(get_db),

    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    sort_order: str = Query("desc")
):

    pdf_file = export_audit_logs_pdf(
        db=db,
        company_id=current_user.company_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        status=status,
        search=search,
        date_from=date_from,
        date_to=date_to,
        sort_order=sort_order
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                "attachment; filename=audit_logs.pdf"
        }
    )

@router.delete("/clear")
def clear_audit_logs_endpoint(
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):

    result = clear_audit_logs(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id
    )

    return result


# =========================================================
# GET SINGLE AUDIT LOG
# =========================================================

@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse
)
def fetch_audit_log(

    audit_log_id: int,

    current_user=Depends(require_admin),

    db: Session = Depends(get_db)
):

    audit_log = get_audit_log_by_id(

        db=db,

        company_id=current_user.company_id,

        audit_log_id=audit_log_id
    )

    if not audit_log:

        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    return audit_log