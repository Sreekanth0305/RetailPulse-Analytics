import json
from datetime import datetime, timedelta

from sqlalchemy import func, desc, asc

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement
from app.models.customer import Customer
from app.models.user import User
from app.models.report_history import ReportHistory


# ---------------------------------------------------------
# Supported report types
# ---------------------------------------------------------

REPORT_TYPES = [
    "Sales Report",
    "Inventory Report",
    "Customer Report",
    "Product Performance Report",
    "Stock Movement Report",
]


# ---------------------------------------------------------
# Date filter helper
# ---------------------------------------------------------

def apply_date_filter(query, column, filters):
    """
    Applies date_from and date_to filters.

    Expected format:
    {
        "date_from": "2026-01-01",
        "date_to": "2026-01-31"
    }
    """

    date_from = filters.get("date_from")
    date_to = filters.get("date_to")

    if date_from:
        start_date = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.filter(column >= start_date)

    if date_to:
        end_date = datetime.strptime(date_to, "%Y-%m-%d")
        end_date = end_date + timedelta(days=1)

        query = query.filter(column < end_date)

    return query


# ---------------------------------------------------------
# Pagination helper
# ---------------------------------------------------------

def paginate_query(query, page, limit):
    """
    Applies pagination to a SQLAlchemy query.
    """

    total = query.count()

    offset = (page - 1) * limit

    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return items, total, total_pages


# ---------------------------------------------------------
# Sales Report
# ---------------------------------------------------------

