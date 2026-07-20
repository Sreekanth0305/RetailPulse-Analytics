from pydantic import BaseModel


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