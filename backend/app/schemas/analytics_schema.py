from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel


class AnalyticsKPIResponse(BaseModel):

    total_revenue: float

    total_orders: int

    total_products_sold: int

    average_order_value: float

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

class TopSellingProductResponse(BaseModel):

    product_name: str
    quantity_sold: int

class TopCategoryResponse(BaseModel):

    category_name: str
    quantity_sold: int

class PaymentMethodResponse(BaseModel):

    payment_method: str
    total_sales: int

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

    class Config:

        from_attributes = True


class DrilldownProductResponse(BaseModel):

    id: int

    name: str

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