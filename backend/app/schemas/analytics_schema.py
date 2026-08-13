from pydantic import BaseModel
from datetime import datetime


class AnalyticsKPIResponse(BaseModel):

    total_revenue: float

    total_orders: int

    total_products_sold: int

    average_order_value: float

    total_discount: float

    total_tax: float

    total_inventory_value: float

    low_stock_products: int

    out_of_stock_products: int

    total_categories: int

class RevenueTrendResponse(BaseModel):
    period: str
    revenue: float

class SalesTrendResponse(BaseModel):

    period: str
    orders: int
    revenue: float

class TopSellingProductResponse(BaseModel):

    product_name: str
    quantity_sold: int
    revenue: float

class TopCategoryResponse(BaseModel):

    category_name: str
    quantity_sold: int

class PaymentMethodResponse(BaseModel):

    payment_method: str
    total_sales: int
    revenue: float

class SalesChannelResponse(BaseModel):

    sales_channel: str
    total_sales: int

class InventoryDistributionResponse(BaseModel):

    category_name: str
    current_stock: int

class StockStatusSummaryResponse(BaseModel):

    stock_status: str
    total_products: int

class LowStockProductResponse(BaseModel):

    product_name: str
    current_stock: int
    reorder_level: int

class OutOfStockProductResponse(BaseModel):

    product_name: str
    current_stock: int

class InventoryValueCategoryResponse(BaseModel):

    category_name: str
    inventory_value: float

    class Config:
        from_attributes = True

class DrilldownCategoryResponse(BaseModel):

    id: int

    name: str

    total_products: int

    class Config:

        from_attributes = True


class DrilldownProductResponse(BaseModel):

    id: int

    name: str

    total_sold: int

    class Config:

        from_attributes = True


class DrilldownSaleResponse(BaseModel):

    invoice_number: str

    customer_name: str

    sale_date: datetime

    total_amount: float

    quantity: int

    payment_method: str

    sales_channel: str

    class Config:

        from_attributes = True

class TopCustomerResponse(BaseModel):
    customer_name: str
    total_orders: int
    total_spend: float
    average_order_value: float