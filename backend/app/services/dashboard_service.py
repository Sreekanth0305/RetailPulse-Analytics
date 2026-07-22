from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.employee import Employee
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale
from app.models.inventory import Inventory

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

# -----------------------------
# Inventory Summary
# -----------------------------

    total_inventory_products = (
    
        db.query(Inventory)
    
        .filter(
            Inventory.company_id == company_id
        )
    
        .count()
    
    )
    
    total_inventory_quantity = (
    
        db.query(
    
            func.sum(Inventory.current_stock)
    
        )
    
        .filter(
            Inventory.company_id == company_id
        )
    
        .scalar()
    
    ) or 0
    
    low_stock_products = (
    
        db.query(Inventory)
    
        .filter(
    
            Inventory.company_id == company_id,
    
            Inventory.stock_status == "Low Stock"
    
        )
    
        .count()
    
    )
    
    out_of_stock_products = (
    
        db.query(Inventory)
    
        .filter(
    
            Inventory.company_id == company_id,
    
            Inventory.stock_status == "Out Of Stock"
    
        )
    
        .count()
    
    )

# -----------------------------
# Inventory By Category Chart
# -----------------------------

    inventory_by_category = (
    
        db.query(
    
            Category.name.label("category"),
    
            func.sum(Inventory.current_stock).label("quantity")
    
        )
    
        .join(
            Product,
            Inventory.product_id == Product.id
        )
    
        .join(
            Category,
            Product.category_id == Category.id
        )
    
        .filter(
            Inventory.company_id == company_id
        )
    
        .group_by(
            Category.name
        )
    
        .all()
    
    )

# -----------------------------
# Stock Status Distribution
# -----------------------------

    stock_status_distribution = (
    
        db.query(
    
            Inventory.stock_status,
    
            func.count(Inventory.id).label("count")
    
        )
    
        .filter(
            Inventory.company_id == company_id
        )
    
        .group_by(
            Inventory.stock_status
        )
    
        .all()
    
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
    average_order_value=average_order_value,

    # Inventory Cards
    total_inventory_products=total_inventory_products,
    total_inventory_quantity=total_inventory_quantity,
    low_stock_products=low_stock_products,
    out_of_stock_products=out_of_stock_products,

    inventory_by_category=[

        {
    
            "category": row.category,
    
            "quantity": row.quantity
    
        }
    
        for row in inventory_by_category
    
    ],
    
    stock_status_distribution=[
    
        {
    
            "status": row.stock_status,
    
            "count": row.count
    
        }
    
        for row in stock_status_distribution
    
    ]
    )