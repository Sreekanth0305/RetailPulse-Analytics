from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.category import Category
from app.models.product import Product
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)

from app.services.audit_service import create_audit_log


# -----------------------------
# Create Category
# -----------------------------
def create_category(
    db: Session,
    company_id: int,
    user_id: int,
    category: CategoryCreate
):

    existing = (
        db.query(Category)
        .filter(
            Category.company_id == company_id,
            Category.name == category.name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists."
        )

    db_category = Category(
        company_id=company_id,
        name=category.name,
        description=category.description,
        status=category.status
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Category Created",

    entity_name=db_category.name

    )

    return db_category


# -----------------------------
# Get All Categories
# -----------------------------
def get_categories(
    db: Session,
    company_id: int
):

    categories = (
        db.query(
            Category,
            func.count(Product.id).label("total_products")
        )
        .outerjoin(
            Product,
            Product.category_id == Category.id
        )
        .filter(
            Category.company_id == company_id
        )
        .group_by(Category.id)
        .all()
    )

    result = []

    for category, total_products in categories:

        result.append({

            "id": category.id,
            "name": category.name,
            "description": category.description,
            "status": category.status,
            "total_products": total_products

        })

    return result


# -----------------------------
# Get Category By ID
# -----------------------------
def get_category(
    db: Session,
    company_id: int,
    category_id: int
):

    category = (
        db.query(Category)
        .filter(
            Category.company_id == company_id,
            Category.id == category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found."
        )

    return category


# -----------------------------
# Update Category
# -----------------------------
def update_category(
    db: Session,
    company_id: int,
    user_id: int,
    category_id: int,
    data: CategoryUpdate
):

    category = get_category(
        db,
        company_id,
        category_id
    )

    category.name = data.name
    category.description = data.description
    category.status = data.status

    db.commit()
    db.refresh(category)

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Category Updated",

    entity_name=category.name

    )

    return category


# -----------------------------
# Delete Category
# -----------------------------
def delete_category(
    db: Session,
    company_id: int,
    user_id: int,
    category_id: int
):

    category = get_category(
        db,
        company_id,
        category_id
    )

    category_name = category.name

    db.delete(category)
    db.commit()

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Category Deleted",

    entity_name=category_name

    )

    return {
        "message": "Category deleted successfully."
    }


# -----------------------------
# Search Categories
# -----------------------------
def search_categories(
    db: Session,
    company_id: int,
    keyword: str
):

    return (
        db.query(Category)
        .filter(
            Category.company_id == company_id,
            Category.name.ilike(f"%{keyword}%")
        )
        .all()
    )