from pydantic import BaseModel
from typing import Optional


class InventoryForecastResponse(BaseModel):
    product_id: int
    product_name: str
    sku: str
    category_name: Optional[str] = None

    current_stock: int
    available_stock: int

    average_daily_sales: float
    forecasted_demand: float

    days_of_stock_remaining: Optional[float]

    lead_time_days: int
    safety_stock: float
    reorder_point: float

    recommended_reorder_quantity: int

    stock_risk: str
    recommendation: str

    reorder_required: bool


class InventoryForecastSummary(BaseModel):
    total_products: int
    products_requiring_reorder: int
    stockout_risk_products: int
    overstocked_products: int
    healthy_products: int


class InventoryForecastDashboardResponse(BaseModel):
    summary: InventoryForecastSummary
    products: list[InventoryForecastResponse]