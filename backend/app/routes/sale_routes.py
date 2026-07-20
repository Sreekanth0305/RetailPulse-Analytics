from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.sale_schema import (
    SaleCreate,
    SaleUpdate,
    SaleResponse,
    SaleDetailResponse,
    SaleListResponse
)

from app.services.sale_service import (
    create_sale,
    get_sales,
    get_sale_details,
    update_sale,
    delete_sale,
    search_sales,
    filter_sales,
    sort_sales
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# -----------------------------
# Create Sale
# -----------------------------
@router.post(
    "/",
    response_model=SaleResponse,
    status_code=201
)
def create_sale_api(
    request: Request,
    sale: SaleCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_sale(

        db,

        current_user.company_id,

        current_user.id,

        sale,

        request

    )

# -----------------------------
# Get All Sales
# -----------------------------
@router.get(
    "/",
    response_model=list[SaleListResponse]
)
def get_all_sales(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("Logged User Company ID:", current_user.company_id)
    return get_sales(

        db,

        current_user.company_id

    )

# -----------------------------
# Search Sales
# -----------------------------
@router.get("/search")
def search_sale_api(
    keyword: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return search_sales(

        db,

        current_user.company_id,

        keyword

    )

# -----------------------------
# Filter Sales
# -----------------------------
@router.get("/filter")
def filter_sales_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return filter_sales(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Sort Sales
# -----------------------------
@router.get("/sort")
def sort_sales_api(

    sort_by: str,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return sort_sales(

        db=db,

        company_id=current_user.company_id,

        sort_by=sort_by

    )

# -----------------------------
# Sale Details
# -----------------------------
@router.get(
    "/{sale_id}",
    response_model=SaleDetailResponse
)
def get_sale_api(

    sale_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_sale_details(

        db,

        current_user.company_id,

        sale_id

    )
# -----------------------------
# Update Sale
# -----------------------------
@router.put(
    "/{sale_id}",
    response_model=SaleResponse
)
def update_sale_api(

    request: Request,

    sale_id: int,

    sale: SaleUpdate,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return update_sale(

        db,

        current_user.company_id,

        current_user.id,

        sale_id,

        sale,

        request

    )

# -----------------------------
# Delete Sale
# -----------------------------
@router.delete("/{sale_id}")
def delete_sale_api(

    request: Request,

    sale_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return delete_sale(

        db,

        current_user.company_id,

        current_user.id,

        sale_id,

        request

    )