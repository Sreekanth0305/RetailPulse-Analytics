import csv
from io import StringIO
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from fastapi.responses import StreamingResponse
from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import desc

from app.models.product import Product
from app.models.category import Category
from app.models.sale_item import SaleItem
from app.models.sale import Sale
from app.models.demand_forecast import DemandForecast
from app.models.forecast_history import ForecastHistory

from app.services.notification_service import create_notification
from app.services.audit_service import create_audit_log


def calculate_confidence(historical_sales):

    historical_sales = float(historical_sales)

    if historical_sales >= 100:
        return 95

    elif historical_sales >= 50:
        return 90

    elif historical_sales >= 20:
        return 80

    return 70

def calculate_prediction(historical_sales):

    historical_sales = float(historical_sales)

    return round(historical_sales * 1.10, 2)

def generate_forecast(
    db: Session,
    company_id: int,
    user_id: int,
    forecast_period: str,
    request
):

    old_forecasts = (
        db.query(DemandForecast)
        .filter(
            DemandForecast.company_id == company_id,
            DemandForecast.forecast_period == forecast_period
        )
        .all()
    )
    
    for forecast in old_forecasts:
    
        db.query(ForecastHistory).filter(
            ForecastHistory.forecast_id == forecast.id
        ).delete()
    
        db.delete(forecast)
    
    db.flush()

    forecasts = []

    # -----------------------------
    # Active Products Only
    # -----------------------------

    products = (

        db.query(Product)

        .filter(

            Product.company_id == company_id,

            Product.status == "Active"

        )

        .all()

    )

    if not products:

        raise HTTPException(

            status_code=404,

            detail="No active products found."

        )

    # -----------------------------
    # Generate Forecast
    # -----------------------------

    for product in products:

        historical_sales = (

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

                SaleItem.product_id == product.id

            )

            .scalar()

        )

        # Ignore products without sales

        if historical_sales == 0:

            continue

        predicted = calculate_prediction(

            historical_sales

        )

        confidence = calculate_confidence(

            historical_sales

        )

        forecast = DemandForecast(

            company_id=company_id,

            product_id=product.id,

            category_id=product.category_id,

            forecast_period=forecast_period,

            predicted_demand=predicted,

            confidence_score=confidence,

            generated_at=datetime.utcnow()

        )

        db.add(forecast)

        db.flush()

        history = ForecastHistory(

            forecast_id=forecast.id,

            historical_sales=historical_sales,

            prediction=predicted,

            accuracy=confidence

        )

        db.add(history)

        forecasts.append(forecast)

    db.commit()

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Forecast Generated",
        entity_name=forecast_period,
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return [
        {
            "id": f.id,
            "product_id": f.product_id,
            "category_id": f.category_id,
            "forecast_period": f.forecast_period,
            "predicted_demand": float(f.predicted_demand),
            "confidence_score": f.confidence_score,
            "generated_at": f.generated_at,
        }
        for f in forecasts
    ]

def refresh_forecast(
    db: Session,
    company_id: int,
    user_id: int,
    forecast_period: str,
    request
):

    # Delete previous forecast history
    db.query(ForecastHistory).filter(
        ForecastHistory.forecast_id.in_(
            db.query(DemandForecast.id).filter(
                DemandForecast.company_id == company_id
            )
        )
    ).delete(synchronize_session=False)

    # Delete previous forecasts
    db.query(DemandForecast).filter(
        DemandForecast.company_id == company_id
    ).delete(synchronize_session=False)

    db.commit()

    # Generate new forecasts
    result = generate_forecast(
        db=db,
        company_id=company_id,
        user_id=user_id,
        forecast_period=forecast_period,
        request=request
    )
    
    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Forecast Refreshed",
        entity_name=forecast_period,
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )
    
    return result
def get_all_forecasts(
    db: Session,
    company_id: int,
    product: str = None,
    category: str = None,
    brand: str = None,
    period: str = None,
    sort_by: str = None
):

    query = (
        db.query(DemandForecast)
        .join(Product)
        .join(Category)
        .options(
            joinedload(DemandForecast.product)
        )
        .filter(
            DemandForecast.company_id == company_id
        )
    )

    # -----------------------
    # Product Filter
    # -----------------------

    if product:

        query = query.filter(
            Product.name.ilike(f"%{product}%")
        )

    # -----------------------
    # Category Filter
    # -----------------------

    if category:

        query = query.filter(
            Category.name.ilike(f"%{category}%")
        )

    # -----------------------
    # Brand Filter
    # -----------------------

    if brand:

        query = query.filter(
            Product.brand.ilike(f"%{brand}%")
        )

    # -----------------------
    # Forecast Period
    # -----------------------

    if period:

        query = query.filter(
            DemandForecast.forecast_period == period
        )

    # -----------------------
    # Sorting
    # -----------------------

    if sort_by == "highest_demand":

        query = query.order_by(
            desc(DemandForecast.predicted_demand)
        )

    elif sort_by == "lowest_stock":

        query = query.order_by(
            Product.stock_quantity.asc()
        )

    elif sort_by == "highest_growth":

        query = query.order_by(
            desc(DemandForecast.predicted_demand)
        )

    elif sort_by == "accuracy":

        query = query.order_by(
            desc(DemandForecast.confidence_score)
        )

    else:

        query = query.order_by(
            DemandForecast.generated_at.desc()
        )

    return query.all()


