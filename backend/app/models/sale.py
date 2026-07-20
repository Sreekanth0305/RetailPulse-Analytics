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


class Sale(Base):

    __tablename__ = "sales"

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

    invoice_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    customer_name = Column(
        String(150),
        nullable=False
    )

    sale_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    sales_channel = Column(
        String(50),
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan"
    )