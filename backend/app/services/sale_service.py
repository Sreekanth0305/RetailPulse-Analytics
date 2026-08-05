from datetime import datetime

from fastapi import HTTPException, Request

from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.customer import Customer

from app.schemas.sale_schema import (
    SaleCreate,
    SaleUpdate
)

from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification
from app.services.customer_purchase_summary_service import update_customer_purchase_summary
from app.services.customer_service import update_customer_segment
from app.services.customer_timeline_service import add_customer_activity
from app.services.forecast_service import generate_forecast

LOW_STOCK_THRESHOLD = 5

# -----------------------------
# Generate Invoice Number
# -----------------------------
def generate_invoice_number(
    db: Session,
    company_id: int
):

    year = datetime.now().year

    last_sale = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id
        )
        .order_by(Sale.id.desc())
        .first()
    )

    if not last_sale:
        return f"INV-{year}-000001"

    last_number = int(
        last_sale.invoice_number.split("-")[-1]
    )

    next_number = last_number + 1

    return f"INV-{year}-{next_number:06d}"
# -----------------------------
# Calculate Item Total
# -----------------------------
def calculate_item_total(

    quantity: int,

    unit_price: float,

    discount: float,

    tax: float

):

    subtotal = quantity * unit_price

    subtotal -= discount

    subtotal += tax

    return subtotal

# -----------------------------
# Calculate Grand Total
# -----------------------------
def calculate_sale_total(
    items
):

    total = 0

    for item in items:

        total += calculate_item_total(

            item.quantity,

            item.unit_price,

            item.discount,

            item.tax

        )

    return total

# -----------------------------
# Create Sale
# -----------------------------
def create_sale(
    db: Session,
    company_id: int,
    user_id: int,
    sale: SaleCreate,
    request: Request
):

    invoice_number = generate_invoice_number(
        db,
        company_id
    )

    grand_total = calculate_sale_total(
        sale.items
    )

    db_sale = Sale(

        company_id=company_id,

        invoice_number=invoice_number,

        customer_name=sale.customer_name,

        sales_channel=sale.sales_channel,

        payment_method=sale.payment_method,

        total_amount=grand_total,

        created_by=user_id

    )

    db.add(db_sale)

    db.flush()

    print("Generated Invoice:", invoice_number)
    print("Sale ID:", db_sale.id)

    # -----------------------------
    # Save Sale Items
    # -----------------------------

    for item in sale.items:

        product = (

            db.query(Product)

            .filter(

                Product.id == item.product_id,

                Product.company_id == company_id

            )

            .first()

        )

        if not product:

            raise HTTPException(

                status_code=404,

                detail="Product not found."

            )
        
        if item.quantity <= 0:

            raise HTTPException(
    
                status_code=400,
    
                detail="Quantity must be greater than zero."
    
            )
            
        if item.quantity > product.stock_quantity:

            raise HTTPException(
        
                status_code=400,
        
                detail=f"Insufficient stock for {product.name}."
        
            )
        
        if item.unit_price < 0:

            raise HTTPException(

                status_code=400,

                detail="Unit price cannot be negative."

            )

        if item.discount < 0:

            raise HTTPException(

                status_code=400,

                detail="Discount cannot be negative."

            )

        if item.tax < 0:

            raise HTTPException(

                status_code=400,

                detail="Tax cannot be negative."

            )
        
        if item.discount > (item.quantity * item.unit_price):

            raise HTTPException(

                status_code=400,

                detail="Discount cannot exceed product value."

            )
        
        total = calculate_item_total(

            item.quantity,

            item.unit_price,

            item.discount,

            item.tax

        )

        db_item = SaleItem(

            sale_id=db_sale.id,

            product_id=product.id,

            category_id=product.category_id,

            quantity=item.quantity,

            unit_price=item.unit_price,

            discount=item.discount,

            tax=item.tax,

            total=total

        )

        print("Adding Item:", db_item.product_id)

        db.add(db_item)

        print("Item Added")

        product.stock_quantity -= item.quantity

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.company_id == company_id,
                Inventory.product_id == product.id
            )
            .first()
        )
        
        if inventory:
            inventory.current_stock = product.stock_quantity
            inventory.available_stock = (
                inventory.current_stock -
                inventory.reserved_stock
            )
        
            inventory.stock_status = (
                "Out Of Stock"
                if inventory.available_stock == 0
                else (
                    "Low Stock"
                    if inventory.available_stock <= inventory.reorder_level
                    else "In Stock"
                )
            )
        
        # Low Stock Notification
        if product.stock_quantity <= LOW_STOCK_THRESHOLD and product.stock_quantity > 0:
        
            create_notification(
        
                db=db,
        
                company_id=company_id,
        
                title="Low Stock",
        
                message=f"{product.name} stock is low. Remaining quantity: {product.stock_quantity}"
        
            )

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="Inventory Updated",
            entity_name=product.name,
            ip_address=request.client.host,
            browser=request.headers.get("user-agent")
        )
        
        # Out Of Stock Notification
        if product.stock_quantity == 0:
        
            product.status = "Out Of Stock"
        
            create_notification(
        
                db=db,
        
                company_id=company_id,
        
                title="Out Of Stock",
        
                message=f"{product.name} is now Out Of Stock."
        
            )

            create_audit_log(
                db=db,
                company_id=company_id,
                user_id=user_id,
                action="Product Marked Out of Stock",
                entity_name=product.name,
                ip_address=request.client.host,
                browser=request.headers.get("user-agent")
            )


    print("Saving Sale:", db_sale.invoice_number)
    db.commit()
    db.refresh(db_sale)

