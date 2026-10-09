from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.workflow_request import WorkflowRequest
from app.models.workflow_history import WorkflowHistory
from app.models.workflow_config import WorkflowConfig

from app.models.user import User
from app.models.product import Product
from app.models.customer import Customer
from app.models.inventory import Inventory

from app.services.notification_service import (
    create_role_based_notifications
)

from app.services.audit_service import (
    create_audit_log
)


VALID_REQUEST_TYPES = [
    "Stock Adjustment",
    "Product Deactivation",
    "Product Price Change",
    "Customer Information Change",
    "Inventory Import Approval"
]


VALID_STATUSES = [
    "Draft",
    "Submitted",
    "Pending Approval",
    "Approved",
    "Rejected",
    "Cancelled"
]


# =========================================================
# HISTORY
# =========================================================

def create_history(
    db: Session,
    workflow,
    user_id: int,
    action: str,
    from_status: str | None,
    to_status: str | None,
    comment: str | None = None
):

    history = WorkflowHistory(

        workflow_id=workflow.id,

        company_id=workflow.company_id,

        user_id=user_id,

        action=action,

        from_status=from_status,

        to_status=to_status,

        comment=comment
    )

    db.add(history)

    return history


# =========================================================
# APPROVER
# =========================================================

def find_approver(
    db: Session,
    company_id: int,
    requester_id: int,
    request_type: str
):

    config = (
        db.query(WorkflowConfig)
        .filter(
            WorkflowConfig.company_id == company_id,
            WorkflowConfig.request_type == request_type,
            WorkflowConfig.is_active.is_(True)
        )
        .first()
    )

    if not config:
        raise HTTPException(
            status_code=400,
            detail="Workflow configuration not found."
        )

    if not config.approval_required:
        return None, config

    approver = (
        db.query(User)
        .filter(
            User.company_id == company_id,
            User.role == config.approver_role,
            User.status == "Active",
            User.id != requester_id
        )
        .first()
    )

    if not approver:
        raise HTTPException(
            status_code=400,
            detail="No eligible approver found."
        )

    return approver, config


# =========================================================
# CREATE REQUEST
# =========================================================

def create_workflow_request(
    db: Session,
    current_user: User,
    data
):

    if data.request_type not in VALID_REQUEST_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Invalid workflow request type."
        )

    if not data.reason.strip():

        raise HTTPException(
            status_code=400,
            detail="Reason is required."
        )

    workflow = WorkflowRequest(

        company_id=current_user.company_id,

        requested_by=current_user.id,

        request_type=data.request_type,

        related_record=data.related_record,

        requested_changes=data.requested_changes,

        reason=data.reason,

        priority=data.priority,

        status="Draft"
    )

    db.add(workflow)

    db.commit()

    db.refresh(workflow)

    create_history(
        db=db,
        workflow=workflow,
        user_id=current_user.id,
        action="Request Created",
        from_status=None,
        to_status="Draft"
    )

    create_audit_log(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        action="Workflow Request Created",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        description=(
            f"{data.request_type} request created."
        ),
        status="SUCCESS"
    )

    db.commit()

    return workflow


# =========================================================
# SUBMIT
# =========================================================

def submit_workflow_request(
    db: Session,
    current_user: User,
    workflow_id: int
):

    workflow = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.id == workflow_id,
            WorkflowRequest.company_id ==
            current_user.company_id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow request not found."
        )

    if workflow.requested_by != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You can only submit your own request."
        )

    if workflow.status != "Draft":

        raise HTTPException(
            status_code=400,
            detail="Only Draft requests can be submitted."
        )

    approver, config = find_approver(
        db=db,
        company_id=current_user.company_id,
        requester_id=current_user.id,
        request_type=workflow.request_type
    )

    old_status = workflow.status

    workflow.status = (
        "Pending Approval"
        if config.approval_required
        else "Approved"
    )

    workflow.approver_id = (
        approver.id
        if approver
        else None
    )

    create_history(
        db=db,
        workflow=workflow,
        user_id=current_user.id,
        action="Request Submitted",
        from_status=old_status,
        to_status=workflow.status
    )

    create_audit_log(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        action="Workflow Request Submitted",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        description=(
            f"{workflow.request_type} request submitted."
        ),
        status="SUCCESS"
    )

    if approver:

        create_role_based_notifications(
            db=db,
            company_id=current_user.company_id,
            notification_type="Approval Required",
            title="Approval Required",
            message=(
                f"New {workflow.request_type} "
                f"request #{workflow.id} requires approval."
            ),
            priority=workflow.priority,
            resource_type="WorkflowRequest",
            resource_id=workflow.id,
            deduplication_key=(
                f"workflow:{workflow.id}:approval"
            ),
            expires_in_days=7
        )

    db.commit()

    db.refresh(workflow)

    return workflow


