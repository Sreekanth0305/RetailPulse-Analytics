from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, String

from fastapi import HTTPException

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.category import Category


# =====================================================
# Dashboard KPI Cards
# =====================================================

def get_dashboard_kpis(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):
    
    sales_query = (
        db.query(Sale)
        .filter(Sale.company_id == company_id)
    )

    if start_date:
        sales_query = sales_query.filter(
            func.date(Sale.sale_date) >= start_date
        )

    if end_date:
        sales_query = sales_query.filter(
            func.date(Sale.sale_date) <= end_date
        )

    if sales_channel:
        sales_query = sales_query.filter(
            Sale.sales_channel == sales_channel
        )

    if payment_method:
        sales_query = sales_query.filter(
            Sale.payment_method == payment_method
        )

    if (
        category_id
        or product_id
        or brand
    ):

        sales_query = (
            sales_query
            .join(
                SaleItem,
                Sale.id == SaleItem.sale_id
            )
            .join(
                Product,
                Product.id == SaleItem.product_id
            )
        )

        if category_id:
            sales_query = sales_query.filter(
                SaleItem.category_id == category_id
            )

        if product_id:
            sales_query = sales_query.filter(
                SaleItem.product_id == product_id
            )

        if brand:
            sales_query = sales_query.filter(
                Product.brand == brand
            )

    sales_query = sales_query.distinct()  

    # -----------------------------------
    # Inventory Query (For Inventory KPIs)
    # -----------------------------------
    
    inventory_query = (
        db.query(Inventory)
        .join(
            Product,
            Product.id == Inventory.product_id
        )
        .filter(
            Inventory.company_id == company_id
        )
    )
    
    if category_id:
        inventory_query = inventory_query.filter(
            Product.category_id == category_id
        )
    
    if product_id:
        inventory_query = inventory_query.filter(
            Product.id == product_id
        )
    
    if brand:
        inventory_query = inventory_query.filter(
            Product.brand == brand
        )

    # -----------------------------------
    # Total Revenue
    # -----------------------------------

    total_revenue = (
        sales_query.with_entities(
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            )
        )
        .scalar()
    )

    # -----------------------------------
    # Total Orders
    # -----------------------------------

    total_orders = sales_query.count()

    # -----------------------------------
    # Total Products Sold
    # -----------------------------------

    items_query = (
        db.query(SaleItem)
        .join(
            Sale,
            Sale.id == SaleItem.sale_id
        )
        .join(
            Product,
            Product.id == SaleItem.product_id
        )
        .filter(
            Sale.company_id == company_id
        )
    )
    
    if start_date:
        items_query = items_query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
        items_query = items_query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
        items_query = items_query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
        items_query = items_query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id:
        items_query = items_query.filter(
            SaleItem.category_id == category_id
        )
    
    if product_id:
        items_query = items_query.filter(
            SaleItem.product_id == product_id
        )
    
    if brand:
        items_query = items_query.filter(
            Product.brand == brand
        )
    
    total_products_sold = (
        items_query.with_entities(
            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            )
        )
        .scalar()
    )
    # -----------------------------------
    # Average Order Value
    # -----------------------------------

    average_order_value = 0

    if total_orders > 0:

        average_order_value = (

            total_revenue / total_orders

        )

    # -----------------------------------
    # Total Inventory Value
    # -----------------------------------

    inventory_value = (
        inventory_query
        .with_entities(
            func.coalesce(
                func.sum(
                    Inventory.current_stock *
                    Product.cost_price
                ),
                0
            )
        )
        .scalar()
    )

    # -----------------------------------
    # Low Stock Products
    # -----------------------------------

    low_stock_products = (
        inventory_query
        .filter(
            Inventory.stock_status == "Low Stock"
        )
        .count()
    )

    # -----------------------------------
    # Out Of Stock Products
    # -----------------------------------

    out_of_stock_products = (
        inventory_query
        .filter(
            Inventory.stock_status == "Out Of Stock"
        )
        .count()
    )

    # -----------------------------------
    # Total Categories
    # -----------------------------------

    category_query = (
        db.query(Category)
        .filter(
            Category.company_id == company_id
        )
    )
    
    if category_id:
        category_query = category_query.filter(
            Category.id == category_id
        )
    
    total_categories = category_query.count()

    return {

        "total_revenue": total_revenue,

        "total_orders": total_orders,

        "total_products_sold": total_products_sold,

        "average_order_value": round(

            average_order_value,

            2

        ),

        "total_inventory_value": inventory_value,

        "low_stock_products": low_stock_products,

        "out_of_stock_products": out_of_stock_products,

        "total_categories": total_categories

    }

