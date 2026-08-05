from pydantic import BaseModel, EmailStr
from datetime import date, datetime


# -----------------------------
# Create Customer
# -----------------------------
class CustomerCreate(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    date_of_birth: date | None = None

    gender: str | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    customer_type: str

    preferred_sales_channel: str | None = None


# -----------------------------
# Update Customer
# -----------------------------
class CustomerUpdate(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    date_of_birth: date | None = None

    gender: str | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    customer_type: str

    preferred_sales_channel: str | None = None

    status: str

class CustomerPurchaseSummaryShort(BaseModel):

    total_orders: int = 0

    total_revenue: float = 0

    class Config:

        from_attributes = True


# -----------------------------
# Customer Response
# -----------------------------
class CustomerResponse(BaseModel):

    id: int

    customer_id: str

    full_name: str

    email: str

    phone: str

    date_of_birth: date | None

    gender: str | None

    address: str | None

    city: str | None

    state: str | None

    country: str |None

    customer_type: str

    preferred_sales_channel: str | None

    status: str

    segment: str

    created_at: datetime

    updated_at: datetime

    purchase_summary: CustomerPurchaseSummaryShort | None = None

    class Config:

        from_attributes = True