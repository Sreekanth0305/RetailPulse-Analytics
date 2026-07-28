from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.customer_purchase_summary import CustomerPurchaseSummary
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product


def update_customer_purchase_summary(
    db: Session,
    company_id: int,
    customer_name: str
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.full_name == customer_name
        )
        .first()
    )

    if not customer:
        return

    sales = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id,
            Sale.customer_name == customer_name
        )
        .all()
    )

    if len(sales) == 0:
        return

    total_orders = len(sales)

    total_revenue = sum(
        sale.total_amount for sale in sales
    )

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    first_purchase = min(
        sale.sale_date for sale in sales
    )

    last_purchase = max(
        sale.sale_date for sale in sales
    )

    total_products = (
        db.query(func.sum(SaleItem.quantity))
        .join(Sale, Sale.id == SaleItem.sale_id)
        .filter(
            Sale.company_id == company_id,
            Sale.customer_name == customer_name
        )
        .scalar()
    ) or 0

    favorite_product = (
        db.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label("qty")
        )
        .join(
            SaleItem,
            Product.id == SaleItem.product_id
        )
        .join(
            Sale,
            Sale.id == SaleItem.sale_id
        )
        .filter(
            Sale.company_id == company_id,
            Sale.customer_name == customer_name
        )
        .group_by(
            Product.id,
            Product.name
        )
        .order_by(
            func.sum(SaleItem.quantity).desc()
        )
        .first()
    )

    favorite_category = (
        db.query(
            Product.category_id,
            func.sum(SaleItem.quantity).label("qty")
        )
        .join(
            SaleItem,
            Product.id == SaleItem.product_id
        )
        .join(
            Sale,
            Sale.id == SaleItem.sale_id
        )
        .filter(
            Sale.company_id == company_id,
            Sale.customer_name == customer_name
        )
        .group_by(Product.category_id)
        .order_by(
            func.sum(SaleItem.quantity).desc()
        )
        .first()
    )

    summary = (
        db.query(CustomerPurchaseSummary)
        .filter(
            CustomerPurchaseSummary.customer_id == customer.id
        )
        .first()
    )

    if not summary:

        summary = CustomerPurchaseSummary(
            customer_id=customer.id
        )

        db.add(summary)

    summary.total_orders = total_orders
    summary.total_revenue = total_revenue
    summary.total_products_purchased = total_products
    summary.average_order_value = average_order_value
    summary.purchase_frequency = total_orders
    summary.first_purchase_date = first_purchase
    summary.last_purchase_date = last_purchase

    summary.favorite_product_id = (
        favorite_product.id
        if favorite_product
        else None
    )

    summary.favorite_category_id = (
        favorite_category.category_id
        if favorite_category
        else None
    )

    db.commit()