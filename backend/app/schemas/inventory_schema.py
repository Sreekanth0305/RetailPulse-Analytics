from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Inventory Response
# -----------------------------
class InventoryResponse(BaseModel):

    id: int

    company_id: int

    product_id: int

    product_name: str

    sku: str

    category_name: str

    brand: str

    current_stock: int

    reserved_stock: int

    available_stock: int

    reorder_level: int

    stock_status: str

    updated_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Stock Adjustment
# -----------------------------
class StockAdjustment(BaseModel):

    quantity: int

    reason: str

    remarks: str | None = None


# -----------------------------
# Update Reorder Level
# -----------------------------
class ReorderLevelUpdate(BaseModel):

    reorder_level: int