# =========================================================
# GET REQUEST
# =========================================================

def get_workflow_request(
    db: Session,
    current_user: User,
    workflow_id: int
):

    workflow = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.id == workflow_id,
            WorkflowRequest.company_id ==
            current_user.company_id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow request not found."
        )

    if (
        workflow.requested_by != current_user.id
        and workflow.approver_id != current_user.id
        and current_user.role != "Admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this request."
        )

    return workflow


# =========================================================
# LIST REQUESTS
# =========================================================

def list_workflow_requests(
    db: Session,
    current_user: User,
    request_type: str | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10
):

    query = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.company_id ==
            current_user.company_id
        )
    )

    if current_user.role != "Admin":

        query = query.filter(
            (WorkflowRequest.requested_by ==
             current_user.id)
            |
            (WorkflowRequest.approver_id ==
             current_user.id)
        )

    if request_type:

        query = query.filter(
            WorkflowRequest.request_type ==
            request_type
        )

    if status:

        query = query.filter(
            WorkflowRequest.status ==
            status
        )

    if search:

        query = query.filter(
            WorkflowRequest.related_record.ilike(
                f"%{search}%"
            )
        )

    total = query.count()

    requests = (
        query
        .order_by(
            WorkflowRequest.created_at.desc()
        )
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "requests": requests
    }


# =========================================================
# APPROVE
# =========================================================

def approve_workflow_request(
    db: Session,
    current_user: User,
    workflow_id: int,
    comment: str | None = None
):

    workflow = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.id == workflow_id,
            WorkflowRequest.company_id ==
            current_user.company_id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow request not found."
        )

    if workflow.status != "Pending Approval":

        raise HTTPException(
            status_code=400,
            detail=(
                "Only Pending Approval requests "
                "can be approved."
            )
        )

    if workflow.approver_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You are not the assigned approver."
        )

    # -----------------------------------------------------
    # APPLY BUSINESS CHANGE
    # -----------------------------------------------------

    apply_workflow_change(
        db=db,
        workflow=workflow
    )

    old_status = workflow.status

    workflow.status = "Approved"

    create_history(
        db=db,
        workflow=workflow,
        user_id=current_user.id,
        action="Request Approved",
        from_status=old_status,
        to_status="Approved",
        comment=comment
    )

    create_audit_log(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        action="Workflow Request Approved",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        description=(
            f"{workflow.request_type} request "
            f"approved."
        ),
        status="SUCCESS"
    )

    create_role_based_notifications(
        db=db,
        company_id=current_user.company_id,
        notification_type="Approval Completed",
        title="Request Approved",
        message=(
            f"Your {workflow.request_type} "
            f"request #{workflow.id} was approved."
        ),
        priority="Low",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        deduplication_key=(
            f"workflow:{workflow.id}:approved"
        ),
        expires_in_days=7
    )

    db.commit()

    db.refresh(workflow)

    return workflow


# =========================================================
# REJECT
# =========================================================

def reject_workflow_request(
    db: Session,
    current_user: User,
    workflow_id: int,
    comment: str | None = None
):

    workflow = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.id == workflow_id,
            WorkflowRequest.company_id ==
            current_user.company_id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow request not found."
        )

    if workflow.status != "Pending Approval":

        raise HTTPException(
            status_code=400,
            detail=(
                "Only Pending Approval requests "
                "can be rejected."
            )
        )

    if workflow.approver_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You are not the assigned approver."
        )

    if not comment or not comment.strip():

        raise HTTPException(
            status_code=400,
            detail="Rejection reason is required."
        )

    old_status = workflow.status

    workflow.status = "Rejected"

    create_history(
        db=db,
        workflow=workflow,
        user_id=current_user.id,
        action="Request Rejected",
        from_status=old_status,
        to_status="Rejected",
        comment=comment
    )

    create_audit_log(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        action="Workflow Request Rejected",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        description=(
            f"{workflow.request_type} request "
            f"rejected."
        ),
        status="SUCCESS"
    )

    create_role_based_notifications(
        db=db,
        company_id=current_user.company_id,
        notification_type="Approval Rejected",
        title="Request Rejected",
        message=(
            f"Your {workflow.request_type} "
            f"request #{workflow.id} was rejected."
        ),
        priority="Normal",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        deduplication_key=(
            f"workflow:{workflow.id}:rejected"
        ),
        expires_in_days=7
    )

    db.commit()

    db.refresh(workflow)

    return workflow


