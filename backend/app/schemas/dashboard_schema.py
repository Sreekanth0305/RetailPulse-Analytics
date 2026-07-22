from pydantic import BaseModel

class InventoryCategoryChart(BaseModel):

    category: str

    quantity: int

class StockStatusChart(BaseModel):

    status: str

    count: int   

class DashboardResponse(BaseModel):

    # Employee Summary
    total_employees: int
    active_employees: int
    departments: int
    attendance: int

    # Product Summary
    total_products: int
    active_products: int
    inactive_products: int
    total_categories: int

    # Sales Summary
    total_sales: int
    total_revenue: float
    total_orders: int
    average_order_value: float

    # Inventory Summary
    total_inventory_quantity: int
    low_stock_products: int
    out_of_stock_products: int
    total_inventory_products: int

    # Inventory Charts
    inventory_by_category: list[InventoryCategoryChart]
    stock_status_distribution: list[StockStatusChart]

    class Config:
        from_attributes = True