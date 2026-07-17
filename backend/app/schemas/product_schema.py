from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Create Product
# -----------------------------
class ProductCreate(BaseModel):

    category_id: int
    name: str
    sku: str
    brand: str
    description: str
    unit_price: float
    cost_price: float
    stock_quantity: int
    unit_of_measure: str
    status: str = "Active"


# -----------------------------
# Update Product
# -----------------------------
class ProductUpdate(BaseModel):

    category_id: int
    name: str
    sku: str
    brand: str
    description: str
    unit_price: float
    cost_price: float
    stock_quantity: int
    unit_of_measure: str
    status: str


# -----------------------------
# Product Response
# -----------------------------
class ProductResponse(BaseModel):

    id: int
    company_id: int
    category_id: int
    name: str
    sku: str
    brand: str
    description: str
    unit_price: float
    cost_price: float
    stock_quantity: int
    unit_of_measure: str
    status: str
    created_at: datetime
    updated_at: datetime

class ProductListResponse(BaseModel):

    id: int
    company_id: int
    category_id: int
    category_name: str

    name: str
    sku: str
    brand: str
    description: str

    unit_price: float
    cost_price: float
    stock_quantity: int
    unit_of_measure: str

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True