from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.category import Category
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate
)

from app.services.audit_service import create_audit_log


# def build_product_response(
#     db: Session,
#     product: Product
# ):

#     category = (
#         db.query(Category)
#         .filter(Category.id == product.category_id)
#         .first()
#     )

#     return {
#         "id": product.id,
#         "company_id": product.company_id,
#         "category_id": product.category_id,
#         "category_name": category.name if category else "",
#         "name": product.name,
#         "sku": product.sku,
#         "brand": product.brand,
#         "description": product.description,
#         "unit_price": product.unit_price,
#         "cost_price": product.cost_price,
#         "stock_quantity": product.stock_quantity,
#         "unit_of_measure": product.unit_of_measure,
#         "status": product.status,
#         "created_at": product.created_at,
#         "updated_at": product.updated_at
#     }


# -----------------------------
# Create Product
# -----------------------------
def create_product(
    db: Session,
    company_id: int,
    user_id: int,
    product: ProductCreate,
    request: Request
):

    # SKU Validation
    existing_sku = (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.sku == product.sku
        )
        .first()
    )

    if existing_sku:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists."
        )

    # Duplicate Product Name Validation
    existing_name = (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.category_id == product.category_id,
            Product.name == product.name
        )
        .first()
    )

    if existing_name:
        raise HTTPException(
            status_code=400,
            detail="Product already exists in this category."
        )

    # Unit Price Validation
    if product.unit_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Unit Price must be greater than zero."
        )

    # Cost Price Validation
    if product.cost_price > product.unit_price:
        raise HTTPException(
            status_code=400,
            detail="Cost Price cannot exceed Unit Price."
        )

    # Stock Validation
    if product.stock_quantity < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock Quantity cannot be negative."
        )

    db_product = Product(
        company_id=company_id,
        category_id=product.category_id,
        name=product.name,
        sku=product.sku,
        brand=product.brand,
        description=product.description,
        unit_price=product.unit_price,
        cost_price=product.cost_price,
        stock_quantity=product.stock_quantity,
        unit_of_measure=product.unit_of_measure,
        status=product.status
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    create_audit_log(
    db=db,
    company_id=company_id,
    user_id=user_id,
    action="Product Created",
    entity_name=db_product.name,
    ip_address=request.client.host,
    browser=request.headers.get("user-agent")
    )

    return db_product


# -----------------------------
# Get All Products
# -----------------------------
def get_products(
    db: Session,
    company_id: int
):

    products = (

        db.query(Product, Category.name)

        .join(

            Category,

            Product.category_id == Category.id

        )

        .filter(

            Product.company_id == company_id

        )

        .all()

    )

    result = []

    for product, category_name in products:

        result.append({

            "id": product.id,

            "company_id": product.company_id,

            "category_id": product.category_id,

            "category_name": category_name,

            "name": product.name,

            "sku": product.sku,

            "brand": product.brand,

            "description": product.description,

            "unit_price": product.unit_price,

            "cost_price": product.cost_price,

            "stock_quantity": product.stock_quantity,

            "unit_of_measure": product.unit_of_measure,

            "status": product.status,

            "created_at": product.created_at,

            "updated_at": product.updated_at

        })

    return result


# -----------------------------
# Get Product By ID
# -----------------------------
def get_product(
    db: Session,
    company_id: int,
    product_id: int
):

    product = (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.id == product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product

# -----------------------------
# Update Product
# -----------------------------
def update_product(
    db: Session,
    company_id: int,
    user_id: int,
    product_id: int,
    data: ProductUpdate,
    request: Request
):

    product = get_product(
        db,
        company_id,
        product_id
    )

    product.category_id = data.category_id
    product.name = data.name
    product.sku = data.sku
    product.brand = data.brand
    product.description = data.description
    product.unit_price = data.unit_price
    product.cost_price = data.cost_price
    product.stock_quantity = data.stock_quantity
    product.unit_of_measure = data.unit_of_measure
    product.status = data.status

    db.commit()
    db.refresh(product)

    create_audit_log(
    db=db,
    company_id=company_id,
    user_id=user_id,
    action="Product Updated",
    entity_name=product.name,
    ip_address=request.client.host,
    browser=request.headers.get("user-agent")
    )

    return product


# -----------------------------
# Delete Product
# -----------------------------
def delete_product(
    db: Session,
    company_id: int,
    user_id: int,
    product_id: int,
    request: Request
):

    product = get_product(
        db,
        company_id,
        product_id
    )

    product_name = product.name
    db.delete(product)
    db.commit()

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Product Deleted",

    entity_name=product_name,

    ip_address=request.client.host,

    browser=request.headers.get("user-agent")

    )

    return {
        "message": "Product deleted successfully."
    }

# -----------------------------
# Activate Product
# -----------------------------
def activate_product(
    db: Session,
    company_id: int,
    user_id: int,
    product_id: int,
    request: Request
):

    product = get_product(
        db,
        company_id,
        product_id
    )

    product.status = "Active"

    db.commit()
    db.refresh(product)

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Product Activated",

    entity_name=product.name,

    ip_address=request.client.host,

    browser=request.headers.get("user-agent")

    )

    category = (
        db.query(Category)
        .filter(Category.id == product.category_id)
        .first()
    )

    return {

        "id": product.id,
        "company_id": product.company_id,
        "category_id": product.category_id,
        "category_name": category.name if category else "",
        "name": product.name,
        "sku": product.sku,
        "brand": product.brand,
        "description": product.description,
        "unit_price": product.unit_price,
        "cost_price": product.cost_price,
        "stock_quantity": product.stock_quantity,
        "unit_of_measure": product.unit_of_measure,
        "status": product.status,
        "created_at": product.created_at,
        "updated_at": product.updated_at

    }