# -------------------------------------------------
# Revenue Trend
# -------------------------------------------------

def get_revenue_trend(
    db: Session,
    company_id: int,
    period: str,
    start_date: str | None = None,
    end_date: str | None = None,
    category_id: int | None = None,
    product_id: int | None = None,
    brand: str | None = None,
    sales_channel: str | None = None,
    payment_method: str | None = None
):

    query = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id
        )
    )
    
    if start_date:
        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
        query = query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
        query = query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id or product_id or brand:
    
        query = (
            query
            .join(
                SaleItem,
                Sale.id == SaleItem.sale_id
            )
            .join(
                Product,
                Product.id == SaleItem.product_id
            )
        )
    
        if category_id:
            query = query.filter(
                SaleItem.category_id == category_id
            )
    
        if product_id:
            query = query.filter(
                SaleItem.product_id == product_id
            )
    
        if brand:
            query = query.filter(
                Product.brand == brand
            )
    
    query = query.distinct()
    
    if period == "daily":

        results = (

            query.with_entities(

                func.date(Sale.sale_date).label("period"),

                func.sum(Sale.total_amount).label("revenue")

            )

            .group_by(

                func.date(Sale.sale_date)

            )

            .order_by(

                func.date(Sale.sale_date)

            )

            .all()

        )

    elif period == "weekly":

        results = (

            query.with_entities(

                func.yearweek(Sale.sale_date).label("period"),

                func.sum(Sale.total_amount).label("revenue")

            )

            .group_by(

                func.yearweek(Sale.sale_date)

            )

            .order_by(

                func.yearweek(Sale.sale_date)

            )

            .all()

        )

    elif period == "monthly":

        results = (

            query.with_entities(

                func.date_format(

                    Sale.sale_date,

                    "%Y-%m"

                ).label("period"),

                func.sum(Sale.total_amount).label("revenue")

            )

            .group_by(

                func.date_format(

                    Sale.sale_date,

                    "%Y-%m"

                )

            )

            .order_by(

                func.date_format(

                    Sale.sale_date,

                    "%Y-%m"

                )

            )

            .all()

        )

    else:

        raise HTTPException(

            status_code=400,

            detail="Period must be daily, weekly or monthly."

        )

    return [

        {

            "period": str(row.period),

            "revenue": float(row.revenue)

        }

        for row in results

    ]

