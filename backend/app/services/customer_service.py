from sqlalchemy.orm import Session
from fastapi import Request
from sqlalchemy import func, or_

from fastapi import HTTPException

from datetime import datetime
from app.models.customer_purchase_summary import CustomerPurchaseSummary

from app.models.customer import Customer
from app.models.sale import Sale

from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate
)

from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification
from app.services.customer_timeline_service import add_customer_activity

def generate_customer_id(db: Session):

    last_customer = (
        db.query(Customer)
        .order_by(Customer.id.desc())
        .first()
    )

    if not last_customer:

        return "CUS0001"

    last_number = int(
        last_customer.customer_id.replace("CUS", "")
    )

    return f"CUS{last_number + 1:04d}"

def create_customer(

    db: Session,

    company_id: int,

    user_id: int,

    customer: CustomerCreate,

    request: Request

):

    email_exists = (
        db.query(Customer)
        .filter(

            Customer.company_id == company_id,

            Customer.email == customer.email

        )
        .first()
    )

    if email_exists:

        raise HTTPException(

            status_code=400,

            detail="Email already exists."

        )

    phone_exists = (
        db.query(Customer)
        .filter(

            Customer.company_id == company_id,

            Customer.phone == customer.phone

        )
        .first()
    )

    if phone_exists:

        raise HTTPException(

            status_code=400,

            detail="Phone number already exists."

        )

    new_customer = Customer(

        company_id=company_id,

        customer_id=generate_customer_id(db),

        full_name=customer.full_name,

        email=customer.email,

        phone=customer.phone,

        date_of_birth=customer.date_of_birth,

        gender=customer.gender,

        address=customer.address,

        city=customer.city,

        state=customer.state,

        country=customer.country,

        customer_type=customer.customer_type,

        preferred_sales_channel=customer.preferred_sales_channel,

        status="Active"

    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    add_customer_activity(

        db=db,
    
        company_id=company_id,
    
        customer_id=new_customer.id,
    
        activity="Customer Registered",
    
        description=f"{new_customer.full_name} registered."
    
    )

    create_notification(

        db=db,

        company_id=company_id,

        title="New Customer Registered",

        message=f"{new_customer.full_name} has been registered.",

    )

    ip_address = request.client.host
    
    browser = request.headers.get("user-agent")
    

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Customer Created",

        entity_name=new_customer.full_name,

        ip_address=ip_address,

        browser=browser

    )

    return new_customer

def get_customers(

    db: Session,

    company_id: int,

    search: str = None,

    customer_type: str = None,

    status: str = None,

    city: str = None,

    state: str = None,

    country: str = None,

    registration_date = None,

    sort_by: str = None

):

    query = (
        db.query(Customer)
        .outerjoin(
            CustomerPurchaseSummary,
            Customer.id == CustomerPurchaseSummary.customer_id
        )
        .filter(
            Customer.company_id == company_id
        )
    )

    # -----------------------------
    # Search
    # -----------------------------
    if search:

        query = query.filter(

            or_(

                Customer.full_name.ilike(f"%{search}%"),

                Customer.customer_id.ilike(f"%{search}%"),

                Customer.email.ilike(f"%{search}%"),

                Customer.phone.ilike(f"%{search}%")

            )

        )

    # -----------------------------
    # Filters
    # -----------------------------

    if customer_type:

        query = query.filter(
            Customer.customer_type == customer_type
        )

    if status:

        query = query.filter(
            Customer.status == status
        )

    if city:

        query = query.filter(
            Customer.city == city
        )

    if state:

        query = query.filter(
            Customer.state == state
        )

    if country:

        query = query.filter(
            Customer.country == country
        )

    if registration_date:

        query = query.filter(
            func.date(Customer.created_at) == registration_date
        )

    # -----------------------------
    # Sorting
    # -----------------------------

    if sort_by == "name":

        query = query.order_by(
            Customer.full_name.asc()
        )

    elif sort_by == "customer_since":

        query = query.order_by(
            Customer.created_at.asc()
        )

    elif sort_by == "total_spend":

        query = query.order_by(
            CustomerPurchaseSummary.total_revenue.desc()
        )

    elif sort_by == "total_orders":

        query = query.order_by(
            CustomerPurchaseSummary.total_orders.desc()
        )

    elif sort_by == "last_purchase":

        query = query.order_by(
            CustomerPurchaseSummary.last_purchase_date.desc()
        )

    else:

        query = query.order_by(
            Customer.created_at.desc()
        )

    return query.all()


def get_customer_by_id(

    db: Session,

    company_id: int,

    customer_id: int

):

    customer = (

        db.query(Customer)

        .filter(

            Customer.company_id == company_id,

            Customer.id == customer_id

        )

        .first()

    )

    if not customer:

        raise HTTPException(

            status_code=404,

            detail="Customer not found."

        )

    return customer

def update_customer(

    db: Session,

    company_id: int,

    user_id: int,

    customer_id: int,

    customer_data: CustomerUpdate,

    request: Request

):

    customer = get_customer_by_id(

        db,

        company_id,

        customer_id

    )

    email_exists = (

        db.query(Customer)

        .filter(

            Customer.company_id == company_id,

            Customer.email == customer_data.email,

            Customer.id != customer_id

        )

        .first()

    )

    if email_exists:

        raise HTTPException(

            status_code=400,

            detail="Email already exists."

        )

    phone_exists = (

        db.query(Customer)

        .filter(

            Customer.company_id == company_id,

            Customer.phone == customer_data.phone,

            Customer.id != customer_id

        )

        .first()

    )

    if phone_exists:

        raise HTTPException(

            status_code=400,

            detail="Phone number already exists."

        )

    customer.full_name = customer_data.full_name

    customer.email = customer_data.email

    customer.phone = customer_data.phone

    customer.date_of_birth = customer_data.date_of_birth

    customer.gender = customer_data.gender

    customer.address = customer_data.address

    customer.city = customer_data.city

    customer.state = customer_data.state

    customer.country = customer_data.country

    customer.customer_type = customer_data.customer_type

    customer.preferred_sales_channel = customer_data.preferred_sales_channel

    customer.status = customer_data.status

    db.commit()

    db.refresh(customer)

    add_customer_activity(

        db=db,
    
        company_id=company_id,
    
        customer_id=customer.id,
    
        activity="Profile Updated",
    
        description="Customer profile updated."
    
    )
    
    ip_address = request.client.host

    browser = request.headers.get("user-agent")

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Customer Updated",

        entity_name=customer.full_name,

        ip_address=ip_address,

        browser=browser


    )

    return customer

def delete_customer(

    db: Session,

    company_id: int,

    user_id: int,

    customer_id: int,

    request: Request

):

    customer = get_customer_by_id(

        db,

        company_id,

        customer_id,

    )

    ip_address = request.client.host

    browser = request.headers.get("user-agent")

    add_customer_activity(

        db=db,
    
        company_id=company_id,
    
        customer_id=customer.id,
    
        activity="Customer Deleted",
    
        description="Customer account deleted."
    
    )


    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Customer Deleted",

        entity_name=customer.full_name,

        ip_address=ip_address,

        browser=browser

    )

    db.delete(customer)

    db.commit()

    return {

        "message": "Customer deleted successfully."

    }

def change_customer_status(

    db: Session,

    company_id: int,

    user_id: int,

    customer_id: int,

    status: str,

    request: Request

):

    customer = get_customer_by_id(

        db,

        company_id,

        customer_id

    )

    ip_address = request.client.host
    
    browser = request.headers.get("user-agent")

    customer.status = status

    db.commit()
    
    db.refresh(customer)
    
    activity = (
        "Customer Reactivated"
        if status == "Active"
        else
        "Customer Deactivated"
    )
    
    add_customer_activity(
    
        db=db,
    
        company_id=company_id,
    
        customer_id=customer.id,
    
        activity=activity,
    
        description=f"Customer status changed to {status}"
    
    )

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action=f"Customer {status}",

        entity_name=customer.full_name,

        ip_address=ip_address,

        browser=browser


    )

    return customer


