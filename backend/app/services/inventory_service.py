from fastapi import HTTPException, Request

from sqlalchemy.orm import Session

from sqlalchemy import or_

from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.models.category import Category

from app.schemas.inventory_schema import (
    StockAdjustment,
    ReorderLevelUpdate
)

from app.services.notification_service import (
    create_notification
)

from app.services.audit_service import (
    create_audit_log
)


LOW_STOCK_THRESHOLD = 5


# =====================================================
# Calculate Available Stock
# =====================================================

def calculate_available_stock(

    current_stock: int,

    reserved_stock: int

):

    return current_stock - reserved_stock


# =====================================================
# Calculate Stock Status
# =====================================================

def calculate_stock_status(

    available_stock: int,

    reorder_level: int

):

    if available_stock == 0:

        return "Out Of Stock"

    elif available_stock <= reorder_level:

        return "Low Stock"

    else:

        return "In Stock"


# =====================================================
# Record Inventory Movement
# =====================================================

def record_inventory_movement(

    db: Session,

    inventory_id: int,

    movement_type: str,

    quantity_changed: int,

    previous_quantity: int,

    updated_quantity: int,

    reason: str,

    remarks: str,

    performed_by: int

):

    movement = InventoryMovement(

        inventory_id=inventory_id,

        movement_type=movement_type,

        quantity_changed=quantity_changed,

        previous_quantity=previous_quantity,

        updated_quantity=updated_quantity,

        reason=reason,

        remarks=remarks,

        performed_by=performed_by

    )

    db.add(movement)

    db.commit()

    db.refresh(movement)

    return movement


# =====================================================
# Create Inventory Record
# =====================================================

def create_inventory_record(

    db: Session,

    company_id: int,

    product_id: int,

    reorder_level: int = 5

):

    inventory = Inventory(

        company_id=company_id,

        product_id=product_id,

        current_stock=0,

        reserved_stock=0,

        available_stock=0,

        reorder_level=reorder_level,

        stock_status="Out Of Stock"

    )

    db.add(inventory)

    db.commit()

    db.refresh(inventory)

    return inventory


# =====================================================
# Get All Inventory
# =====================================================

def get_inventory(

    db: Session,

    company_id: int

):

    inventory = (

        db.query(

            Inventory,

            Product.name.label("product_name"),

            Product.sku.label("sku"),

            Category.name.label("category_name"),

            Product.brand.label("brand")

        )

        .join(

            Product,

            Inventory.product_id == Product.id

        )

        .join(

            Category,

            Product.category_id == Category.id

        )

        .filter(

            Inventory.company_id == company_id

        )

        .order_by(

            Product.name.asc()

        )

        .all()

    )

    result = []

    for inv, product_name, sku, category_name, brand in inventory:

        result.append({

            "id": inv.id,

            "company_id": inv.company_id,

            "product_id": inv.product_id,

            "product_name": product_name,

            "sku": sku,

            "category": category_name,

            "brand": brand,

            "current_stock": inv.current_stock,

            "reserved_stock": inv.reserved_stock,

            "available_stock": inv.available_stock,

            "reorder_level": inv.reorder_level,

            "stock_status": inv.stock_status,

            "updated_at": inv.updated_at

        })

    return result

# =====================================================
# Search Inventory
# =====================================================

def search_inventory(

    db: Session,

    company_id: int,

    keyword: str

):

    inventory = (

        db.query(

            Inventory,

            Product.name.label("product_name"),

            Product.sku.label("sku"),

            Category.name.label("category_name"),

            Product.brand.label("brand")

        )

        .join(
            Product,
            Inventory.product_id == Product.id
        )

        .join(
            Category,
            Product.category_id == Category.id
        )

        .filter(

            Inventory.company_id == company_id,

            or_(

                Product.name.ilike(f"%{keyword}%"),

                Product.sku.ilike(f"%{keyword}%")

            )

        )

        .order_by(Product.name.asc())

        .all()

    )

    result = []

    for inv, product_name, sku, category_name, brand in inventory:

        result.append({

            "id": inv.id,

            "company_id": inv.company_id,

            "product_id": inv.product_id,

            "product_name": product_name,

            "sku": sku,

            "category": category_name,

            "brand": brand,

            "current_stock": inv.current_stock,

            "reserved_stock": inv.reserved_stock,

            "available_stock": inv.available_stock,

            "reorder_level": inv.reorder_level,

            "stock_status": inv.stock_status,

            "updated_at": inv.updated_at

        })

    return result


