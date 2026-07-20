from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Sale Item
# -----------------------------
class SaleItemCreate(BaseModel):

    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0
    tax: float = 0


# -----------------------------
# Create Sale
# -----------------------------
class SaleCreate(BaseModel):

    customer_name: str

    sales_channel: str

    payment_method: str

    items: list[SaleItemCreate]


# -----------------------------
# Update Sale
# -----------------------------
class SaleUpdate(BaseModel):

    customer_name: str

    sales_channel: str

    payment_method: str

    items: list[SaleItemCreate]


# -----------------------------
# Sale Response
# -----------------------------
class SaleResponse(BaseModel):

    id: int

    company_id: int

    invoice_number: str

    customer_name: str

    sale_date: datetime

    sales_channel: str

    payment_method: str

    total_amount: float

    created_by: int

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Sale List Response
# -----------------------------
class SaleListResponse(BaseModel):

    id: int

    invoice_number: str

    customer_name: str

    product_name: str

    sale_date: datetime

    sales_channel: str

    payment_method: str

    total_amount: float

    class Config:
        from_attributes = True


# -----------------------------
# Sale Details Response
# -----------------------------
class SaleItemResponse(BaseModel):

    product_id: int

    product_name: str

    category_id: int

    category_name: str

    quantity: int

    unit_price: float

    discount: float

    tax: float

    total: float

    class Config:
        from_attributes = True


class SaleDetailResponse(BaseModel):

    id: int

    invoice_number: str

    customer_name: str

    sale_date: datetime

    sales_channel: str

    payment_method: str

    total_amount: float

    items: list[SaleItemResponse]