def generate_sales_report(
    db,
    company_id,
    filters,
    page,
    limit,
    sort_by,
    sort_order,
):
    """
    Generates Sales Report.

    Uses:
        sales
        sale_items
        products
        categories
        users
    """

    query = (
        db.query(
            Sale.id,
            Sale.invoice_number,
            Sale.sale_date,
            Sale.customer_name,
            Sale.sales_channel,
            Sale.payment_method,
            Sale.subtotal,
            Sale.discount,
            Sale.tax,
            Sale.total_amount,
            Sale.payment_status,
            User.name.label("created_by_name"),
        )
        .join(
            User,
            Sale.created_by == User.id
        )
        .filter(
            Sale.company_id == company_id
        )
    )

    # Date filter
    query = apply_date_filter(
        query,
        Sale.sale_date,
        filters
    )

    # Customer filter
    if filters.get("customer"):
        query = query.filter(
            Sale.customer_name.ilike(
                f"%{filters['customer']}%"
            )
        )

    # Sales status filter
    if filters.get("sales_status"):
        query = query.filter(
            Sale.payment_status == filters["sales_status"]
        )

    # User filter
    if filters.get("user_id"):
        query = query.filter(
            Sale.created_by == filters["user_id"]
        )

    # Product/category/brand filters
    product_filter = filters.get("product_id")
    category_filter = filters.get("category_id")
    brand_filter = filters.get("brand")
    
    if (
        product_filter
        or category_filter
        or brand_filter
    ):
        sale_ids = (
            db.query(SaleItem.sale_id)
            .join(
                Product,
                SaleItem.product_id == Product.id
            )
            .join(
                Category,
                SaleItem.category_id == Category.id
            )
            .filter(
                Product.company_id == company_id
            )
        )
    
        # Product filter
        if product_filter:
            sale_ids = sale_ids.filter(
                SaleItem.product_id == int(product_filter)
            )
    
        # Category filter
        if category_filter:
            sale_ids = sale_ids.filter(
                SaleItem.category_id == int(category_filter)
            )
    
        # Brand filter
        if brand_filter:
            sale_ids = sale_ids.filter(
                Product.brand.ilike(
                    f"%{brand_filter}%"
                )
            )
    
        query = query.filter(
            Sale.id.in_(sale_ids)
        )

    # Sorting
    sort_columns = {
        "id": Sale.id,
        "invoice_number": Sale.invoice_number,
        "sale_date": Sale.sale_date,
        "customer_name": Sale.customer_name,
        "total_amount": Sale.total_amount,
        "payment_status": Sale.payment_status,
    }

    sort_column = sort_columns.get(
        sort_by,
        Sale.sale_date
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    items, total, total_pages = paginate_query(
        query,
        page,
        limit
    )

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "invoice_number": item.invoice_number,
            "sale_date": item.sale_date,
            "customer_name": item.customer_name,
            "sales_channel": item.sales_channel,
            "payment_method": item.payment_method,
            "subtotal": item.subtotal,
            "discount": item.discount,
            "tax": item.tax,
            "total_amount": item.total_amount,
            "payment_status": item.payment_status,
            "created_by": item.created_by_name,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ---------------------------------------------------------
# Inventory Report
# ---------------------------------------------------------

def generate_inventory_report(
    db,
    company_id,
    filters,
    page,
    limit,
    sort_by,
    sort_order,
):
    """
    Generates Inventory Report.
    """

    query = (
        db.query(
            Inventory.id,
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.sku,
            Product.brand,
            Category.name.label("category_name"),
            Inventory.current_stock,
            Inventory.reserved_stock,
            Inventory.available_stock,
            Inventory.reorder_level,
            Inventory.stock_status,
            Inventory.updated_at,
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
            Product.company_id == company_id,
        )
    )

    # Date filter
    query = apply_date_filter(
        query,
        Inventory.updated_at,
        filters
    )

    # Product filter
    if filters.get("product"):
        query = query.filter(
            Product.name.ilike(
                f"%{filters['product']}%"
            )
        )

    # Category filter
    if filters.get("category"):
        query = query.filter(
            Category.name.ilike(
                f"%{filters['category']}%"
            )
        )

    # Brand filter
    if filters.get("brand"):
        query = query.filter(
            Product.brand.ilike(
                f"%{filters['brand']}%"
            )
        )

    # Stock status
    if filters.get("stock_status"):
        query = query.filter(
            Inventory.stock_status
            == filters["stock_status"]
        )

    # Sorting
    sort_columns = {
        "product_name": Product.name,
        "current_stock": Inventory.current_stock,
        "available_stock": Inventory.available_stock,
        "stock_status": Inventory.stock_status,
        "updated_at": Inventory.updated_at,
    }

    sort_column = sort_columns.get(
        sort_by,
        Inventory.updated_at
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    items, total, total_pages = paginate_query(
        query,
        page,
        limit
    )

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "sku": item.sku,
            "brand": item.brand,
            "category": item.category_name,
            "current_stock": item.current_stock,
            "reserved_stock": item.reserved_stock,
            "available_stock": item.available_stock,
            "reorder_level": item.reorder_level,
            "stock_status": item.stock_status,
            "updated_at": item.updated_at,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ---------------------------------------------------------
# Customer Report
# ---------------------------------------------------------

def generate_customer_report(
    db,
    company_id,
    filters,
    page,
    limit,
    sort_by,
    sort_order,
):
    """
    Generates Customer Report.
    """

    query = (
        db.query(
            Customer.id,
            Customer.customer_id,
            Customer.full_name,
            Customer.email,
            Customer.phone,
            Customer.gender,
            Customer.city,
            Customer.state,
            Customer.country,
            Customer.customer_type,
            Customer.preferred_sales_channel,
            Customer.status,
            Customer.segment,
            Customer.created_at,
        )
        .filter(
            Customer.company_id == company_id,
            Customer.is_deleted == False,
        )
    )

    # Date filter
    query = apply_date_filter(
        query,
        Customer.created_at,
        filters
    )

    # Customer filter
    if filters.get("customer"):
        query = query.filter(
            Customer.full_name.ilike(
                f"%{filters['customer']}%"
            )
        )

    # Customer status
    if filters.get("status"):
        query = query.filter(
            Customer.status == filters["status"]
        )

    # Sorting
    sort_columns = {
        "id": Customer.id,
        "customer_id": Customer.customer_id,
        "full_name": Customer.full_name,
        "customer_type": Customer.customer_type,
        "status": Customer.status,
        "created_at": Customer.created_at,
    }

    sort_column = sort_columns.get(
        sort_by,
        Customer.created_at
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    items, total, total_pages = paginate_query(
        query,
        page,
        limit
    )

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "customer_id": item.customer_id,
            "full_name": item.full_name,
            "email": item.email,
            "phone": item.phone,
            "gender": item.gender,
            "city": item.city,
            "state": item.state,
            "country": item.country,
            "customer_type": item.customer_type,
            "preferred_sales_channel": item.preferred_sales_channel,
            "status": item.status,
            "segment": item.segment,
            "created_at": item.created_at,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ---------------------------------------------------------
# Product Performance Report
# ---------------------------------------------------------

def generate_product_performance_report(
    db,
    company_id,
    filters,
    page,
    limit,
    sort_by,
    sort_order,
):
    """
    Generates Product Performance Report.

    Calculates:
        quantity sold
        revenue
        number of sales
        estimated profit
    """

    query = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.sku,
            Product.brand,
            Category.name.label("category_name"),

            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            ).label("quantity_sold"),

            func.coalesce(
                func.sum(SaleItem.total),
                0
            ).label("revenue"),

            func.count(
                func.distinct(Sale.id)
            ).label("number_of_sales"),

            func.coalesce(
                func.sum(
                    SaleItem.quantity
                    * (
                        Product.unit_price
                        - Product.cost_price
                    )
                ),
                0
            ).label("estimated_profit"),

        )
        .join(
            Category,
            Product.category_id == Category.id
        )
        .outerjoin(
            SaleItem,
            SaleItem.product_id == Product.id
        )
        .outerjoin(
            Sale,
            Sale.id == SaleItem.sale_id
        )
        .filter(
            Product.company_id == company_id
        )
    )

    # Date filter
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")

    if date_from:
        start_date = datetime.strptime(
            date_from,
            "%Y-%m-%d"
        )

        query = query.filter(
            Sale.sale_date >= start_date
        )

    if date_to:
        end_date = datetime.strptime(
            date_to,
            "%Y-%m-%d"
        ) + timedelta(days=1)

        query = query.filter(
            Sale.sale_date < end_date
        )

    # Product
    if filters.get("product"):
        query = query.filter(
            Product.name.ilike(
                f"%{filters['product']}%"
            )
        )

    # Category
    if filters.get("category"):
        query = query.filter(
            Category.name.ilike(
                f"%{filters['category']}%"
            )
        )

    # Brand
    if filters.get("brand"):
        query = query.filter(
            Product.brand.ilike(
                f"%{filters['brand']}%"
            )
        )

    # Customer
    if filters.get("customer"):
        query = query.filter(
            Sale.customer_name.ilike(
                f"%{filters['customer']}%"
            )
        )

    # Sales status
    if filters.get("sales_status"):
        query = query.filter(
            Sale.payment_status
            == filters["sales_status"]
        )

    # User
    if filters.get("user_id"):
        query = query.filter(
            Sale.created_by == filters["user_id"]
        )

    query = query.group_by(
        Product.id,
        Product.name,
        Product.sku,
        Product.brand,
        Category.name,
    )

    # Sorting
    sort_columns = {
        "product_name": Product.name,
        "quantity_sold": func.sum(SaleItem.quantity),
        "revenue": func.sum(SaleItem.total),
        "number_of_sales": func.count(
            func.distinct(Sale.id)
        ),
        "estimated_profit": func.sum(
            SaleItem.quantity
            * (
                Product.unit_price
                - Product.cost_price
            )
        ),
    }

    sort_column = sort_columns.get(
        sort_by,
        func.sum(SaleItem.total)
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    items, total, total_pages = paginate_query(
        query,
        page,
        limit
    )

    result = []

    for item in items:
        result.append({
            "product_id": item.product_id,
            "product_name": item.product_name,
            "sku": item.sku,
            "brand": item.brand,
            "category": item.category_name,
            "quantity_sold": item.quantity_sold,
            "revenue": float(item.revenue or 0),
            "number_of_sales": item.number_of_sales,
            "estimated_profit": float(
                item.estimated_profit or 0
            ),
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ---------------------------------------------------------
# Stock Movement Report
# ---------------------------------------------------------

def generate_stock_movement_report(
    db,
    company_id,
    filters,
    page,
    limit,
    sort_by,
    sort_order,
):
    """
    Generates Stock Movement Report.

    InventoryMovement is used as the stock movement table.
    """

    query = (
        db.query(
            InventoryMovement.id,
            Product.name.label("product_name"),
            Product.sku,
            Product.brand,
            Category.name.label("category_name"),
            InventoryMovement.movement_type,
            InventoryMovement.quantity_changed,
            InventoryMovement.previous_quantity,
            InventoryMovement.updated_quantity,
            InventoryMovement.reason,
            InventoryMovement.remarks,
            User.name.label("performed_by_name"),
            InventoryMovement.created_at,
            Inventory.stock_status,
        )
        .join(
            Inventory,
            InventoryMovement.inventory_id
            == Inventory.id
        )
        .join(
            Product,
            Inventory.product_id
            == Product.id
        )
        .join(
            Category,
            Product.category_id
            == Category.id
        )
        .join(
            User,
            InventoryMovement.performed_by
            == User.id
        )
        .filter(
            Inventory.company_id == company_id,
            Product.company_id == company_id,
        )
    )

    # Date filter
    query = apply_date_filter(
        query,
        InventoryMovement.created_at,
        filters
    )

    # Product
    if filters.get("product"):
        query = query.filter(
            Product.name.ilike(
                f"%{filters['product']}%"
            )
        )

    # Category
    if filters.get("category"):
        query = query.filter(
            Category.name.ilike(
                f"%{filters['category']}%"
            )
        )

    # Brand
    if filters.get("brand"):
        query = query.filter(
            Product.brand.ilike(
                f"%{filters['brand']}%"
            )
        )

    # Stock status
    if filters.get("stock_status"):
        query = query.filter(
            Inventory.stock_status
            == filters["stock_status"]
        )

    # User
    if filters.get("user_id"):
        query = query.filter(
            InventoryMovement.performed_by
            == filters["user_id"]
        )

    # Movement type
    if filters.get("movement_type"):
        query = query.filter(
            InventoryMovement.movement_type
            == filters["movement_type"]
        )

    # Sorting
    sort_columns = {
        "id": InventoryMovement.id,
        "product_name": Product.name,
        "quantity_changed":
            InventoryMovement.quantity_changed,
        "created_at":
            InventoryMovement.created_at,
        "movement_type":
            InventoryMovement.movement_type,
    }

    sort_column = sort_columns.get(
        sort_by,
        InventoryMovement.created_at
    )

    if sort_order.lower() == "asc":
        query = query.order_by(
            asc(sort_column)
        )
    else:
        query = query.order_by(
            desc(sort_column)
        )

    items, total, total_pages = paginate_query(
        query,
        page,
        limit
    )

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "product_name": item.product_name,
            "sku": item.sku,
            "brand": item.brand,
            "category": item.category_name,
            "movement_type": item.movement_type,
            "quantity_changed": item.quantity_changed,
            "previous_quantity": item.previous_quantity,
            "updated_quantity": item.updated_quantity,
            "reason": item.reason,
            "remarks": item.remarks,
            "performed_by": item.performed_by_name,
            "stock_status": item.stock_status,
            "created_at": item.created_at,
        })

    return {
        "items": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


# ---------------------------------------------------------
# Main Report Generator
# ---------------------------------------------------------

def generate_report(
    db,
    company_id,
    user_id,
    report_type,
    filters=None,
    page=1,
    limit=20,
    sort_by="",
    sort_order="desc",
):
    """
    Main function used by the API route.

    It selects the correct report generator
    based on report_type.
    """

    if filters is None:
        filters = {}

    if report_type not in REPORT_TYPES:
        raise ValueError(
            f"Unsupported report type: {report_type}"
        )

    if page < 1:
        page = 1

    if limit < 1:
        limit = 20

    try:

        if report_type == "Sales Report":

            report_data = generate_sales_report(
                db=db,
                company_id=company_id,
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        elif report_type == "Inventory Report":

            report_data = generate_inventory_report(
                db=db,
                company_id=company_id,
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        elif report_type == "Customer Report":

            report_data = generate_customer_report(
                db=db,
                company_id=company_id,
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        elif report_type == "Product Performance Report":

            report_data = generate_product_performance_report(
                db=db,
                company_id=company_id,
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        elif report_type == "Stock Movement Report":

            report_data = generate_stock_movement_report(
                db=db,
                company_id=company_id,
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        generated_at = datetime.utcnow()

        # -------------------------------------------------
        # Save successful report generation in history
        # -------------------------------------------------

        history = ReportHistory(
            company_id=company_id,
            user_id=user_id,
            report_type=report_type,
            filters=json.dumps(filters),
            export_format=None,
            status="Success",
            error_message=None,
            generated_at=generated_at,
        )

        db.add(history)
        db.commit()

        return {
            "report_type": report_type,
            "generated_at": generated_at,
            "filters": filters,
            "items": report_data["items"],
            "total": report_data["total"],
            "page": report_data["page"],
            "limit": report_data["limit"],
            "total_pages": report_data["total_pages"],
        }

    except Exception as e:

        db.rollback()

        # -------------------------------------------------
        # Save failed report generation in history
        # -------------------------------------------------

        try:

            history = ReportHistory(
                company_id=company_id,
                user_id=user_id,
                report_type=report_type,
                filters=json.dumps(filters),
                export_format=None,
                status="Failed",
                error_message=str(e),
                generated_at=datetime.utcnow(),
            )

            db.add(history)
            db.commit()

        except Exception:
            db.rollback()

        raise