def get_product_forecasts(
    db: Session,
    company_id: int
):
    return (
        db.query(DemandForecast)
        .options(joinedload(DemandForecast.product))
        .filter(
            DemandForecast.company_id == company_id
        )
        .order_by(
            DemandForecast.predicted_demand.desc()
        )
        .all()
    )


def get_category_forecasts(
    db: Session,
    company_id: int
):

    forecasts = (
        db.query(
            Category.name.label("category"),
            func.sum(DemandForecast.predicted_demand).label("predicted_demand")
        )
        .join(
            Category,
            Category.id == DemandForecast.category_id
        )
        .filter(
            DemandForecast.company_id == company_id
        )
        .group_by(
            Category.name
        )
        .all()
    )

    return [
        {
            "category": row.category,
            "predicted_demand": float(row.predicted_demand)
        }
        for row in forecasts
    ]

def get_inventory_recommendations(
    db: Session,
    company_id: int,
    user_id: int,
    request
):

    forecasts = (
        db.query(DemandForecast)
        .options(joinedload(DemandForecast.product))
        .filter(
            DemandForecast.company_id == company_id
        )
        .all()
    )

    recommendations = []

    for forecast in forecasts:

        product = forecast.product

        current_stock = product.stock_quantity
        predicted_demand = float(forecast.predicted_demand)

        if current_stock == 0:

            recommendation = "Immediate Restock Required"

        elif current_stock < predicted_demand:

            recommendation = "Reorder Soon"

        elif current_stock > predicted_demand * 2:

            recommendation = "Overstock Risk"

        else:

            recommendation = "Stock Level Healthy"

        recommendations.append({

            "product_id": product.id,

            "product_name": product.name,

            "current_stock": current_stock,

            "predicted_demand": predicted_demand,

            "recommendation": recommendation

        })

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Inventory Recommendation Generated",
        entity_name="Forecast Recommendations",
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return recommendations

def export_demand_forecast_csv(
    db: Session,
    company_id: int,
    user_id: int,
    request
):

    forecasts = get_all_forecasts(
        db,
        company_id
    )

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Product",
        "Category",
        "Forecast Period",
        "Predicted Demand",
        "Confidence Score"
    ])

    for f in forecasts:

        writer.writerow([

            f.product.name,

            f.product.category.name,

            f.forecast_period,

            float(f.predicted_demand),

            f.confidence_score

        ])

    output.seek(0)

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Forecast Exported (CSV)",
        entity_name="Demand Forecast Report",
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return StreamingResponse(

        iter([output.getvalue()]),

        media_type="text/csv",

        headers={

            "Content-Disposition":

            "attachment; filename=demand_forecast.csv"

        }

    )

def export_category_forecast_csv(
    db: Session,
    company_id: int,
    user_id: int,
    request
):

    data = get_category_forecasts(
        db,
        company_id
    )

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "Category",

        "Predicted Demand"

    ])

    for row in data:

        writer.writerow([

            row["category"],

            row["predicted_demand"]

        ])

    output.seek(0)

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Forecast Exported (CSV)",
        entity_name="Category Forecast Report",
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return StreamingResponse(

        iter([output.getvalue()]),

        media_type="text/csv",

        headers={

            "Content-Disposition":

            "attachment; filename=category_forecast.csv"

        }

    )

def export_product_forecast_pdf(
    db: Session,
    company_id: int,
    user_id: int,
    request
):

    forecasts = get_product_forecasts(
        db,
        company_id
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    data = [[

        "Product",

        "Demand",

        "Confidence"

    ]]

    for f in forecasts:

        data.append([

            f.product.name,

            float(f.predicted_demand),

            f.confidence_score

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.grey),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white)

        ])

    )

    doc.build([table])

    buffer.seek(0)
 
    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Forecast Exported (PDF)",
        entity_name="Product Forecast Report",
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return StreamingResponse(

        buffer,

        media_type="application/pdf",

        headers={

            "Content-Disposition":

            "attachment; filename=product_forecast.pdf"

        }

    )

