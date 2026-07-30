from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class ForecastHistory(Base):

    __tablename__ = "forecast_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    forecast_id = Column(
        Integer,
        ForeignKey("demand_forecasts.id"),
        nullable=False
    )

    historical_sales = Column(
        Float,
        default=0
    )

    prediction = Column(
        Float,
        default=0
    )

    accuracy = Column(
        Float,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    forecast = relationship(
        "DemandForecast",
        back_populates="history"
    )