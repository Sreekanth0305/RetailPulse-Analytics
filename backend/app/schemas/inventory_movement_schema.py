from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Inventory Movement Response
# -----------------------------
class InventoryMovementResponse(BaseModel):

    id: int

    product_name: str

    movement_type: str

    previous_quantity: int

    updated_quantity: int

    quantity_changed: int

    reason: str

    remarks: str | None = None

    performed_by: int

    created_at: datetime

    class Config:
        from_attributes = True