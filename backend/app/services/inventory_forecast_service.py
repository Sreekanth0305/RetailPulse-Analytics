from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.category import Category


# =========================================================
# Task 11 Forecast Configuration
# =========================================================

HISTORICAL_DAYS = 30

DEFAULT_FORECAST_DAYS = 30

DEFAULT_LEAD_TIME_DAYS = 7

SAFETY_STOCK_DAYS = 3

OVERSTOCK_DAYS = 60


# =========================================================
# Calculate Average Daily Sales
# =========================================================

def calculate_average_daily_sales(
    db: Session,
    company_id: int,
    product_id: int,
    historical_days: int = HISTORICAL_DAYS
):

    start_date = datetime.now() - timedelta(
        days=historical_days
    )

    total_quantity = (
        db.query(
            func.coalesce(
                func.sum(SaleItem.quantity),
                0
            )
        )
        .join(
            Sale,
            Sale.id == SaleItem.sale_id
        )
        .filter(
            Sale.company_id == company_id,
            SaleItem.product_id == product_id,
            Sale.sale_date >= start_date
        )
        .scalar()
    )

    total_quantity = float(total_quantity or 0)

    if historical_days <= 0:
        return 0.0

    return total_quantity / historical_days


# =========================================================
# Days Of Stock Remaining
# =========================================================

def calculate_days_of_stock_remaining(
    current_stock: float,
    average_daily_sales: float
):

    if average_daily_sales <= 0:
        return None

    return current_stock / average_daily_sales


# =========================================================
# Forecasted Demand
# =========================================================

def calculate_forecasted_demand(
    average_daily_sales: float,
    forecast_days: int
):

    return average_daily_sales * forecast_days


# =========================================================
# Safety Stock
#
# Safety Stock = Average Daily Sales × Safety Stock Days
# =========================================================

def calculate_safety_stock(
    average_daily_sales: float
):

    return average_daily_sales * SAFETY_STOCK_DAYS


# =========================================================
# Reorder Point
#
# Reorder Point =
# Average Daily Sales × Lead Time
# + Safety Stock
# =========================================================

def calculate_reorder_point(
    average_daily_sales: float,
    lead_time_days: int
):

    safety_stock = calculate_safety_stock(
        average_daily_sales
    )

    return (
        average_daily_sales * lead_time_days
        + safety_stock
    )


# =========================================================
# Stock Risk
# =========================================================

def calculate_stock_risk(
    current_stock: float,
    average_daily_sales: float,
    reorder_point: float
):

    if current_stock <= 0:
        return "Out of Stock"

    if current_stock <= 5:
        return "Low Stock"

    if average_daily_sales <= 0:
        return "Healthy"

    days_remaining = (
        current_stock /
        average_daily_sales
    )

    if days_remaining <= 7:
        return "Stockout Risk"

    if current_stock <= reorder_point:
        return "Low Stock"

    if days_remaining >= OVERSTOCK_DAYS:
        return "Overstock"

    return "Healthy"


# =========================================================
# Recommendation
# =========================================================

def calculate_recommendation(
    current_stock: float,
    forecasted_demand: float,
    reorder_point: float
):

    target_stock = max(
        forecasted_demand,
        reorder_point
    )

    recommended_quantity = max(
        0,
        round(target_stock - current_stock)
    )

    if current_stock <= 0:
        return (
            recommended_quantity,
            "Immediate Restock Required"
        )

    if current_stock <= 5:
        return (
            recommended_quantity,
            "Reorder Required"
        )

    if current_stock < reorder_point:
        return (
            recommended_quantity,
            "Reorder Required"
        )

    if current_stock >= (
        forecasted_demand * 2
    ):
        return (
            0,
            "Overstock Detected"
        )

    return (
        recommended_quantity,
        "Stock Level Healthy"
    )


# =========================================================
# Get Inventory Forecast
# =========================================================