# =====================================================
# Filter Inventory
# =====================================================

def filter_inventory(

    db: Session,

    company_id: int,

    category_id: int | None = None,

    brand: str | None = None,

    stock_status: str | None = None

):

    query = (

        db.query(

            Inventory,

            Product.name.label("product_name"),

            Product.sku.label("sku"),

            Category.name.label("category_name"),

            Product.brand.label("brand")

        )

        .join(
            Product,
            Inventory.product_id == Product.id
        )

        .join(
            Category,
            Product.category_id == Category.id
        )

        .filter(
            Inventory.company_id == company_id
        )

    )

    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )

    if brand:

        query = query.filter(
            Product.brand == brand
        )

    if stock_status:

        query = query.filter(
            Inventory.stock_status == stock_status
        )

    inventory = query.order_by(
        Product.name.asc()
    ).all()

    result = []

    for inv, product_name, sku, category_name, brand in inventory:

        result.append({

            "id": inv.id,

            "company_id": inv.company_id,

            "product_id": inv.product_id,

            "product_name": product_name,

            "sku": sku,

            "category": category_name,

            "brand": brand,

            "current_stock": inv.current_stock,

            "reserved_stock": inv.reserved_stock,

            "available_stock": inv.available_stock,

            "reorder_level": inv.reorder_level,

            "stock_status": inv.stock_status,

            "updated_at": inv.updated_at

        })

    return result


# =====================================================
# Sort Inventory
# =====================================================

def sort_inventory(

    db: Session,

    company_id: int,

    sort_by: str

):

    query = (

        db.query(

            Inventory,

            Product.name.label("product_name"),

            Product.sku.label("sku"),

            Category.name.label("category_name"),

            Product.brand.label("brand")

        )

        .join(
            Product,
            Inventory.product_id == Product.id
        )

        .join(
            Category,
            Product.category_id == Category.id
        )

        .filter(
            Inventory.company_id == company_id
        )

    )

    if sort_by == "product":

        query = query.order_by(
            Product.name.asc()
        )

    elif sort_by == "stock":

        query = query.order_by(
            Inventory.current_stock.desc()
        )

    elif sort_by == "updated":

        query = query.order_by(
            Inventory.updated_at.desc()
        )

    else:

        raise HTTPException(

            status_code=400,

            detail="Invalid sort option."

        )

    inventory = query.all()

    result = []

    for inv, product_name, sku, category_name, brand in inventory:

        result.append({

            "id": inv.id,

            "company_id": inv.company_id,

            "product_id": inv.product_id,

            "product_name": product_name,

            "sku": sku,

            "category": category_name,

            "brand": brand,

            "current_stock": inv.current_stock,

            "reserved_stock": inv.reserved_stock,

            "available_stock": inv.available_stock,

            "reorder_level": inv.reorder_level,

            "stock_status": inv.stock_status,

            "updated_at": inv.updated_at

        })

    return result


# =====================================================
# Get Inventory By Product
# =====================================================

def get_inventory_by_product(

    db: Session,

    company_id: int,

    product_id: int

):

    inventory = (

        db.query(Inventory)

        .filter(

            Inventory.company_id == company_id,

            Inventory.product_id == product_id

        )

        .first()

    )

    if not inventory:

        raise HTTPException(

            status_code=404,

            detail="Inventory record not found."

        )

    return inventory

# =====================================================
# Add Stock
# =====================================================