# -----------------------------
# Auto Refresh Forecast
# -----------------------------
    generate_forecast(
        db=db,
        company_id=company_id,
        user_id=user_id,
        forecast_period="Next 30 days",
        request=request
    )

    update_customer_purchase_summary(

        db=db,
    
        company_id=company_id,
    
        customer_name=db_sale.customer_name
    
    )

    customer = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.full_name == sale.customer_name
        )
        .first()
    )
    
    if customer:
    
        previous_sales = (
            db.query(Sale)
            .filter(
                Sale.company_id == company_id,
                Sale.customer_name == sale.customer_name
            )
            .count()
        )
    
        if previous_sales == 1:
    
            add_customer_activity(
                db=db,
                company_id=company_id,
                customer_id=customer.id,
                activity="First Purchase",
                description=f"Invoice {invoice_number}"
            )
    
        if grand_total >= 10000:
    
            add_customer_activity(
                db=db,
                company_id=company_id,
                customer_id=customer.id,
                activity="Large Purchase Completed",
                description=f"Purchase Amount ₹{grand_total}"
            )
    
        update_customer_segment(
            db=db,
            customer_name=sale.customer_name,
            company_id=company_id
        )

    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Sale Created",
        entity_name=invoice_number,
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return db_sale
        
# -----------------------------
# Get All Sales
# -----------------------------
def get_sales(
    db: Session,
    company_id: int
):

    sales = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id
        )
        .order_by(
            Sale.sale_date.desc()
        )
        .all()
    )

    result = []

    for sale in sales:

        items = (
            db.query(Product.name)
            .join(
                SaleItem,
                Product.id == SaleItem.product_id
            )
            .filter(
                SaleItem.sale_id == sale.id
            )
            .all()
        )

        product_names = ", ".join(
            [item.name for item in items]
        )

        result.append({
            "id": sale.id,
            "invoice_number": sale.invoice_number,
            "customer_name": sale.customer_name,
            "product_name": product_names,
            "sale_date": sale.sale_date,
            "sales_channel": sale.sales_channel,
            "payment_method": sale.payment_method,
            "total_amount": sale.total_amount
        })

    return result

# -----------------------------
# Get Sale By ID
# -----------------------------
def get_sale(
    db: Session,
    company_id: int,
    sale_id: int
):

    sale = (

        db.query(Sale)

        .filter(

            Sale.company_id == company_id,

            Sale.id == sale_id

        )

        .first()

    )

    if not sale:

        raise HTTPException(

            status_code=404,

            detail="Sale not found."

        )

    return sale       

# -----------------------------
# Sale Details
# -----------------------------
def get_sale_details(
    db: Session,
    company_id: int,
    sale_id: int
):

    sale = get_sale(
        db,
        company_id,
        sale_id
    )

    items = (

        db.query(

            SaleItem,

            Product.name,

            Category.name

        )

        .join(

            Product,

            SaleItem.product_id == Product.id

        )

        .join(

            Category,

            SaleItem.category_id == Category.id

        )

        .filter(

            SaleItem.sale_id == sale.id

        )

        .all()

    )

    result = []

    for item, product_name, category_name in items:

        result.append({

            "product_id": item.product_id,

            "product_name": product_name,

            "category_id": item.category_id,

            "category_name": category_name,

            "quantity": item.quantity,

            "unit_price": item.unit_price,

            "discount": item.discount,

            "tax": item.tax,

            "total": item.total

        })

    return {

        "id": sale.id,

        "invoice_number": sale.invoice_number,

        "customer_name": sale.customer_name,

        "sale_date": sale.sale_date,

        "sales_channel": sale.sales_channel,

        "payment_method": sale.payment_method,

        "total_amount": sale.total_amount,

        "items": result

    }

