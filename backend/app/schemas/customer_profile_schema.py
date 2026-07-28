from datetime import date
from pydantic import BaseModel


class CustomerPurchaseSummaryResponse(BaseModel):

    total_orders: int

    total_revenue: float

    average_order_value: float

    purchase_frequency: float

    favorite_product: int | None = None

    favorite_category: int | None = None

    first_purchase: date | None = None

    last_purchase: date | None = None

    class Config:

        from_attributes = True


class CustomerProfileResponse(BaseModel):

    id: int

    customer_id: str

    full_name: str

    email: str

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

    summary: CustomerPurchaseSummaryResponse

    class Config:

        from_attributes = True