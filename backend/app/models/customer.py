from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.config.database import Base


class Customer(Base):

    __tablename__ = "customers"

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

    customer_id = Column(
        String(20),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=True
    )

    gender = Column(
        String(20),
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    city = Column(
        String(100),
        nullable=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    customer_type = Column(
        String(50),
        nullable=False
    )

    preferred_sales_channel = Column(
        String(50),
        nullable=True
    )

    status = Column(
        String(20),
        default="Active"
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    segment = Column(
        String(30),
        default="New Customer"
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

    company = relationship(
        "Company",
        back_populates="customers"
    )

    purchase_summary=relationship(

        "CustomerPurchaseSummary",
    
        uselist=False,
    
        back_populates="customer",
    
        cascade="all, delete-orphan"
    
    )