# -----------------------------
# Update Sale
# -----------------------------
def update_sale(
    db: Session,
    company_id: int,
    user_id: int,
    sale_id: int,
    data: SaleUpdate,
    request: Request
):

    sale = get_sale(
        db,
        company_id,
        sale_id
    )

    # Restore previous stock
    old_items = (
        db.query(SaleItem)
        .filter(SaleItem.sale_id == sale.id)
        .all()
    )

    for item in old_items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if product:

            product.stock_quantity += item.quantity

            if product.status == "Out of Stock":
                product.status = "Active"

    # Remove old sale items
    (
        db.query(SaleItem)
        .filter(SaleItem.sale_id == sale.id)
        .delete()
    )

    grand_total = calculate_sale_total(data.items)

    sale.customer_name = data.customer_name

    sale.sales_channel = data.sales_channel

    sale.payment_method = data.payment_method

    sale.total_amount = grand_total

    for item in data.items:

        product = (

            db.query(Product)

            .filter(

                Product.id == item.product_id,

                Product.company_id == company_id

            )

            .first()

        )

        if not product:

            raise HTTPException(

                status_code=404,

                detail="Product not found."

            )
        
        if item.quantity > product.stock_quantity:

            raise HTTPException(

                status_code=400,

                detail=f"Insufficient stock for {product.name}"

            )

        total = calculate_item_total(

            item.quantity,

            item.unit_price,

            item.discount,

            item.tax

        )

        db_item = SaleItem(

            sale_id=sale.id,

            product_id=product.id,

            category_id=product.category_id,

            quantity=item.quantity,

            unit_price=item.unit_price,

            discount=item.discount,

            tax=item.tax,

            total=total

        )

        db.add(db_item)

        product.stock_quantity -= item.quantity

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.company_id == company_id,
                Inventory.product_id == product.id
            )
            .first()
        )
        
        if inventory:
            inventory.current_stock = product.stock_quantity
            inventory.available_stock = (
                inventory.current_stock -
                inventory.reserved_stock
            )
        
            inventory.stock_status = (
                "Out Of Stock"
                if inventory.available_stock == 0
                else (
                    "Low Stock"
                    if inventory.available_stock <= inventory.reorder_level
                    else "In Stock"
                )
            )

        # Low Stock Notification
        if product.stock_quantity <= LOW_STOCK_THRESHOLD and product.stock_quantity > 0:
        
            create_notification(
        
                db=db,
        
                company_id=company_id,
        
                title="Low Stock",
        
                message=f"{product.name} stock is low. Remaining quantity: {product.stock_quantity}"
        
            )

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="Inventory Updated",
            entity_name=product.name,
            ip_address=request.client.host,
            browser=request.headers.get("user-agent")
        )
        
        # Out Of Stock Notification
        if product.stock_quantity == 0:
        
            product.status = "Out Of Stock"
        
            create_notification(
        
                db=db,
        
                company_id=company_id,
        
                title="Out Of Stock",
        
                message=f"{product.name} is now Out Of Stock."
        
            )

            create_audit_log(
                db=db,
                company_id=company_id,
                user_id=user_id,
                action="Product Marked Out of Stock",
                entity_name=product.name,
                ip_address=request.client.host,
                browser=request.headers.get("user-agent")
            )
    db.commit()
    db.refresh(sale)

    generate_forecast(
        db=db,
        company_id=company_id,
        user_id=user_id,
        forecast_period="Next 30 days",
        request=request
    )
    update_customer_purchase_summary(

        db=db,
    
        company_id=company_id,
    
        customer_name=sale.customer_name
    
    )

    customer = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.full_name == sale.customer_name
        )
        .first()
    )
    
    if customer:
        update_customer_segment(
            db=db,
            customer_name=customer.full_name,
            company_id=company_id
        )

    create_audit_log(

        db=db,

        company_id=company_id,

        user_id=user_id,

        action="Sale Updated",

        entity_name=sale.invoice_number,

        ip_address=request.client.host,

        browser=request.headers.get("user-agent")

    )

    return sale

# -----------------------------
# Delete Sale
# -----------------------------
def delete_sale(
    db: Session,
    company_id: int,
    user_id: int,
    sale_id: int,
    request: Request
):

    sale = get_sale(
        db,
        company_id,
        sale_id
    )

    customer_name = sale.customer_name

    items = (

        db.query(SaleItem)

        .filter(

            SaleItem.sale_id == sale.id

        )

        .all()

    )

    for item in items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )
    
        if product:
            product.stock_quantity += item.quantity
    
            if product.status == "Out of Stock":
                product.status = "Active"

            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.company_id == company_id,
                    Inventory.product_id == product.id
                )
                .first()
            )
            
            if inventory:
                inventory.current_stock = product.stock_quantity
            
                inventory.available_stock = (
                    inventory.current_stock -
                    inventory.reserved_stock
                )
            
                inventory.stock_status = (
                    "Out Of Stock"
                    if inventory.available_stock == 0
                    else (
                        "Low Stock"
                        if inventory.available_stock <= inventory.reorder_level
                        else "In Stock"
                    )
                )
    
    db.query(SaleItem).filter(
        SaleItem.sale_id == sale.id
    ).delete()
    
    invoice = sale.invoice_number
    
    db.delete(sale)
    
    db.commit()

    generate_forecast(
        db=db,
        company_id=company_id,
        user_id=user_id,
        forecast_period="Next 30 days",
        request=request
    )
    update_customer_purchase_summary(

        db=db,
    
        company_id=company_id,
    
        customer_name=customer_name
    
    )

    customer = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.full_name == customer_name
        )
        .first()
    )
    
    if customer:
        update_customer_segment(
            db=db,
            customer_name=customer.full_name,
            company_id=company_id
        )
    
    create_audit_log(
        db=db,
        company_id=company_id,
        user_id=user_id,
        action="Sale Deleted",
        entity_name=invoice,
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )
    
    return {
        "message": "Sale deleted successfully."
    }

# -----------------------------
# Search Sales
# -----------------------------
def search_sales(
    db: Session,
    company_id: int,
    keyword: str
):

    sales = (

        db.query(Sale)

        .join(
            SaleItem,
            Sale.id == SaleItem.sale_id
        )

        .join(
            Product,
            SaleItem.product_id == Product.id
        )

        .filter(

            Sale.company_id == company_id,

            (

                Sale.invoice_number.ilike(f"%{keyword}%")

                |

                Sale.customer_name.ilike(f"%{keyword}%")

                |

                Product.name.ilike(f"%{keyword}%")

            )

        )

        .distinct()

        .order_by(
            Sale.sale_date.desc()
        )

        .all()

    )

    return sales

# -----------------------------
# Filter Sales
# -----------------------------
def filter_sales(
    db: Session,
    company_id: int,
    start_date: str | None = None,
    end_date: str | None = None,
    category_id: int | None = None,
    sales_channel: str | None = None,
    payment_method: str | None = None
):

    query = (

        db.query(Sale)

        .filter(
            Sale.company_id == company_id
        )

    )

    # -----------------------------
    # Date Range
    # -----------------------------
    if start_date:

        query = query.filter(
            func.date(Sale.sale_date) >= start_date
        )

    if end_date:

        query = query.filter(
            func.date(Sale.sale_date) <= end_date
        )

    # -----------------------------
    # Sales Channel
    # -----------------------------
    if sales_channel:

        query = query.filter(
            Sale.sales_channel == sales_channel
        )

    # -----------------------------
    # Payment Method
    # -----------------------------
    if payment_method:

        query = query.filter(
            Sale.payment_method == payment_method
        )

    # -----------------------------
    # Category Filter
    # -----------------------------
    if category_id:

        query = (

            query.join(
                SaleItem,
                Sale.id == SaleItem.sale_id
            )

            .filter(
                SaleItem.category_id == category_id
            )

            .distinct()

        )

    return query.order_by(
        Sale.sale_date.desc()
    ).all()

# -----------------------------
# Sort Sales
# -----------------------------
def sort_sales(
    db: Session,
    company_id: int,
    sort_by: str
):

    query = (

        db.query(Sale)

        .filter(
            Sale.company_id == company_id
        )

    )

    if sort_by == "date":

        query = query.order_by(
            Sale.sale_date.desc()
        )

    elif sort_by == "invoice":

        query = query.order_by(
            Sale.invoice_number.asc()
        )

    elif sort_by == "amount":

        query = query.order_by(
            Sale.total_amount.desc()
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid sort option."
        )

    return query.all()

# -----------------------------
# Customer Purchase History
# -----------------------------
def get_customer_purchase_history(
    db: Session,
    company_id: int,
    customer_name: str
):

    sales = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id,
            Sale.customer_name == customer_name
        )
        .order_by(Sale.sale_date.desc())
        .all()
    )

    return sales