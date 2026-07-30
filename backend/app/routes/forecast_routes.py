from fastapi import APIRouter, Depends
from fastapi import Request

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.routes.auth_routes import get_current_user

from app.services.forecast_service import (
    generate_forecast,
    get_all_forecasts,
    get_product_forecasts,
    get_category_forecasts,
    get_inventory_recommendations,
    export_demand_forecast_csv,
    export_product_forecast_pdf,
    export_category_forecast_csv,
    generate_forecast_notifications,
    historical_vs_forecast,
    product_demand_trend,
    category_demand_trend,
    top_predicted_products,
    seasonal_sales_pattern
)

router = APIRouter(
    prefix="/forecast",
    tags=["Demand Forecast"]
)


# ------------------------------------
# Generate Forecast
# ------------------------------------
@router.post("/generate")
def generate_forecast_api(
    request: Request,
    forecast_period: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return generate_forecast(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        forecast_period=forecast_period,
        request=request
    )

# ------------------------------------
# Get All Forecasts
# ------------------------------------
@router.get("/")
def get_forecasts_api(

    product: str = None,
    category: str = None,
    brand: str = None,
    period: str = None,
    sort_by: str = None,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):

    return get_all_forecasts(

        db=db,

        company_id=current_user.company_id,

        product=product,

        category=category,

        brand=brand,

        period=period,

        sort_by=sort_by

    )

# ------------------------------------
# Product Forecast
# ------------------------------------
@router.get("/product")
def get_product_forecast_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_product_forecasts(
        db=db,
        company_id=current_user.company_id
    )


# ------------------------------------
# Category Forecast
# ------------------------------------
@router.get("/category")
def get_category_forecast_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_category_forecasts(
        db=db,
        company_id=current_user.company_id
    )

# ------------------------------------
# Inventory Recommendation
# ------------------------------------

@router.get("/recommendations")
def inventory_recommendation_api(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_inventory_recommendations(
        db=db,
        company_id=current_user.company_id,
        user_id=current_user.id,
        request=request
    )

@router.get("/export/csv")
def export_forecast_csv(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return export_demand_forecast_csv(

        db,

        current_user.company_id

    )

@router.get("/export/category/csv")
def export_category_csv(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return export_category_forecast_csv(

        db,

        current_user.company_id

    )

@router.get("/export/product/pdf")
def export_product_pdf(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return export_product_forecast_pdf(

        db,

        current_user.company_id

    )

# ------------------------------------
# Forecast Notifications
# ------------------------------------

@router.post("/notifications")
def forecast_notifications_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return generate_forecast_notifications(
        db=db,
        company_id=current_user.company_id
    )

# ------------------------------------
# Historical Sales vs Forecast
# ------------------------------------

@router.get("/charts/historical-vs-forecast")
def historical_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return historical_vs_forecast(
        db,
        current_user.company_id
    )


# ------------------------------------
# Product Trend
# ------------------------------------

@router.get("/charts/product-trend")
def product_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return product_demand_trend(
        db,
        current_user.company_id
    )


# ------------------------------------
# Category Trend
# ------------------------------------

@router.get("/charts/category-trend")
def category_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return category_demand_trend(
        db,
        current_user.company_id
    )


# ------------------------------------
# Top Products
# ------------------------------------

@router.get("/charts/top-products")
def top_products_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return top_predicted_products(
        db,
        current_user.company_id
    )


# ------------------------------------
# Seasonal Pattern
# ------------------------------------

@router.get("/charts/seasonal")
def seasonal_chart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return seasonal_sales_pattern(
        db,
        current_user.company_id
    )