# ------------------------------------
# Forecast Notifications
# ------------------------------------

from app.services.notification_service import create_notification


def generate_forecast_notifications(
    db: Session,
    company_id: int
):

    forecasts = (
        db.query(DemandForecast)
        .options(joinedload(DemandForecast.product))
        .filter(
            DemandForecast.company_id == company_id
        )
        .all()
    )

    count = 0

    for forecast in forecasts:

        product = forecast.product

        if product is None:
            continue

        current_stock = product.stock_quantity
        predicted = float(forecast.predicted_demand)

        # Product predicted to run out
        if predicted >= current_stock:

            create_notification(
                db=db,
                company_id=company_id,
                title="Forecast Alert",
                message=f"{product.name} is predicted to run out of stock in {forecast.forecast_period}."
            )

            count += 1

        # High demand growth
        elif predicted >= current_stock * 0.8:

            create_notification(
                db=db,
                company_id=company_id,
                title="High Demand Forecast",
                message=f"{product.name} is expected to have high demand in {forecast.forecast_period}."
            )

            count += 1

    db.commit()

    return {
        "message": f"{count} forecast notifications generated."
    }

# ------------------------------------
# Historical Sales vs Forecast
# ------------------------------------

def historical_vs_forecast(
    db: Session,
    company_id: int
):

    result = (
        db.query(
            Product.name.label("product"),
            func.coalesce(func.sum(SaleItem.quantity), 0).label("historical_sales"),
            func.coalesce(DemandForecast.predicted_demand, 0).label("forecast")
        )
        .join(
            SaleItem,
            SaleItem.product_id == Product.id,
            isouter=True
        )
        .join(
            Sale,
            Sale.id == SaleItem.sale_id,
            isouter=True
        )
        .join(
            DemandForecast,
            DemandForecast.product_id == Product.id,
            isouter=True
        )
        .filter(
            Product.company_id == company_id
        )
        .group_by(
            Product.id,
            Product.name,
            DemandForecast.predicted_demand
        )
        .all()
    )

    return [
        {
            "product": r.product,
            "historical_sales": int(r.historical_sales),
            "forecast": float(r.forecast)
        }
        for r in result
    ]  

# ------------------------------------
# Product Demand Trend
# ------------------------------------

def product_demand_trend(
    db: Session,
    company_id: int
):

    forecasts = (
        db.query(DemandForecast)
        .options(joinedload(DemandForecast.product))
        .filter(
            DemandForecast.company_id == company_id
        )
        .order_by(
            DemandForecast.predicted_demand.desc()
        )
        .all()
    )

    return [

        {

            "product": f.product.name,

            "predicted_demand": float(f.predicted_demand)

        }

        for f in forecasts

    ] 

# ------------------------------------
# Category Demand Trend
# ------------------------------------

def category_demand_trend(
    db: Session,
    company_id: int
):

    result = (
        db.query(
            Category.name,
            func.sum(
                DemandForecast.predicted_demand
            ).label("predicted")
        )
        .join(
            DemandForecast,
            DemandForecast.category_id == Category.id
        )
        .filter(
            DemandForecast.company_id == company_id
        )
        .group_by(
            Category.name
        )
        .all()
    )

    return [

        {

            "category": r.name,

            "predicted_demand": float(r.predicted)

        }

        for r in result

    ]

# ------------------------------------
# Top Predicted Products
# ------------------------------------

def top_predicted_products(
    db: Session,
    company_id: int
):

    forecasts = (
        db.query(DemandForecast)
        .options(joinedload(DemandForecast.product))
        .filter(
            DemandForecast.company_id == company_id
        )
        .order_by(
            DemandForecast.predicted_demand.desc()
        )
        .limit(10)
        .all()
    )

    return [

        {

            "product": f.product.name,

            "predicted_demand": float(f.predicted_demand)

        }

        for f in forecasts

    ]

# ------------------------------------
# Seasonal Sales Pattern
# ------------------------------------

def seasonal_sales_pattern(
    db: Session,
    company_id: int
):

    result = (
        db.query(

            func.extract(
                "month",
                Sale.sale_date
            ).label("month"),

            func.sum(
                SaleItem.quantity
            ).label("sales")

        )
        .join(
            SaleItem,
            Sale.id == SaleItem.sale_id
        )
        .filter(
            Sale.company_id == company_id
        )
        .group_by(
            func.extract(
                "month",
                Sale.sale_date
            )
        )
        .order_by(
            func.extract(
                "month",
                Sale.sale_date
            )
        )
        .all()
    )

    return [

        {

            "month": int(r.month),

            "sales": int(r.sales)

        }

        for r in result

    ]