def get_inventory_forecast(
    db: Session,
    company_id: int,
    forecast_days: int = DEFAULT_FORECAST_DAYS,
    lead_time_days: int = DEFAULT_LEAD_TIME_DAYS,
    category_id: int | None = None,
    product_id: int | None = None,
    stock_risk: str | None = None,
    reorder_required: bool | None = None,
    sort_by: str | None = None
):

    if forecast_days <= 0:
        raise HTTPException(
            status_code=400,
            detail="Forecast days must be greater than zero."
        )

    if lead_time_days < 0:
        raise HTTPException(
            status_code=400,
            detail="Lead time cannot be negative."
        )

    query = (
        db.query(
            Inventory,
            Product.name.label("product_name"),
            Product.sku.label("sku"),
            Category.name.label("category_name")
        )
        .join(
            Product,
            Product.id == Inventory.product_id
        )
        .outerjoin(
            Category,
            Category.id == Product.category_id
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

    rows = query.all()

    results = []

    for (
        inventory,
        product_name,
        sku,
        category_name
    ) in rows:

        average_daily_sales = (
            calculate_average_daily_sales(
                db=db,
                company_id=company_id,
                product_id=inventory.product_id
            )
        )

        available_stock = (
            inventory.available_stock
            if inventory.available_stock is not None
            else inventory.current_stock
        )

        forecasted_demand = (
            calculate_forecasted_demand(
                average_daily_sales,
                forecast_days
            )
        )

        days_remaining = (
            calculate_days_of_stock_remaining(
                available_stock,
                average_daily_sales
            )
        )

        safety_stock = (
            calculate_safety_stock(
                average_daily_sales
            )
        )

        reorder_point = (
            calculate_reorder_point(
                average_daily_sales,
                lead_time_days
            )
        )

        risk = calculate_stock_risk(
            available_stock,
            average_daily_sales,
            reorder_point
        )

        (
            recommended_quantity,
            recommendation
        ) = calculate_recommendation(
            available_stock,
            forecasted_demand,
            reorder_point
        )

        needs_reorder = (
            available_stock <= 5
            or available_stock <= reorder_point
            or recommended_quantity > 0
        )

        result = {
            "product_id": inventory.product_id,
            "product_name": product_name,
            "sku": sku,
            "category_name": category_name,

            "current_stock": inventory.current_stock,
            "available_stock": available_stock,

            "average_daily_sales": round(
                average_daily_sales,
                2
            ),

            "forecasted_demand": round(
                forecasted_demand,
                2
            ),

            "days_of_stock_remaining": (
                round(days_remaining, 2)
                if days_remaining is not None
                else None
            ),

            "lead_time_days": lead_time_days,

            "safety_stock": round(
                safety_stock,
                2
            ),

            "reorder_point": round(
                reorder_point,
                2
            ),

            "recommended_reorder_quantity":
                recommended_quantity,

            "stock_risk": risk,

            "recommendation":
                recommendation,

            "reorder_required":
                needs_reorder
        }

        results.append(result)

    # -----------------------------------------
    # Risk Filter
    # -----------------------------------------

    if stock_risk:
        results = [
            item
            for item in results
            if item["stock_risk"] == stock_risk
        ]

    # -----------------------------------------
    # Reorder Filter
    # -----------------------------------------

    if reorder_required is not None:
        results = [
            item
            for item in results
            if item["reorder_required"]
            == reorder_required
        ]

    # -----------------------------------------
    # Sorting
    # -----------------------------------------

    if sort_by == "current_stock":
        results.sort(
            key=lambda x: x["current_stock"]
        )

    elif sort_by == "forecasted_demand":
        results.sort(
            key=lambda x: x["forecasted_demand"],
            reverse=True
        )

    elif sort_by == "days_remaining":
        results.sort(
            key=lambda x:
                x["days_of_stock_remaining"]
                if x["days_of_stock_remaining"]
                is not None
                else float("inf")
        )

    elif sort_by == "recommended_quantity":
        results.sort(
            key=lambda x:
                x["recommended_reorder_quantity"],
            reverse=True
        )

    elif sort_by == "risk":
        risk_order = {
            "Out of Stock": 1,
            "Stockout Risk": 2,
            "Low Stock": 3,
            "Healthy": 4,
            "Overstock": 5
        }

        results.sort(
            key=lambda x:
                risk_order.get(
                    x["stock_risk"],
                    99
                )
        )

    return results


# =========================================================
# Summary
# =========================================================

def get_inventory_forecast_summary(
    forecast_data
):

    return {
        "total_products":
            len(forecast_data),

        "products_requiring_reorder":
            sum(
                1
                for item in forecast_data
                if item["reorder_required"]
            ),

        "stockout_risk_products":
            sum(
                1
                for item in forecast_data
                if item["stock_risk"]
                in [
                    "Out of Stock",
                    "Stockout Risk"
                ]
            ),

        "overstocked_products":
            sum(
                1
                for item in forecast_data
                if item["stock_risk"]
                == "Overstock"
            ),

        "healthy_products":
            sum(
                1
                for item in forecast_data
                if item["stock_risk"]
                == "Healthy"
            )
    }


# =========================================================
# Single Product Recommendation
# =========================================================

def get_product_inventory_forecast(
    db: Session,
    company_id: int,
    product_id: int,
    forecast_days: int = DEFAULT_FORECAST_DAYS,
    lead_time_days: int = DEFAULT_LEAD_TIME_DAYS
):

    data = get_inventory_forecast(
        db=db,
        company_id=company_id,
        forecast_days=forecast_days,
        lead_time_days=lead_time_days,
        product_id=product_id
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Inventory forecast not found for this product."
        )

    return data[0]