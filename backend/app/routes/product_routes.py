from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)

from app.services.product_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
    search_products,
    filter_products,
    activate_product,
    deactivate_product,
    sort_products
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# -----------------------------
# Create Product
# -----------------------------
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def create_product_api(
    request: Request,
    product: ProductCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_product(
        db,
        current_user.company_id,
        current_user.id,
        product,
        request
    )


# -----------------------------
# Get All Products
# -----------------------------
@router.get(
    "/",
    response_model=list[ProductListResponse]
)
def get_all_products(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_products(
        db,
        current_user.company_id
    )


# -----------------------------
# Search Products
# -----------------------------
@router.get("/search")
def search_product(
    keyword: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return search_products(
        db,
        current_user.company_id,
        keyword
    )


# -----------------------------
# Filter Products
# -----------------------------
@router.get("/filter")
def filter_product(
    category_id: int | None = None,
    status: str | None = None,
    brand: str | None = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return filter_products(
        db,
        current_user.company_id,
        category_id,
        status,
        brand
    )

@router.get("/sort")
def sort_product(
    sort_by: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return sort_products(
        db,
        current_user.company_id,
        sort_by
    )


# -----------------------------
# Get Product By ID
# -----------------------------
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_api(
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_product(
        db,
        current_user.company_id,
        product_id
    )


# -----------------------------
# Update Product
# -----------------------------
@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_api(
    request: Request,
    product_id: int,
    product: ProductUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return update_product(
        db,
        current_user.company_id,
        current_user.id,
        product_id,
        product,
        request
    )


# -----------------------------
# Delete Product
# -----------------------------
@router.delete("/{product_id}")
def delete_product_api(
    request: Request,
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return delete_product(
        db,
        current_user.company_id,
        current_user.id,
        product_id,
        request
    )

# -----------------------------
# Activate Product
# -----------------------------
@router.patch(
    "/{product_id}/activate",
    response_model=ProductResponse
)
def activate_product_api(
    request: Request,
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return activate_product(
        db,
        current_user.company_id,
        current_user.id,
        product_id,
        request
    )


# -----------------------------
# Deactivate Product
# -----------------------------
@router.patch(
    "/{product_id}/deactivate",
    response_model=ProductResponse
)
def deactivate_product_api(
    request: Request,
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return deactivate_product(
        db,
        current_user.company_id,
        current_user.id,
        product_id,
        request
    )