from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.services.inventory_forecast_service import (
    get_inventory_forecast,
    get_inventory_forecast_summary,
    get_product_inventory_forecast
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Forecast"]
)


# =========================================================
# GET /inventory/forecast
# =========================================================

@router.get("/forecast")
def inventory_forecast(
    forecast_days: int = 30,
    lead_time_days: int = 7,

    category_id: int | None = None,
    product_id: int | None = None,

    stock_risk: str | None = None,

    reorder_required: bool | None = None,

    sort_by: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    data = get_inventory_forecast(
        db=db,

        company_id=current_user.company_id,

        forecast_days=forecast_days,

        lead_time_days=lead_time_days,

        category_id=category_id,

        product_id=product_id,

        stock_risk=stock_risk,

        reorder_required=reorder_required,

        sort_by=sort_by
    )

    return {
        "summary":
            get_inventory_forecast_summary(data),

        "products":
            data
    }


# =========================================================
# GET /inventory/recommendations
# =========================================================

@router.get("/recommendations")
def inventory_recommendations(
    forecast_days: int = 30,

    lead_time_days: int = 7,

    category_id: int | None = None,

    stock_risk: str | None = None,

    reorder_required: bool | None = True,

    sort_by: str | None = "recommended_quantity",

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    data = get_inventory_forecast(
        db=db,

        company_id=current_user.company_id,

        forecast_days=forecast_days,

        lead_time_days=lead_time_days,

        category_id=category_id,

        stock_risk=stock_risk,

        reorder_required=reorder_required,

        sort_by=sort_by
    )

    return data


# =========================================================
# GET /inventory/recommendations/{product_id}
# =========================================================

@router.get(
    "/recommendations/{product_id}"
)
def product_inventory_recommendation(
    product_id: int,

    forecast_days: int = 30,

    lead_time_days: int = 7,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):

    return get_product_inventory_forecast(
        db=db,

        company_id=current_user.company_id,

        product_id=product_id,

        forecast_days=forecast_days,

        lead_time_days=lead_time_days
    )