from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import (
    get_current_user,
    require_admin
)

from app.models.user import User

from app.schemas.workflow_schema import (
    WorkflowCreateRequest,
    WorkflowCommentRequest,
    WorkflowConfigRequest
)

from app.services.workflow_service import (
    create_workflow_request,
    submit_workflow_request,
    get_workflow_request,
    list_workflow_requests,
    approve_workflow_request,
    reject_workflow_request,
    cancel_workflow_request
)

from app.models.workflow_history import WorkflowHistory
from app.models.workflow_config import WorkflowConfig


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


# =========================================================
# CREATE
# =========================================================

@router.post("")
def create_request(
    data: WorkflowCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_workflow_request(
        db=db,
        current_user=current_user,
        data=data
    )


# =========================================================
# SUBMIT
# =========================================================

@router.post("/{workflow_id}/submit")
def submit_request(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return submit_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id
    )


# =========================================================
# LIST
# =========================================================

@router.get("")
def list_requests(
    request_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return list_workflow_requests(
        db=db,
        current_user=current_user,
        request_type=request_type,
        status=status,
        search=search,
        page=page,
        limit=limit
    )

# =========================================================
# CONFIGURATION
# =========================================================

@router.post("/config")
def create_workflow_config(
    data: WorkflowConfigRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    config = WorkflowConfig(
        company_id=current_user.company_id,
        request_type=data.request_type,
        approver_role=data.approver_role,
        approval_required=data.approval_required,
        allow_self_approval=data.allow_self_approval,
        is_active=data.is_active
    )

    db.add(config)

    db.commit()

    db.refresh(config)

    return config


@router.get("/config/list")
def get_workflow_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return (
        db.query(WorkflowConfig)
        .filter(
            WorkflowConfig.company_id ==
            current_user.company_id
        )
        .all()
    )


# =========================================================
# DETAILS
# =========================================================

@router.get("/{workflow_id}")
def get_request(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id
    )


# =========================================================
# APPROVE
# =========================================================

@router.post("/{workflow_id}/approve")
def approve_request(
    workflow_id: int,
    data: WorkflowCommentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return approve_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id,
        comment=data.comment
    )


# =========================================================
# REJECT
# =========================================================

@router.post("/{workflow_id}/reject")
def reject_request(
    workflow_id: int,
    data: WorkflowCommentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return reject_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id,
        comment=data.comment
    )


# =========================================================
# CANCEL
# =========================================================

@router.post("/{workflow_id}/cancel")
def cancel_request(
    workflow_id: int,
    data: WorkflowCommentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return cancel_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id,
        comment=data.comment
    )


# =========================================================
# HISTORY
# =========================================================

@router.get("/{workflow_id}/history")
def get_history(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workflow = get_workflow_request(
        db=db,
        current_user=current_user,
        workflow_id=workflow_id
    )

    return (
        db.query(WorkflowHistory)
        .filter(
            WorkflowHistory.workflow_id == workflow.id,
            WorkflowHistory.company_id ==
            current_user.company_id
        )
        .order_by(
            WorkflowHistory.created_at.asc()
        )
        .all()
    )