# -----------------------------
# Sales Trend
# -----------------------------
def get_sales_trend(

    db: Session,

    company_id: int,

    period: str,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):
    query = (

        db.query(Sale)
    
        .filter(
    
            Sale.company_id == company_id
    
        )
    
    )

    print("INSIDE UPDATED get_sales_trend")
    
    if start_date:
    
        query = query.filter(
    
            func.date(Sale.sale_date) >= start_date
    
        )
    
    if end_date:
    
        query = query.filter(
    
            func.date(Sale.sale_date) <= end_date
    
        )
    
    if sales_channel:
    
        query = query.filter(
    
            Sale.sales_channel == sales_channel
    
        )
    
    if payment_method:
    
        query = query.filter(
    
            Sale.payment_method == payment_method
    
        )
    
    if category_id or product_id or brand:
    
        query = (
    
            query
    
            .join(
    
                SaleItem,
    
                Sale.id == SaleItem.sale_id
    
            )
    
            .join(
    
                Product,
    
                Product.id == SaleItem.product_id
    
            )
    
        )
    
        if category_id:
    
            query = query.filter(
    
                SaleItem.category_id == category_id
    
            )
    
        if product_id:
    
            query = query.filter(
    
                SaleItem.product_id == product_id
    
            )
    
        if brand:
    
            query = query.filter(
    
                Product.brand == brand
    
            )
    
    if category_id or product_id or brand:
        query = query.distinct()
    
    if period == "daily":

        trend = (
    
            query.with_entities(
    
                cast(
                    func.date(Sale.sale_date),
                    String
                ).label("period"),
    
                func.count(Sale.id).label("orders")
    
            )
    
            .group_by(
    
                func.date(Sale.sale_date)
    
            )
    
            .order_by(
    
                func.date(Sale.sale_date)
    
            )
    
            .all()
    
        )
    
    elif period == "weekly":

        trend = (
    
            query.with_entities(
    
                func.date_format(
                    Sale.sale_date,
                    "%x-W%v"
                ).label("period"),
    
                func.count(Sale.id).label("orders")
    
            )
    
            .group_by(
    
                func.date_format(
                    Sale.sale_date,
                    "%x-W%v"
                )
    
            )
    
            .order_by(
    
                func.date_format(
                    Sale.sale_date,
                    "%x-W%v"
                )
    
            )
    
            .all()
    
        )
    
    else:
    
        trend = (
    
            query.with_entities(
    
                func.date_format(
    
                    Sale.sale_date,
    
                    "%Y-%m"
    
                ).label("period"),
    
                func.count(Sale.id).label("orders")
    
            )
    
            .group_by(
    
                func.date_format(
    
                    Sale.sale_date,
    
                    "%Y-%m"
    
                )
    
            )
    
            .order_by(
    
                func.date_format(
    
                    Sale.sale_date,
    
                    "%Y-%m"
    
                )
    
            )
    
            .all()
    
        )

    print(trend)

    return [

        {
    
            "period": str(row.period),
    
            "orders": int(row.orders)
    
        }
    
        for row in trend
    
    ]

# -----------------------------
# Top 10 Best Selling Products
# -----------------------------
def get_top_selling_products(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Product.name.label("product_name"),
    
            func.sum(
                SaleItem.quantity
            ).label("quantity_sold")
    
        )
    
        .join(
    
            SaleItem,
    
            Product.id == SaleItem.product_id
    
        )
    
        .join(
    
            Sale,
    
            Sale.id == SaleItem.sale_id
    
        )
    
        .filter(
    
            Product.company_id == company_id
    
        )
    
    )

    if start_date:

        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
    
        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
    
        query = query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
    
        query = query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id:
    
        query = query.filter(
            SaleItem.category_id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            SaleItem.product_id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    products = (

        query
    
        .group_by(
    
            Product.id,
    
            Product.name
    
        )
    
        .order_by(
    
            desc("quantity_sold")
    
        )
    
        .limit(10)
    
        .all()
    
    )

    return [

        {

            "product_name": row.product_name,

            "quantity_sold": row.quantity_sold

        }

        for row in products

    ]

# -----------------------------
# Top Performing Categories
# -----------------------------
def get_top_categories(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Category.name.label("category_name"),
    
            func.sum(
                SaleItem.quantity
            ).label("quantity_sold")
    
        )
    
        .join(
    
            SaleItem,
    
            Category.id == SaleItem.category_id
    
        )
    
        .join(
    
            Sale,
    
            Sale.id == SaleItem.sale_id
    
        )
    
        .join(
    
            Product,
    
            Product.id == SaleItem.product_id
    
        )
    
        .filter(
    
            Category.company_id == company_id
    
        )
    
    )

    if start_date:

        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
    
        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
    
        query = query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
    
        query = query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id:
    
        query = query.filter(
            SaleItem.category_id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            SaleItem.product_id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )
    
    categories = (

        query
    
        .group_by(
    
            Category.id,
    
            Category.name
    
        )
    
        .order_by(
    
            desc("quantity_sold")
    
        )
    
        .all()
    
    )

    return [

        {

            "category_name": row.category_name,

            "quantity_sold": row.quantity_sold

        }

        for row in categories

    ]

