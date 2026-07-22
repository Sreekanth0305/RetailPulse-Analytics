from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.config.database import Base


class InventoryMovement(Base):

    __tablename__ = "inventory_movements"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    inventory_id = Column(
        Integer,
        ForeignKey("inventory.id"),
        nullable=False
    )

    movement_type = Column(
        String(50),
        nullable=False
    )

    quantity_changed = Column(
        Integer,
        nullable=False
    )

    previous_quantity = Column(
        Integer,
        nullable=False
    )

    updated_quantity = Column(
        Integer,
        nullable=False
    )

    reason = Column(
        String(255),
        nullable=False
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    performed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )