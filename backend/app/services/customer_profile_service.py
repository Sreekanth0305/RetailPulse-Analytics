from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_purchase_summary import CustomerPurchaseSummary


def get_customer_profile(

    db: Session,

    company_id: int,

    customer_id: int

):

    customer = (

        db.query(Customer)

        .filter(

            Customer.id == customer_id,

            Customer.company_id == company_id

        )

        .first()

    )

    if not customer:

        raise HTTPException(

            status_code=404,

            detail="Customer not found."

        )

    summary = (

        db.query(CustomerPurchaseSummary)

        .filter(

            CustomerPurchaseSummary.customer_id == customer.id

        )

        .first()

    )

    if not summary:

        raise HTTPException(

            status_code=404,

            detail="Purchase summary not found."

        )

    return {

        "id": customer.id,

        "customer_id": customer.customer_id,

        "full_name": customer.full_name,

        "email": customer.email,

        "phone": customer.phone,

        "date_of_birth": customer.date_of_birth,

        "gender": customer.gender,

        "address": customer.address,

        "city": customer.city,

        "state": customer.state,

        "country": customer.country,

        "customer_type": customer.customer_type,

        "preferred_sales_channel": customer.preferred_sales_channel,

        "status": customer.status,

        "summary": {

            "total_orders": summary.total_orders,

            "total_revenue":  summary.total_revenue,

            "total_products_purchased": summary.total_products_purchased,

            "average_order_value": summary.average_order_value,

            "purchase_frequency": summary.purchase_frequency,

            "favorite_product": summary.favorite_product_id,

            "favorite_category": summary.favorite_category_id,

            "first_purchase":
                summary.first_purchase_date.date()
                if summary.first_purchase_date else None,
        
            "last_purchase":
                summary.last_purchase_date.date()
                if summary.last_purchase_date else None


        }

    }