from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse
)

from app.services.category_service import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
    search_categories
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# -----------------------------
# Create Category
# -----------------------------
@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201
)
def create_category_api(
    request: Request,
    category: CategoryCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return create_category(
        db,
        current_user.company_id,
        current_user.id,
        category,
        request
    )


# -----------------------------
# Get All Categories
# -----------------------------
@router.get(
    "/",
    response_model=list[CategoryListResponse]
)
def get_all_categories(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_categories(
        db,
        current_user.company_id
    )


# -----------------------------
# Search Categories
# -----------------------------
@router.get("/search")
def search_category(
    keyword: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return search_categories(
        db,
        current_user.company_id,
        keyword
    )


# -----------------------------
# Get Category By ID
# -----------------------------
@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category_api(
    category_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_category(
        db,
        current_user.company_id,
        category_id
    )


# -----------------------------
# Update Category
# -----------------------------
@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category_api(
    request: Request,
    category_id: int,
    category: CategoryUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return update_category(
        db,
        current_user.company_id,
        current_user.id,
        category_id,
        category,
        request
    )


# -----------------------------
# Delete Category
# -----------------------------
@router.delete("/{category_id}")
def delete_category_api(
    request: Request,
    category_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return delete_category(
        db,
        current_user.company_id,
        current_user.id,
        category_id,
        request
    )