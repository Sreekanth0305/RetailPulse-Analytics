from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.employee import Employee
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale

from app.schemas.dashboard_schema import DashboardResponse


def get_dashboard_data(db: Session, company_id: int):

    # Employee Summary
    total_employees = (
        db.query(Employee)
        .filter(Employee.company_id == company_id)
        .count()
    )

    active_employees = (
        db.query(Employee)
        .filter(
            Employee.company_id == company_id,
            Employee.status == "Active"
        )
        .count()
    )

    departments = (
        db.query(Employee.department)
        .filter(Employee.company_id == company_id)
        .distinct()
        .count()
    )

    attendance = 96

    # Product Summary
    total_products = (
        db.query(Product)
        .filter(Product.company_id == company_id)
        .count()
    )

    active_products = (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.status == "Active"
        )
        .count()
    )

    inactive_products = (
        db.query(Product)
        .filter(
            Product.company_id == company_id,
            Product.status == "Inactive"
        )
        .count()
    )

    total_categories = (
        db.query(Category)
        .filter(Category.company_id == company_id)
        .count()
    )

    # -----------------------------
    # Sales Summary
    # -----------------------------
    
    total_sales = (
    
        db.query(func.sum(Sale.total_amount))
    
        .filter(
            Sale.company_id == company_id
        )
    
        .scalar()
    
    ) or 0
    
    total_orders = (
    
        db.query(Sale)
    
        .filter(
            Sale.company_id == company_id
        )
    
        .count()
    
    )
    
    average_order_value = (
    
        total_sales / total_orders
    
        if total_orders > 0
    
        else 0
    
    )

    return DashboardResponse(

    # Employee Cards
    total_employees=total_employees,
    active_employees=active_employees,
    departments=departments,
    attendance=attendance,

    # Product Cards
    total_products=total_products,
    active_products=active_products,
    inactive_products=inactive_products,
    total_categories=total_categories,

    # Sales Cards
    total_sales=total_sales,
    total_revenue=total_sales,
    total_orders=total_orders,
    average_order_value=average_order_value


    )