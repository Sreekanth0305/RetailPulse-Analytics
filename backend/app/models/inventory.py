from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    String
)

from sqlalchemy.sql import func

from app.config.database import Base


class Inventory(Base):

    __tablename__ = "inventory"

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
        nullable=False,
        unique=True
    )

    current_stock = Column(
        Integer,
        default=0
    )

    reserved_stock = Column(
        Integer,
        default=0
    )

    available_stock = Column(
        Integer,
        default=0
    )

    reorder_level = Column(
        Integer,
        default=5
    )

    stock_status = Column(
        String(30),
        default="In Stock"
    )

    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )