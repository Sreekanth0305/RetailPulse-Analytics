from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class DemandForecast(Base):

    __tablename__ = "demand_forecasts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    forecast_period = Column(
        String(50),
        nullable=False
    )

    predicted_demand = Column(
        Float,
        default=0
    )

    confidence_score = Column(
        Float,
        default=0
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    company = relationship("Company")

    product = relationship("Product")

    category = relationship("Category")

    history = relationship(
        "ForecastHistory",
        back_populates="forecast",
        cascade="all, delete-orphan"
    )