def add_stock(

    db: Session,

    company_id: int,

    user_id: int,

    product_id: int,

    data: StockAdjustment,

    request: Request

):

    inventory = get_inventory_by_product(
        db,
        company_id,
        product_id
    )

    if data.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero."
        )

    previous_quantity = inventory.current_stock

    inventory.current_stock += data.quantity

    inventory.available_stock = calculate_available_stock(

        inventory.current_stock,

        inventory.reserved_stock

    )

    inventory.stock_status = calculate_stock_status(

        inventory.available_stock,

        inventory.reorder_level

    )

    db.commit()
    db.refresh(inventory)

    record_inventory_movement(

        db=db,

        inventory_id=inventory.id,

        movement_type="Stock Addition",

        quantity_changed=data.quantity,

        previous_quantity=previous_quantity,

        updated_quantity=inventory.current_stock,

        reason=data.reason,

        remarks=data.remarks,

        performed_by=user_id

    )

    create_notification(

        db=db,

        company_id=company_id,

        title="Stock Added",

        message=f"{data.quantity} units added."

    )

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Stock Added",

        entity_name=str(product_id),

        ip_address=request.client.host,

        browser=request.headers.get("user-agent")

    )

    return inventory


# =====================================================
# Remove Stock
# =====================================================

def remove_stock(

    db: Session,

    company_id: int,

    user_id: int,

    product_id: int,

    data: StockAdjustment,

    request: Request

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    if data.quantity <= 0:

        raise HTTPException(

            status_code=400,

            detail="Quantity must be greater than zero."

        )

    if data.quantity > inventory.available_stock:

        raise HTTPException(

            status_code=400,

            detail="Insufficient stock."

        )

    previous_quantity = inventory.current_stock

    inventory.current_stock -= data.quantity

    inventory.available_stock = calculate_available_stock(

        inventory.current_stock,

        inventory.reserved_stock

    )

    inventory.stock_status = calculate_stock_status(

        inventory.available_stock,

        inventory.reorder_level

    )

    db.commit()
    db.refresh(inventory)

    record_inventory_movement(

        db=db,

        inventory_id=inventory.id,

        movement_type="Stock Removal",

        quantity_changed=data.quantity,

        previous_quantity=previous_quantity,

        updated_quantity=inventory.current_stock,

        reason=data.reason,

        remarks=data.remarks,

        performed_by=user_id

    )

    create_notification(

        db=db,

        company_id=company_id,

        title="Stock Removed",

        message=f"{data.quantity} units removed."

    )

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Stock Removed",

        entity_name=str(product_id),

        ip_address=request.client.host,

        browser=request.headers.get("user-agent")

    )

    return inventory


# =====================================================
# Manual Stock Adjustment
# =====================================================

def adjust_stock(

    db: Session,

    company_id: int,

    user_id: int,

    product_id: int,

    data: StockAdjustment,

    request: Request

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    previous_quantity = inventory.current_stock

    inventory.current_stock = data.quantity

    inventory.available_stock = calculate_available_stock(

        inventory.current_stock,

        inventory.reserved_stock

    )

    inventory.stock_status = calculate_stock_status(

        inventory.available_stock,

        inventory.reorder_level

    )

    db.commit()
    db.refresh(inventory)

    record_inventory_movement(

        db=db,

        inventory_id=inventory.id,

        movement_type="Manual Adjustment",

        quantity_changed=abs(

            previous_quantity -

            inventory.current_stock

        ),

        previous_quantity=previous_quantity,

        updated_quantity=inventory.current_stock,

        reason=data.reason,

        remarks=data.remarks,

        performed_by=user_id

    )

    create_notification(

        db=db,

        company_id=company_id,

        title="Stock Adjusted",

        message="Inventory adjusted manually."

    )

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Stock Adjusted",

        entity_name=str(product_id),

        ip_address=request.client.host,

        browser=request.headers.get("user-agent")

    )

    return inventory