# =========================================================
# CANCEL
# =========================================================

def cancel_workflow_request(
    db: Session,
    current_user: User,
    workflow_id: int,
    comment: str | None = None
):

    workflow = (
        db.query(WorkflowRequest)
        .filter(
            WorkflowRequest.id == workflow_id,
            WorkflowRequest.company_id ==
            current_user.company_id
        )
        .first()
    )

    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow request not found."
        )

    if workflow.requested_by != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="Only the requester can cancel this request."
        )

    if workflow.status not in [
        "Draft",
        "Submitted",
        "Pending Approval"
    ]:

        raise HTTPException(
            status_code=400,
            detail="This request cannot be cancelled."
        )

    old_status = workflow.status

    workflow.status = "Cancelled"

    create_history(
        db=db,
        workflow=workflow,
        user_id=current_user.id,
        action="Request Cancelled",
        from_status=old_status,
        to_status="Cancelled",
        comment=comment
    )

    create_audit_log(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        action="Workflow Request Cancelled",
        resource_type="WorkflowRequest",
        resource_id=workflow.id,
        description=(
            f"{workflow.request_type} request "
            f"cancelled."
        ),
        status="SUCCESS"
    )

    db.commit()

    db.refresh(workflow)

    return workflow


# =========================================================
# APPLY APPROVED CHANGE
# =========================================================

def apply_workflow_change(
    db: Session,
    workflow: WorkflowRequest
):

    changes = workflow.requested_changes or {}

    # -----------------------------------------------------
    # STOCK ADJUSTMENT
    # -----------------------------------------------------

    if workflow.request_type == "Stock Adjustment":

        product_id = changes.get("product_id")

        new_stock = changes.get("new_stock")

        if product_id is None:
            raise HTTPException(
                status_code=400,
                detail="Product ID is required."
            )

        if new_stock is None:
            raise HTTPException(
                status_code=400,
                detail="New stock value is required."
            )

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.company_id ==
                workflow.company_id,
                Inventory.product_id ==
                int(product_id)
            )
            .first()
        )

        if not inventory:

            raise HTTPException(
                status_code=404,
                detail="Inventory record not found."
            )

        if int(new_stock) < 0:

            raise HTTPException(
                status_code=400,
                detail="Stock cannot be negative."
            )

        inventory.current_stock = int(new_stock)

        inventory.available_stock = (
            int(new_stock)
            - inventory.reserved_stock
        )

    # -----------------------------------------------------
    # PRODUCT PRICE CHANGE
    # -----------------------------------------------------

    elif workflow.request_type == "Product Price Change":

        product_id = changes.get("product_id")

        new_price = changes.get("new_price")

        product = (
            db.query(Product)
            .filter(
                Product.id == int(product_id),
                Product.company_id ==
                workflow.company_id
            )
            .first()
        )

        if not product:

            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )

        if new_price is None or float(new_price) <= 0:

            raise HTTPException(
                status_code=400,
                detail="Invalid product price."
            )

        product.unit_price = float(new_price)

    # -----------------------------------------------------
    # PRODUCT DEACTIVATION
    # -----------------------------------------------------

    elif workflow.request_type == "Product Deactivation":

        product_id = changes.get("product_id")

        product = (
            db.query(Product)
            .filter(
                Product.id == int(product_id),
                Product.company_id ==
                workflow.company_id
            )
            .first()
        )

        if not product:

            raise HTTPException(
                status_code=404,
                detail="Product not found."
            )

        product.status = "Inactive"

    # -----------------------------------------------------
    # CUSTOMER INFORMATION CHANGE
    # -----------------------------------------------------

    elif workflow.request_type == "Customer Information Change":

        customer_id = changes.get("customer_id")

        customer = (
            db.query(Customer)
            .filter(
                Customer.id == int(customer_id),
                Customer.company_id ==
                workflow.company_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found."
            )

        if "full_name" in changes:
            customer.full_name = changes["full_name"]

        if "email" in changes:
            customer.email = changes["email"]

        if "phone" in changes:
            customer.phone = changes["phone"]

    # -----------------------------------------------------
    # INVENTORY IMPORT APPROVAL
    # -----------------------------------------------------

    elif workflow.request_type == "Inventory Import Approval":

        import_id = changes.get("import_id")

        if not import_id:

            raise HTTPException(
                status_code=400,
                detail="Import ID is required."
            )