# -----------------------------
# Sales By Payment Method
# -----------------------------
def get_sales_by_payment_method(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Sale.payment_method,
    
            func.count(
                Sale.id
            ).label("total_sales")
    
        )
    
        .filter(
    
            Sale.company_id == company_id
    
        )
    
    )

    if start_date:

        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
    
        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
    
        query = query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
    
        query = query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id or product_id or brand:
    
        query = (
    
            query
    
            .join(
                SaleItem,
                Sale.id == SaleItem.sale_id
            )
    
            .join(
                Product,
                Product.id == SaleItem.product_id
            )
    
        )
    
        if category_id:
    
            query = query.filter(
                SaleItem.category_id == category_id
            )
    
        if product_id:
    
            query = query.filter(
                SaleItem.product_id == product_id
            )
    
        if brand:
    
            query = query.filter(
                Product.brand == brand
            )
    
    query = query.distinct()

    payment_methods = (

    query

    .group_by(

        Sale.payment_method

    )

    .order_by(

        func.count(Sale.id).desc()

    )

    .all()

)

    return [

        {

            "payment_method": row.payment_method,

            "total_sales": row.total_sales

        }

        for row in payment_methods

    ]

# -----------------------------
# Sales By Sales Channel
# -----------------------------
def get_sales_by_sales_channel(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Sale.sales_channel,
    
            func.count(
                Sale.id
            ).label("total_sales")
    
        )
    
        .filter(
    
            Sale.company_id == company_id
    
        )
    
    )

    if start_date:

        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )
    
    if end_date:
    
        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )
    
    if sales_channel:
    
        query = query.filter(
            Sale.sales_channel == sales_channel
        )
    
    if payment_method:
    
        query = query.filter(
            Sale.payment_method == payment_method
        )
    
    if category_id or product_id or brand:
    
        query = (
    
            query
    
            .join(
                SaleItem,
                Sale.id == SaleItem.sale_id
            )
    
            .join(
                Product,
                Product.id == SaleItem.product_id
            )
    
        )
    
        if category_id:
    
            query = query.filter(
                SaleItem.category_id == category_id
            )
    
        if product_id:
    
            query = query.filter(
                SaleItem.product_id == product_id
            )
    
        if brand:
    
            query = query.filter(
                Product.brand == brand
            )
    
    query = query.distinct()

    sales_channels = (

        query
    
        .group_by(
    
            Sale.sales_channel
    
        )
    
        .order_by(
    
            func.count(Sale.id).desc()
    
        )
    
        .all()
    
    )

    return [

        {

            "sales_channel": row.sales_channel,

            "total_sales": row.total_sales

        }

        for row in sales_channels

    ]

# -----------------------------
# Inventory Distribution By Category
# -----------------------------
def get_inventory_distribution(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Category.name.label("category_name"),
    
            func.sum(
                Inventory.current_stock
            ).label("current_stock")
    
        )
    
        .join(
    
            Product,
    
            Product.category_id == Category.id
    
        )
    
        .join(
    
            Inventory,
    
            Inventory.product_id == Product.id
    
        )
    
        .filter(
    
            Category.company_id == company_id
    
        )
    
    )

    if category_id:

        query = query.filter(
            Category.id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            Product.id == product_id
        )
        
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    inventory = (

        query
    
        .group_by(
    
            Category.id,
    
            Category.name
    
        )
    
        .order_by(
    
            Category.name
    
        )
    
        .all()
    
    )
    
    return [

        {

            "category_name": row.category_name,

            "current_stock": row.current_stock

        }

        for row in inventory

    ]

# -----------------------------
# Stock Status Summary
# -----------------------------
def get_stock_status_summary(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Inventory.stock_status,
    
            func.count(
                Inventory.id
            ).label("total_products")
    
        )
    
        .join(
    
            Product,
    
            Product.id == Inventory.product_id
    
        )
    
        .filter(
    
            Inventory.company_id == company_id
    
        )
    
    )

    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            Product.id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    summary = (

        query
    
        .group_by(
    
            Inventory.stock_status
    
        )
    
        .order_by(
    
            Inventory.stock_status
    
        )
    
        .all()
    
    )
    return [

        {

            "stock_status": row.stock_status,

            "total_products": row.total_products

        }

        for row in summary

    ]