# =====================================================
# Update Reorder Level
# =====================================================

def update_reorder_level(

    db: Session,

    company_id: int,

    user_id: int,

    product_id: int,

    data: ReorderLevelUpdate,

    request: Request

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    if data.reorder_level < 0:

        raise HTTPException(

            status_code=400,

            detail="Reorder level cannot be negative."

        )

    inventory.reorder_level = data.reorder_level

    inventory.stock_status = calculate_stock_status(

        inventory.available_stock,

        inventory.reorder_level

    )

    db.commit()
    db.refresh(inventory)

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Reorder Level Updated",

        entity_name=str(product_id),

        ip_address=request.client.host,

        browser=request.headers.get("user-agent")

    )

    return inventory

# =====================================================
# Get Inventory Movement History
# =====================================================

def get_inventory_movements(

    db: Session,

    company_id: int,

    product_id: int

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    movements = (

        db.query(
            InventoryMovement,
            Product.name.label("product_name")
        )

        .join(
            Inventory,
            Inventory.id == InventoryMovement.inventory_id
        )
        .join(
            Product,
            Product.id == Inventory.product_id
        )

        .filter(

            InventoryMovement.inventory_id == inventory.id

        )

        .order_by(

            InventoryMovement.created_at.desc()

        )

        .all()

    )

    result = []

    for movement, product_name in movements:

        result.append({

            "id": movement.id,

            "product_name": product_name,

            "movement_type": movement.movement_type,

            "quantity_changed": movement.quantity_changed,

            "previous_quantity": movement.previous_quantity,

            "updated_quantity": movement.updated_quantity,

            "reason": movement.reason,

            "remarks": movement.remarks,

            "performed_by": movement.performed_by,

            "created_at": movement.created_at

        })

    return result


# =====================================================
# Check Stock Status Notifications
# =====================================================

def check_stock_notifications(

    db: Session,

    company_id: int,

    inventory: Inventory,

    product_name: str

):

    if inventory.available_stock == 0:

        create_notification(

            db=db,

            company_id=company_id,

            title="Out Of Stock",

            message=f"{product_name} is Out Of Stock."

        )

    elif inventory.available_stock <= inventory.reorder_level:

        create_notification(

            db=db,

            company_id=company_id,

            title="Low Stock",

            message=(
                f"{product_name} stock is low. "
                f"Remaining quantity: {inventory.available_stock}"
            )

        )


# =====================================================
# Update Stock Status
# =====================================================

def refresh_stock_status(

    db: Session,

    company_id: int,

    inventory: Inventory,

    product_name: str

):

    inventory.available_stock = calculate_available_stock(

        inventory.current_stock,

        inventory.reserved_stock

    )

    inventory.stock_status = calculate_stock_status(

        inventory.available_stock,

        inventory.reorder_level

    )

    db.commit()

    db.refresh(inventory)

    check_stock_notifications(

        db,

        company_id,

        inventory,

        product_name

    )

    return inventory


# =====================================================
# Reserve Stock
# =====================================================

def reserve_stock(

    db: Session,

    company_id: int,

    product_id: int,

    quantity: int

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    if quantity > inventory.available_stock:

        raise HTTPException(

            status_code=400,

            detail="Insufficient available stock."

        )

    inventory.reserved_stock += quantity

    refresh_stock_status(

        db,

        company_id,

        inventory,

        ""

    )

    return inventory


# =====================================================
# Release Reserved Stock
# =====================================================

def release_reserved_stock(

    db: Session,

    company_id: int,

    product_id: int,

    quantity: int

):

    inventory = get_inventory_by_product(

        db,

        company_id,

        product_id

    )

    if quantity > inventory.reserved_stock:

        raise HTTPException(

            status_code=400,

            detail="Invalid reserved quantity."

        )

    inventory.reserved_stock -= quantity

    refresh_stock_status(

        db,

        company_id,

        inventory,

        ""

    )

    return inventory