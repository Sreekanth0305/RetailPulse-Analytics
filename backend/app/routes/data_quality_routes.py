import json

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user, require_admin

from app.models.user import User
from app.models.data_quality_issue import DataQualityIssue
from app.models.reconciliation_history import ReconciliationHistory

from app.schemas.data_quality_schema import (
    DataQualityIssueStatusUpdate
)

from app.services.data_quality_service import (
    run_reconciliation
)


router = APIRouter(
    prefix="/data-quality",
    tags=["Data Quality"]
)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    company_id = current_user.company_id

    total_issues = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id
        )
        .count()
    )

    errors = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id,
            DataQualityIssue.severity == "Error"
        )
        .count()
    )

    warnings = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id,
            DataQualityIssue.severity == "Warning"
        )
        .count()
    )

    unresolved = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id,
            DataQualityIssue.status.in_(
                ["Open", "Investigating"]
            )
        )
        .count()
    )

    resolved = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id,
            DataQualityIssue.status == "Resolved"
        )
        .count()
    )

    last_reconciliation = (
        db.query(ReconciliationHistory)
        .filter(
            ReconciliationHistory.company_id == company_id
        )
        .order_by(
            ReconciliationHistory.started_at.desc()
        )
        .first()
    )

    records_checked = (
        last_reconciliation.records_checked
        if last_reconciliation
        else 0
    )

    return {
        "total_records_checked": records_checked,
        "valid_records": max(
            records_checked - total_issues,
            0
        ),
        "warnings": warnings,
        "errors": errors,
        "unresolved_issues": unresolved,
        "resolved_issues": resolved,
        "last_reconciliation_time": (
            last_reconciliation.completed_at
            if last_reconciliation
            else None
        )
    }


# ---------------------------------------------------------
# RUN RECONCILIATION
# ---------------------------------------------------------

@router.post("/reconcile")
def reconcile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return run_reconciliation(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id
    )


# ---------------------------------------------------------
# ISSUES
# ---------------------------------------------------------

@router.get("/issues")
def get_issues(
    search: str = "",
    issue_type: str = "",
    severity: str = "",
    module: str = "",
    status: str = "",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if page < 1:
        page = 1

    query = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id
            == current_user.company_id
        )
    )

    if search:

        search_value = f"%{search}%"

        query = query.filter(
            DataQualityIssue.description.ilike(search_value)
            |
            DataQualityIssue.affected_record.ilike(
                search_value
            )
        )

    if issue_type:
        query = query.filter(
            DataQualityIssue.issue_type == issue_type
        )

    if severity:
        query = query.filter(
            DataQualityIssue.severity == severity
        )

    if module:
        query = query.filter(
            DataQualityIssue.module == module
        )

    if status:
        query = query.filter(
            DataQualityIssue.status == status
        )

    total = query.count()

    offset = (page - 1) * limit

    issues = (
        query
        .order_by(
            DataQualityIssue.detected_at.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": [
            {
                "id": issue.id,
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "module": issue.module,
                "affected_record": issue.affected_record,
                "description": issue.description,
                "detected_at": issue.detected_at,
                "status": issue.status,
                "resolution_note": issue.resolution_note
            }
            for issue in issues
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (
            (total + limit - 1) // limit
            if total
            else 0
        )
    }


# ---------------------------------------------------------
# ISSUE DETAILS
# ---------------------------------------------------------

@router.get("/issues/{issue_id}")
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    issue = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.id == issue_id,
            DataQualityIssue.company_id
            == current_user.company_id
        )
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Data quality issue not found."
        )

    return {
        "id": issue.id,
        "issue_type": issue.issue_type,
        "severity": issue.severity,
        "module": issue.module,
        "affected_record": issue.affected_record,
        "description": issue.description,
        "detected_at": issue.detected_at,
        "status": issue.status,
        "resolved_at": issue.resolved_at,
        "resolved_by": issue.resolved_by,
        "resolution_note": issue.resolution_note
    }


# ---------------------------------------------------------
# UPDATE ISSUE STATUS
# ---------------------------------------------------------

@router.patch("/issues/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    data: DataQualityIssueStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    allowed_statuses = [
        "Open",
        "Investigating",
        "Resolved",
        "Ignored"
    ]

    if data.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid issue status."
        )

    issue = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.id == issue_id,
            DataQualityIssue.company_id
            == current_user.company_id
        )
        .first()
    )

    if not issue:

        raise HTTPException(
            status_code=404,
            detail="Data quality issue not found."
        )

    old_status = issue.status

    issue.previous_status = old_status
    issue.new_status = data.status
    issue.status = data.status

    if data.status == "Resolved":

        issue.resolved_at = datetime.utcnow()
        issue.resolved_by = current_user.id
        issue.resolution_note = data.resolution_note

    else:

        issue.resolved_at = None
        issue.resolved_by = None
        issue.resolution_note = data.resolution_note

    db.commit()
    db.refresh(issue)

    return {
        "message": "Issue status updated successfully.",
        "id": issue.id,
        "previous_status": old_status,
        "new_status": issue.status,
        "resolved_by": issue.resolved_by,
        "resolved_at": issue.resolved_at,
        "resolution_note": issue.resolution_note
    }


# ---------------------------------------------------------
# RECONCILIATION HISTORY
# ---------------------------------------------------------

@router.get("/history")
def get_reconciliation_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = (
        db.query(ReconciliationHistory)
        .filter(
            ReconciliationHistory.company_id
            == current_user.company_id
        )
    )

    total = query.count()

    history = (
        query
        .order_by(
            ReconciliationHistory.started_at.desc()
        )
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": [
            {
                "id": item.id,
                "execution_id": item.execution_id,
                "started_at": item.started_at,
                "completed_at": item.completed_at,
                "triggered_by": item.triggered_by,
                "records_checked": item.records_checked,
                "issues_detected": item.issues_detected,
                "issues_resolved": item.issues_resolved,
                "failed_checks": item.failed_checks,
                "execution_status": item.execution_status,
                "error_message": item.error_message
            }
            for item in history
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (
            (total + limit - 1) // limit
            if total
            else 0
        )
    }