# -----------------------------
# Top Low Stock Products
# -----------------------------
def get_low_stock_products(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Product.name.label("product_name"),
    
            Inventory.current_stock,
    
            Inventory.reorder_level
    
        )
    
        .join(
    
            Inventory,
    
            Product.id == Inventory.product_id
    
        )
    
        .filter(
    
            Inventory.company_id == company_id,
    
            Inventory.current_stock <= Inventory.reorder_level,
    
            Inventory.current_stock > 0
    
        )
    
    )

    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            Product.id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    products = (

        query
    
        .order_by(
    
            Inventory.current_stock.asc()
    
        )
    
        .limit(10)
    
        .all()
    
    )

    return [

        {

            "product_name": row.product_name,

            "current_stock": row.current_stock,

            "reorder_level": row.reorder_level

        }

        for row in products

    ]

# -----------------------------
# Out Of Stock Products
# -----------------------------
def get_out_of_stock_products(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Product.name.label("product_name"),
    
            Inventory.current_stock
    
        )
    
        .join(
    
            Inventory,
    
            Product.id == Inventory.product_id
    
        )
    
        .filter(
    
            Inventory.company_id == company_id,
    
            Inventory.current_stock == 0
    
        )
    
    )

    if category_id:

        query = query.filter(
            Product.category_id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            Product.id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    products = (

        query
    
        .order_by(
    
            Product.name.asc()
    
        )
    
        .all()
    
    )

    return [

        {

            "product_name": row.product_name,

            "current_stock": row.current_stock

        }

        for row in products

    ]

# -----------------------------
# Inventory Value By Category
# -----------------------------
def get_inventory_value_by_category(

    db: Session,

    company_id: int,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None

):

    query = (

        db.query(
    
            Category.name.label("category_name"),
    
            func.coalesce(
    
                func.sum(
    
                    Inventory.current_stock *
    
                    Product.cost_price
    
                ),
    
                0
    
            ).label("inventory_value")
    
        )
    
        .join(
    
            Product,
    
            Product.category_id == Category.id
    
        )
    
        .join(
    
            Inventory,
    
            Inventory.product_id == Product.id
    
        )
    
        .filter(
    
            Category.company_id == company_id
    
        )
    
    )

    if category_id:

        query = query.filter(
            Category.id == category_id
        )
    
    if product_id:
    
        query = query.filter(
            Product.id == product_id
        )
    
    if brand:
    
        query = query.filter(
            Product.brand == brand
        )

    categories = (

        query
    
        .group_by(
    
            Category.id,
    
            Category.name
    
        )
    
        .order_by(
    
            Category.name
    
        )
    
        .all()
    
    )

    return [

        {

            "category_name": row.category_name,

            "inventory_value": row.inventory_value

        }

        for row in categories

    ]

def get_drilldown_categories(

    db: Session,

    company_id: int

):

    categories = (

        db.query(
    
            Category.id.label("id"),
    
            Category.name.label("name"),
    
            func.count(Product.id).label("total_products")
    
        )
    
        .outerjoin(
    
            Product,
    
            Product.category_id == Category.id
    
        )
    
        .filter(
    
            Category.company_id == company_id
    
        )
    
        .group_by(
    
            Category.id,
    
            Category.name
    
        )
    
        .order_by(
    
            Category.name
    
        )
    
        .all()
    
    )

    return categories

def get_drilldown_products(

    db: Session,

    company_id: int,

    category_id: int

):

    products = (

        db.query(

            Product.id.label("id"),

            Product.name.label("name"),

            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            ).label("total_sold")

        )

        .outerjoin(
            SaleItem,
            Product.id == SaleItem.product_id
        )

        .filter(

            Product.company_id == company_id,

            Product.category_id == category_id

        )

        .group_by(

            Product.id,

            Product.name

        )

        .order_by(

            Product.name

        )

        .all()

    )

    return products

def get_drilldown_sales(

    db: Session,

    company_id: int,

    product_id: int

):

    sales = (

        db.query(

            Sale.invoice_number,

            Sale.customer_name,

            Sale.sale_date,

            Sale.total_amount,

            SaleItem.quantity,

            Sale.payment_method,

            Sale.sales_channel

        )

        .join(

            SaleItem,

            Sale.id == SaleItem.sale_id

        )

        .filter(

            Sale.company_id == company_id,

            SaleItem.product_id == product_id

        )

        .order_by(

            Sale.sale_date.desc()

        )

        .all()

    )

    return sales