def get_customer_analytics(db: Session, company_id: int):

    total_customers = db.query(Customer).filter(
        Customer.company_id == company_id
    ).count()

    active_customers = db.query(Customer).filter(
        Customer.company_id == company_id,
        Customer.status == "Active"
    ).count()

    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    new_customers = db.query(Customer).filter(
        Customer.company_id == company_id,
        func.extract("month", Customer.created_at) == current_month,
        func.extract("year", Customer.created_at) == current_year
    ).count()

    returning_customers = db.query(CustomerPurchaseSummary).filter(
        CustomerPurchaseSummary.total_orders > 1
    ).count()

    total_revenue = db.query(
        func.coalesce(
            func.sum(CustomerPurchaseSummary.total_revenue),
            0
        )
    ).scalar()

    average_spend = db.query(
        func.coalesce(
            func.avg(CustomerPurchaseSummary.total_revenue),
            0
        )
    ).scalar()

    purchase_frequency = db.query(
        func.coalesce(
            func.avg(CustomerPurchaseSummary.purchase_frequency),
            0
        )
    ).scalar()

    top_customers = (
        db.query(
            Customer.full_name,
            CustomerPurchaseSummary.total_orders,
            CustomerPurchaseSummary.total_revenue
        )
        .join(
            CustomerPurchaseSummary,
            Customer.id ==
            CustomerPurchaseSummary.customer_id
        )
        .filter(
            Customer.company_id == company_id
        )
        .order_by(
            CustomerPurchaseSummary.total_revenue.desc()
        )
        .limit(10)
        .all()
    )

    customer_types = (
        db.query(
            Customer.customer_type,
            func.sum(CustomerPurchaseSummary.total_revenue).label("revenue")
        )
        .join(
            CustomerPurchaseSummary,
            Customer.id == CustomerPurchaseSummary.customer_id
        )
        .filter(
            Customer.company_id == company_id
        )
        .group_by(
            Customer.customer_type
        )
        .all()
    )

    customer_growth = (
        db.query(
            func.date_format(Customer.created_at, "%Y-%m").label("month"),
            func.count(Customer.id).label("customers")
        )
        .filter(
            Customer.company_id == company_id
        )
        .group_by(
            func.date_format(Customer.created_at, "%Y-%m")
        )
        .order_by(
            func.date_format(Customer.created_at, "%Y-%m")
        )
        .all()
    )
    
    return {

        "total_customers": total_customers,

        "active_customers": active_customers,

        "new_customers": new_customers,

        "returning_customers": returning_customers,

        "average_customer_spend": average_spend,

        "total_revenue": total_revenue,

        "purchase_frequency": purchase_frequency,

         "top_customers": [
            {
                "full_name": row.full_name,
                "total_orders": row.total_orders,
                "total_revenue": float(row.total_revenue)
            }
            for row in top_customers
        ],
    
        "customer_types": [
            {
                "customer_type": row.customer_type,
                "count": row[1]
            }
            for row in customer_types
        ],

        "customer_growth": [
            {
                "month": row.month,
                "customers": row.customers
            }
            for row in customer_growth
        ],
    
    }


def update_customer_segment(
    db: Session,
    customer_name: str,
    company_id: int
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.full_name == customer_name,
            Customer.company_id == company_id
        )
        .first()
    )

    if not customer:
        return

    summary = (
        db.query(
            func.count(Sale.id).label("orders"),
            func.coalesce(func.sum(Sale.total_amount), 0).label("revenue")
        )
        .filter(
            Sale.customer_name == customer_name,
            Sale.company_id == company_id
        )
        .first()
    )

    total_orders = summary.orders or 0
    total_revenue = float(summary.revenue or 0)

    if total_orders == 0:
        segment = "New Customer"

    elif total_orders <= 5:
        segment = "Regular Customer"

    elif total_orders <= 10:
        segment = "Loyal Customer"

    else:
        segment = "VIP Customer"

    customer.segment = segment

    db.commit()