from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Create Forecast
# -----------------------------
class ForecastCreate(BaseModel):

    forecast_period: str


# -----------------------------
# Forecast Response
# -----------------------------
class ForecastResponse(BaseModel):

    id: int

    product_id: int

    category_id: int

    forecast_period: str

    predicted_demand: float

    confidence_score: float

    generated_at: datetime

    class Config:

        from_attributes = True


# -----------------------------
# Forecast History Response
# -----------------------------
class ForecastHistoryResponse(BaseModel):

    id: int

    historical_sales: float

    prediction: float

    accuracy: float

    created_at: datetime

    class Config:

        from_attributes = True