# -----------------------------
# Deactivate Product
# -----------------------------
def deactivate_product(
    db: Session,
    company_id: int,
    user_id: int,
    product_id: int,
    request: Request
):

    product = get_product(
        db,
        company_id,
        product_id
    )

    product.status = "Inactive"

    db.commit()
    db.refresh(product)

    create_audit_log(

    db=db,

    company_id=company_id,

    user_id=user_id,

    action="Product Deactivated",

    entity_name=product.name,

    ip_address=request.client.host,

    browser=request.headers.get("user-agent")    

    )

    category = (
        db.query(Category)
        .filter(Category.id == product.category_id)
        .first()
    )

    return {

        "id": product.id,
        "company_id": product.company_id,
        "category_id": product.category_id,
        "category_name": category.name if category else "",
        "name": product.name,
        "sku": product.sku,
        "brand": product.brand,
        "description": product.description,
        "unit_price": product.unit_price,
        "cost_price": product.cost_price,
        "stock_quantity": product.stock_quantity,
        "unit_of_measure": product.unit_of_measure,
        "status": product.status,
        "created_at": product.created_at,
        "updated_at": product.updated_at

    }

# -----------------------------
# Search Products
# -----------------------------
def search_products(
    db: Session,
    company_id: int,
    keyword: str
):

    products = (

        db.query(Product, Category.name)

        .join(

            Category,

            Product.category_id == Category.id

        )

        .filter(

            Product.company_id == company_id,

            (

                Product.name.ilike(f"%{keyword}%") |

                Product.brand.ilike(f"%{keyword}%") |

                Product.sku.ilike(f"%{keyword}%")

            )

        )

        .all()

    )

    result = []

    for product, category_name in products:

        result.append({

            "id": product.id,

            "company_id": product.company_id,

            "category_id": product.category_id,

            "category_name": category_name,

            "name": product.name,

            "sku": product.sku,

            "brand": product.brand,

            "description": product.description,

            "unit_price": product.unit_price,

            "cost_price": product.cost_price,

            "stock_quantity": product.stock_quantity,

            "unit_of_measure": product.unit_of_measure,

            "status": product.status,

            "created_at": product.created_at,

            "updated_at": product.updated_at

        })

    return result


# -----------------------------
# Filter Products
# -----------------------------
def filter_products(
    db: Session,
    company_id: int,
    category_id: int | None = None,
    status: str | None = None,
    brand: str | None = None
):

    query = (

        db.query(Product, Category.name)

        .join(

            Category,

            Product.category_id == Category.id

        )

        .filter(

            Product.company_id == company_id

        )

    )

    if category_id:

        query = query.filter(

            Product.category_id == category_id

        )

    if status:

        query = query.filter(

            Product.status == status

        )

    if brand:

        query = query.filter(

            Product.brand.ilike(f"%{brand}%")

        )

    products = query.all()

    result = []

    for product, category_name in products:

        result.append({

            "id": product.id,

            "company_id": product.company_id,

            "category_id": product.category_id,

            "category_name": category_name,

            "name": product.name,

            "sku": product.sku,

            "brand": product.brand,

            "description": product.description,

            "unit_price": product.unit_price,

            "cost_price": product.cost_price,

            "stock_quantity": product.stock_quantity,

            "unit_of_measure": product.unit_of_measure,

            "status": product.status,

            "created_at": product.created_at,

            "updated_at": product.updated_at

        })

    return result

# -----------------------------
# Sort Products
# -----------------------------
def sort_products(
    db: Session,
    company_id: int,
    sort_by: str
):

    query = (
        db.query(Product, Category.name)
        .join(
            Category,
            Product.category_id == Category.id
        )
        .filter(
            Product.company_id == company_id
        )
    )

    if sort_by == "name":

        query = query.order_by(Product.name.asc())

    elif sort_by == "price":

        query = query.order_by(Product.unit_price.asc())

    elif sort_by == "recent":

        query = query.order_by(Product.created_at.desc())

    products = query.all()

    result = []

    for product, category_name in products:

        result.append({

            "id": product.id,
            "company_id": product.company_id,
            "category_id": product.category_id,
            "category_name": category_name,
            "name": product.name,
            "sku": product.sku,
            "brand": product.brand,
            "description": product.description,
            "unit_price": product.unit_price,
            "cost_price": product.cost_price,
            "stock_quantity": product.stock_quantity,
            "unit_of_measure": product.unit_of_measure,
            "status": product.status,
            "created_at": product.created_at,
            "updated_at": product.updated_at

        })

    return result