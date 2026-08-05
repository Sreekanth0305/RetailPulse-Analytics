from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)

from app.services.customer_service import (
    create_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
    change_customer_status,
    get_customer_analytics,
    rebuild_customer_purchase_summary
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# ==========================================
# Create Customer
# ==========================================
@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer_api(

    request: Request,

    customer: CustomerCreate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return create_customer(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        customer=customer,

        request=request

    )


# ==========================================
# Get All Customers
# ==========================================
@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers_api(

    search: str | None = Query(None),

    customer_type: str | None = Query(None),

    status: str | None = Query(None),

    city: str | None = Query(None),

    state: str | None = Query(None),

    country: str | None = Query(None),

    registration_date: str | None = Query(None),

    sort_by: str | None = Query(None),

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_customers(

        db=db,

        company_id=current_user.company_id,

        search=search,

        customer_type=customer_type,

        status=status,

        city=city,

        state=state,

        country=country,

        registration_date=registration_date,

        sort_by=sort_by

    )


@router.get("/analytics")
def customer_analytics_api(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_customer_analytics(
        db,
        current_user.company_id
    )

@router.post("/rebuild-purchase-summary")
def rebuild_purchase_summary_api(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return rebuild_customer_purchase_summary(

        db=db,

        company_id=current_user.company_id

    )

# ==========================================
# Get Customer By ID
# ==========================================
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer_api(

    customer_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_customer_by_id(

        db=db,

        company_id=current_user.company_id,

        customer_id=customer_id

    )


# ==========================================
# Update Customer
# ==========================================
@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer_api(

    request: Request,

    customer_id: int,

    customer: CustomerUpdate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return update_customer(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        customer_id=customer_id,

        customer_data=customer,

        request=request

    )


# ==========================================
# Delete Customer
# ==========================================
@router.delete(
    "/{customer_id}"
)
def delete_customer_api(

    request: Request,

    customer_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return delete_customer(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        customer_id=customer_id,

        request=request

    )


# ==========================================
# Activate / Deactivate Customer
# ==========================================
@router.put(
    "/{customer_id}/status"
)
def change_customer_status_api(

    request: Request,

    customer_id: int,

    status: str,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return change_customer_status(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        customer_id=customer_id,

        status=status,

        request=request

    )