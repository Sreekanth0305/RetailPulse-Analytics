import csv
import io
import json
import re

from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.category import Category
from app.models.customer import Customer
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.import_history import ImportHistory
from app.models.import_error import ImportErrorRecord
from app.models.inventory import Inventory

from app.services.notification_service import (
    create_role_based_notifications
)

from app.services.data_quality_service import run_reconciliation

from app.services.audit_service import create_audit_log


# =========================================================
# Required columns
# =========================================================

REQUIRED_COLUMNS = {

    "products": {
        "Product Name",
        "SKU",
        "Category",
        "Unit Price",
        "Stock Quantity"
    },

    "customers": {
        "Name",
        "Email",
        "Phone"
    },

    "sales": {
        "Invoice Number",
        "Customer",
        "Product",
        "Quantity",
        "Unit Price",
        "Sale Date",
        "Sales Channel",
        "Payment Method"
    },

    "inventory": {
        "SKU",
        "Current Stock",
        "Reserved Stock",
        "Reorder Level"
    }
}

PROGRESS_UPDATE_INTERVAL = 10

# =========================================================
# Email validation
# =========================================================

def is_valid_email(email: str) -> bool:

    pattern = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}$"
    )

    return bool(
        re.match(pattern, email)
    )


# =========================================================
# Phone validation
# =========================================================

def is_valid_phone(phone: str) -> bool:

    digits = re.sub(
        r"\D",
        "",
        phone
    )

    return len(digits) == 10


# =========================================================
# Parse CSV
# =========================================================

async def parse_csv(
    file: UploadFile
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    content = await file.read()

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV file is empty."
        )

    try:

        text = content.decode(
            "utf-8-sig"
        )

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail="CSV file must use UTF-8 encoding."
        )

    reader = csv.DictReader(
        io.StringIO(text)
    )

    columns = reader.fieldnames or []

    rows = list(reader)

    return columns, rows


# =========================================================
# Column validation
# =========================================================

def validate_columns(
    import_type: str,
    columns: list[str]
):

    required = REQUIRED_COLUMNS.get(
        import_type
    )

    if not required:

        raise HTTPException(
            status_code=400,
            detail="Invalid import type."
        )

    uploaded = {
        column.strip()
        for column in columns
    }

    missing = required - uploaded

    if missing:

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Required columns are missing.",
                "missing_columns": list(missing)
            }
        )


# =========================================================
# Product validation
# =========================================================

def validate_product_row(
    db: Session,
    company_id: int,
    row: dict
):

    errors = []

    name = (
        row.get("Product Name")
        or ""
    ).strip()

    sku = (
        row.get("SKU")
        or ""
    ).strip()

    category_name = (
        row.get("Category")
        or ""
    ).strip()

    price = (
        row.get("Unit Price")
        or ""
    ).strip()

    stock = (
        row.get("Stock Quantity")
        or ""
    ).strip()

    if not name:

        errors.append(
            "Product Name is required."
        )

    if not sku:

        errors.append(
            "SKU is required."
        )

    if not category_name:

        errors.append(
            "Category is required."
        )

    try:

        unit_price = float(price)

        if unit_price <= 0:

            errors.append(
                "Unit Price must be greater than zero."
            )

    except ValueError:

        errors.append(
            "Unit Price must be numeric."
        )

    try:

        stock_quantity = int(stock)

        if stock_quantity < 0:

            errors.append(
                "Stock Quantity cannot be negative."
            )

    except ValueError:

        errors.append(
            "Stock Quantity must be numeric."
        )

    duplicate = False

    if sku:

        existing = (
            db.query(Product)
            .filter(
                Product.company_id == company_id,
                Product.sku == sku
            )
            .first()
        )

        if existing:

            duplicate = True

    return errors, duplicate


# =========================================================
# Customer validation
# =========================================================

def validate_customer_row(
    db: Session,
    company_id: int,
    row: dict
):

    errors = []

    name = (
        row.get("Name")
        or ""
    ).strip()

    email = (
        row.get("Email")
        or ""
    ).strip()

    phone = (
        row.get("Phone")
        or ""
    ).strip()

    if not name:

        errors.append(
            "Name is required."
        )

    if not email:

        errors.append(
            "Email is required."
        )

    elif not is_valid_email(email):

        errors.append(
            "Invalid email address."
        )

    if not phone:

        errors.append(
            "Phone is required."
        )

    elif not is_valid_phone(phone):

        errors.append(
            "Phone must contain 10 digits."
        )

    return errors

# =========================================================
# Sales validation
# =========================================================

def validate_sales_row(
    db: Session,
    company_id: int,
    row: dict
):

    errors = []

    invoice_number = (
        row.get("Invoice Number")
        or ""
    ).strip()

    customer = (
        row.get("Customer")
        or ""
    ).strip()

    product = (
        row.get("Product")
        or ""
    ).strip()

    quantity = (
        row.get("Quantity")
        or ""
    ).strip()

    unit_price = (
        row.get("Unit Price")
        or ""
    ).strip()

    sale_date = (
        row.get("Sale Date")
        or ""
    ).strip()

    sales_channel = (
        row.get("Sales Channel")
        or ""
    ).strip()

    payment_method = (
        row.get("Payment Method")
        or ""
    ).strip()

    # -------------------------
    # Required fields
    # -------------------------

    if not invoice_number:

        errors.append(
            "Invoice Number is required."
        )

    if not customer:

        errors.append(
            "Customer is required."
        )

    if not product:

        errors.append(
            "Product is required."
        )

    if not sales_channel:

        errors.append(
            "Sales Channel is required."
        )

    if not payment_method:

        errors.append(
            "Payment Method is required."
        )

    # -------------------------
    # Quantity validation
    # -------------------------

    try:

        quantity_value = int(quantity)

        if quantity_value <= 0:

            errors.append(
                "Quantity must be greater than zero."
            )

    except ValueError:

        errors.append(
            "Quantity must be numeric."
        )

    # -------------------------
    # Unit price validation
    # -------------------------

    try:

        price_value = float(unit_price)

        if price_value <= 0:

            errors.append(
                "Unit Price must be greater than zero."
            )

    except ValueError:

        errors.append(
            "Unit Price must be numeric."
        )

    # -------------------------
    # Sale date validation
    # -------------------------

    try:

        datetime.fromisoformat(
            sale_date
        )

    except ValueError:

        errors.append(
            "Invalid Sale Date."
        )

    # -------------------------
    # Customer existence
    # -------------------------

    if customer:

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.company_id == company_id,
                Customer.full_name == customer
            )
            .first()
        )

        if not existing_customer:

            errors.append(
                "Customer does not exist."
            )

    # -------------------------
    # Product existence
    # -------------------------

    if product:

        existing_product = (
            db.query(Product)
            .filter(
                Product.company_id == company_id,
                Product.name == product
            )
            .first()
        )

        if not existing_product:

            errors.append(
                "Product does not exist."
            )

        elif quantity.isdigit():

            quantity_value = int(quantity)

            if quantity_value > existing_product.stock_quantity:

                errors.append(
                    "Quantity exceeds available stock."
                )

    return errors

def validate_inventory_row(db: Session, company_id: int, row: dict):
    errors = []

    sku = (row.get("SKU") or "").strip()
    current_stock = (row.get("Current Stock") or "").strip()
    reserved_stock = (row.get("Reserved Stock") or "").strip()
    reorder_level = (row.get("Reorder Level") or "").strip()

    if not sku:
        errors.append("SKU is required.")

    current_stock_value = None
    reserved_stock_value = None
    reorder_level_value = None

    try:
        current_stock_value = int(current_stock)
        if current_stock_value < 0:
            errors.append("Current Stock cannot be negative.")
    except ValueError:
        errors.append("Current Stock must be numeric.")

    try:
        reserved_stock_value = int(reserved_stock)
        if reserved_stock_value < 0:
            errors.append("Reserved Stock cannot be negative.")
    except ValueError:
        errors.append("Reserved Stock must be numeric.")

    try:
        reorder_level_value = int(reorder_level)
        if reorder_level_value < 0:
            errors.append("Reorder Level cannot be negative.")
    except ValueError:
        errors.append("Reorder Level must be numeric.")

    if (
        current_stock_value is not None
        and reserved_stock_value is not None
        and reserved_stock_value > current_stock_value
    ):
        errors.append("Reserved Stock cannot be greater than Current Stock.")

    product = None

    if sku:
        product = (
            db.query(Product)
            .filter(
                Product.company_id == company_id,
                Product.sku == sku
            )
            .first()
        )

        if not product:
            errors.append("Product with this SKU does not exist.")

    duplicate = False

    if product:
        existing_inventory = (
            db.query(Inventory)
            .filter(
                Inventory.company_id == company_id,
                Inventory.product_id == product.id
            )
            .first()
        )

        if existing_inventory:
            duplicate = True

    return errors, duplicate

def get_duplicate_key(import_type: str, row: dict):
    if import_type == "products":
        return (row.get("SKU") or "").strip().lower()

    if import_type == "customers":
        email = (row.get("Email") or "").strip().lower()
        phone = (row.get("Phone") or "").strip()

        if email:
            return f"email:{email}"

        if phone:
            return f"phone:{phone}"

    if import_type == "sales":
        return (row.get("Invoice Number") or "").strip().lower()

    if import_type == "inventory":
        return (row.get("SKU") or "").strip().lower()

    return None

# =========================================================
# Validate import
# =========================================================

async def validate_import(
    db: Session,
    company_id: int,
    user_id: int,
    import_type: str,
    file: UploadFile
):

    columns, rows = await parse_csv(
        file
    )

    validate_columns(
        import_type,
        columns
    )

    total = len(rows)

    valid = 0

    invalid = 0

    duplicate = 0

    errors_to_store = []

    preview = rows[:10]

    for index, row in enumerate(
        rows,
        start=2
    ):

        row_errors = []

        is_duplicate = False

        if import_type == "products":

            row_errors, is_duplicate = (
                validate_product_row(
                    db,
                    company_id,
                    row
                )
            )

        elif import_type == "inventory":
            row_errors, is_duplicate = (
                validate_inventory_row(
                db,
                company_id,
                row
                )
            )


        elif import_type == "customers":

            row_errors = (
                validate_customer_row(
                    db,
                    company_id,
                    row
                )
            )
        
            if not row_errors:
        
                email = (
                    row.get("Email")
                    or ""
                ).strip()
        
                if email:
        
                    existing_customer = (
                        db.query(Customer)
                        .filter(
                            Customer.company_id == company_id,
                            Customer.email == email
                        )
                        .first()
                    )
        
                    if existing_customer:
        
                        is_duplicate = True

        elif import_type == "sales":

            row_errors = (
                validate_sales_row(
                    db,
                    company_id,
                    row
                )
            )
        
            if not row_errors:
        
                invoice_number = (
                    row.get("Invoice Number")
                    or ""
                ).strip()
        
                if invoice_number:
        
                    existing_sale = (
                        db.query(Sale)
                        .filter(
                            Sale.company_id == company_id,
                            Sale.invoice_number == invoice_number
                        )
                        .first()
                    )
        
                    if existing_sale:
        
                        is_duplicate = True

        if is_duplicate:

            duplicate += 1

            errors_to_store.append({

                "row_number": index,

                "error_type": "Duplicate",

                "error_message":
                    "Duplicate record.",
                    
                "row_data": row

            })

        elif row_errors:

            invalid += 1

            errors_to_store.append({

                "row_number": index,

                "error_type": "Validation",

                "error_message":
                    "; ".join(row_errors),

                "row_data": row

            })

        else:

            valid += 1

    history = ImportHistory(

        company_id=company_id,

        import_type=import_type,

        filename=file.filename,

        uploaded_by=user_id,

        total_records=total,

        successful_records=0,

        failed_records=invalid,

        duplicate_records=duplicate,

        status="Pending"

    )

    db.add(history)

    db.commit()

    db.refresh(history)

    for error in errors_to_store:

        db_error = ImportErrorRecord(

            import_id=history.id,

            row_number=
                error["row_number"],

            error_type=
                error["error_type"],

            error_message=
                error["error_message"],

            row_data=
                json.dumps(
                    error["row_data"]
                )

        )

        db.add(db_error)

    db.commit()

    return {

        "import_id": history.id,

        "import_type": import_type,

        "filename": file.filename,

        "total_records": total,

        "valid_records": valid,

        "invalid_records": invalid,

        "duplicate_records": duplicate,

        "columns": columns,

        "preview": preview

    }


# =========================================================
# Process Products
# =========================================================

def process_products(
    db: Session,
    company_id: int,
    rows: list[dict]
):

    successful = 0

    failed = 0

    for row in rows:

        try:

            category = (
                db.query(Category)
                .filter(
                    Category.company_id ==
                    company_id,
                    Category.name ==
                    row["Category"].strip()
                )
                .first()
            )

            if not category:

                failed += 1

                continue

            product = Product(

                company_id=company_id,

                category_id=category.id,

                name=
                    row["Product Name"].strip(),

                sku=
                    row["SKU"].strip(),

                unit_price=
                    float(row["Unit Price"]),

                cost_price=0,

                stock_quantity=
                    int(row["Stock Quantity"]),

                unit_of_measure="Unit",

                status="Active"

            )

            db.add(product)

            successful += 1

        except Exception:

            failed += 1

    return successful, failed

def update_import_progress(
    db: Session,
    history,
    successful: int,
    failed: int,
    duplicate: int
):
    history.successful_records = successful
    history.failed_records = failed
    history.duplicate_records = duplicate

    db.commit()

def is_import_cancelled(
    db: Session,
    import_id: int,
    company_id: int
) -> bool:

    history = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.id == import_id,
            ImportHistory.company_id == company_id
        )
        .first()
    )

    if not history:
        return False

    return history.status == "Cancelled"


# =========================================================
# Process Import
# =========================================================

async def process_import(
    db: Session,
    company_id: int,
    user_id: int,
    import_id: int,
    import_type: str,
    file: UploadFile
):

    history = (

        db.query(ImportHistory)

        .filter(

            ImportHistory.id ==
            import_id,

            ImportHistory.company_id ==
            company_id

        )

        .first()

    )


    if not history:

        raise HTTPException(
            status_code=404,
            detail="Import record not found."
        )


    if history.status == "Completed":

        raise HTTPException(
            status_code=400,
            detail="This import has already been processed."
        )


    try:

        history.status = "Processing"

        db.commit()

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="Import Started",
            resource_type="Import",
            resource_id=history.id,
            description=(
                f"{import_type.capitalize()} import "
                f"'{history.filename}' started."
            ),
            status="SUCCESS"
        )


        columns, rows = await parse_csv(file)


        validate_columns(
            import_type,
            columns
        )


        successful = 0

        failed = 0
        
        duplicate = 0

        processed = 0

        # =================================================
        # PRODUCTS
        # =================================================

        if import_type == "products":

            for row in rows:

                if is_import_cancelled(
                    db,
                    import_id,
                    company_id
                ):
                    break

                row_errors, is_duplicate = (
                    validate_product_row(
                        db,
                        company_id,
                        row
                    )
                )


                if is_duplicate:
                    duplicate += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                if row_errors:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue
                

                category = (

                    db.query(Category)

                    .filter(

                        Category.company_id ==
                        company_id,

                        Category.name ==
                        row["Category"].strip()

                    )

                    .first()

                )


                if not category:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                product = Product(

                    company_id=company_id,

                    category_id=category.id,

                    name=row[
                        "Product Name"
                    ].strip(),

                    sku=row[
                        "SKU"
                    ].strip(),

                    unit_price=float(
                        row["Unit Price"]
                    ),

                    cost_price=0,

                    stock_quantity=int(
                        row["Stock Quantity"]
                    ),

                    unit_of_measure="Unit",

                    status="Active"

                )


                db.add(product)

                successful += 1

                processed += 1

                if (
                    processed % PROGRESS_UPDATE_INTERVAL == 0
                    or processed == history.total_records
                ):
                    update_import_progress(
                        db,
                        history,
                        successful,
                        failed,
                        duplicate
                    )
                
        # =================================================
        # INVENTORY
        # =========================================

        elif import_type == "inventory":
            for row in rows:

                if is_import_cancelled(
                    db,
                    import_id,
                    company_id
                ):
                    break

                row_errors, is_duplicate = validate_inventory_row(
                    db,
                    company_id,
                    row
                )

                if is_duplicate:
                    duplicate += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                if row_errors:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                sku = row["SKU"].strip()

                product = (
                    db.query(Product)
                    .filter(
                        Product.company_id == company_id,
                        Product.sku == sku
                    )
                    .first()
                )

                if not product:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                current_stock = int(row["Current Stock"])
                reserved_stock = int(row["Reserved Stock"])
                reorder_level = int(row["Reorder Level"])

                available_stock = current_stock - reserved_stock

                if available_stock <= 0:
                    stock_status = "Out of Stock"
                elif available_stock <= reorder_level:
                    stock_status = "Low Stock"
                else:
                    stock_status = "In Stock"

                inventory = Inventory(
                    company_id=company_id,
                    product_id=product.id,
                    current_stock=current_stock,
                    reserved_stock=reserved_stock,
                    available_stock=available_stock,
                    reorder_level=reorder_level,
                    stock_status=stock_status
                )

                db.add(inventory)
                successful += 1
                processed += 1

                if (
                    processed % PROGRESS_UPDATE_INTERVAL == 0
                    or processed == history.total_records
                ):
                    update_import_progress(
                        db,
                        history,
                        successful,
                        failed,
                        duplicate
                    )


        # =================================================
        # CUSTOMERS
        # =================================================

        elif import_type == "customers":

            for row in rows:

                if is_import_cancelled(
                    db,
                    import_id,
                    company_id
                ):
                    break
        
                row_errors = (
                    validate_customer_row(
                        db,
                        company_id,
                        row
                    )
                )


                if row_errors:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                email = row[
                    "Email"
                ].strip()


                existing = (

                    db.query(Customer)

                    .filter(

                        Customer.company_id ==
                        company_id,

                        Customer.email ==
                        email

                    )

                    .first()

                )


                if existing:
                    duplicate += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                customer = Customer(

                    company_id=company_id,

                    customer_id=
                        f"IMP-{history.id}-{processed + 1}",

                    full_name=
                        row["Name"].strip(),

                    email=email,

                    phone=
                        row["Phone"].strip(),

                    customer_type=
                        "Imported",

                    status="Active"

                )


                db.add(customer)

                successful += 1

                processed += 1

                if (
                    processed % PROGRESS_UPDATE_INTERVAL == 0
                    or processed == history.total_records
                ):
                    update_import_progress(
                        db,
                        history,
                        successful,
                        failed,
                        duplicate
                    )


        # =================================================
        # SALES
        # =================================================

        elif import_type == "sales":

            for row in rows:

                if is_import_cancelled(
                    db,
                    import_id,
                    company_id
                ):
                    break 

                row_errors = (
                    validate_sales_row(
                        db,
                        company_id,
                        row
                    )
                )

                if row_errors:
                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                invoice_number = (
                    row["Invoice Number"]
                    .strip()
                )


                existing_sale = (

                    db.query(Sale)

                    .filter(

                        Sale.company_id ==
                        company_id,

                        Sale.invoice_number ==
                        invoice_number

                    )

                    .first()

                )


                if existing_sale:
                    duplicate += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                customer = (

                    db.query(Customer)

                    .filter(

                        Customer.company_id ==
                        company_id,

                        Customer.full_name ==
                        row["Customer"].strip()

                    )

                    .first()

                )


                if not customer:

                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                product = (

                    db.query(Product)

                    .filter(

                        Product.company_id ==
                        company_id,

                        Product.name ==
                        row["Product"].strip()

                    )

                    .first()

                )


                if not product:

                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue

                quantity = int(
                    row["Quantity"]
                )


                if quantity > product.stock_quantity:

                    failed += 1
                    processed += 1
                
                    if (
                        processed % PROGRESS_UPDATE_INTERVAL == 0
                        or processed == history.total_records
                    ):
                        update_import_progress(
                            db,
                            history,
                            successful,
                            failed,
                            duplicate
                        )
                
                    continue


                unit_price = float(
                    row["Unit Price"]
                )


                total = (
                    quantity *
                    unit_price
                )


                sale = Sale(

                    company_id=company_id,

                    invoice_number=
                        invoice_number,

                    customer_name=
                        customer.full_name,

                    sale_date=
                        datetime.fromisoformat(
                            row["Sale Date"]
                        ),

                    sales_channel=
                        row["Sales Channel"].strip(),

                    payment_method=
                        row["Payment Method"].strip(),

                    subtotal=total,

                    discount=0,

                    tax=0,

                    total_amount=total,

                    payment_status="Paid",

                    created_by=user_id

                )


                db.add(sale)

                db.flush()


                sale_item = SaleItem(

                    sale_id=sale.id,

                    product_id=product.id,

                    category_id=product.category_id,

                    quantity=quantity,

                    unit_price=unit_price,

                    discount=0,

                    tax=0,

                    total=total

                )


                db.add(sale_item)


                # Reduce stock

                product.stock_quantity -= quantity


                successful += 1

                processed += 1

                if (
                    processed % PROGRESS_UPDATE_INTERVAL == 0
                    or processed == history.total_records
                ):
                    update_import_progress(
                        db,
                        history,
                        successful,
                        failed,
                        duplicate
                    )


        # =================================================
        # CHECK IF IMPORT WAS CANCELLED
        # =================================================
        
        if is_import_cancelled(
            db,
            import_id,
            company_id
        ):
        
            history = (
                db.query(ImportHistory)
                .filter(
                    ImportHistory.id == import_id,
                    ImportHistory.company_id == company_id
                )
                .first()
            )
        
            history.status = "Cancelled"
        
            history.completed_at = datetime.utcnow()
        
            db.commit()
        
            db.refresh(history)

            create_audit_log(
                db=db,
                company_id=company_id,
                user_id=user_id,
                action="Import Cancelled",
                resource_type="Import",
                resource_id=history.id,
                description=(
                    f"{import_type.capitalize()} import "
                    f"'{history.filename}' was cancelled."
                ),
                status="SUCCESS"
            )
        
            return {
        
                "import_id":
                    history.id,
        
                "status":
                    history.status,
        
                "total_records":
                    history.total_records,
        
                "successful_records":
                    history.successful_records,
        
                "failed_records":
                    history.failed_records,
        
                "duplicate_records":
                    history.duplicate_records,
        
                "message":
                    "Import was cancelled successfully."
        
            }
        
        
        # =================================================
        # SAVE IMPORT RESULT
        # =================================================
        
        history.successful_records = successful
        
        history.failed_records = failed
        
        history.duplicate_records = duplicate
        
        history.status = (
        
            "Completed"
        
            if failed == 0 and duplicate == 0
        
            else "Completed with Errors"
        
        )
        
        history.completed_at = (
            datetime.utcnow()
        )

        db.commit()

        db.refresh(history)

        # =================================================
        # DATA QUALITY & RECONCILIATION INTEGRATION
        # =================================================
        
        try:
        
            run_reconciliation(
                db=db,
                company_id=company_id,
                user_id=user_id
            )
        
        except Exception as e:
        
            # Data quality reconciliation should not
            # make the completed import fail.
            print(
                f"Data quality reconciliation failed "
                f"after import {import_id}: {str(e)}"
            )
                
        
        # =================================================
        # CREATE IMPORT AUDIT LOG
        # =================================================
        
        if history.status == "Completed":
        
            create_audit_log(
                db=db,
                company_id=company_id,
                user_id=user_id,
                action="Import Completed",
                resource_type="Import",
                resource_id=history.id,
                description=(
                    f"{import_type.capitalize()} import "
                    f"'{history.filename}' completed successfully. "
                    f"{successful} records imported."
                ),
                status="SUCCESS"
            )
        
        elif history.status == "Completed with Errors":
        
            create_audit_log(
                db=db,
                company_id=company_id,
                user_id=user_id,
                action="Import Completed with Errors",
                resource_type="Import",
                resource_id=history.id,
                description=(
                    f"{import_type.capitalize()} import "
                    f"'{history.filename}' completed with "
                    f"{failed} failed and "
                    f"{duplicate} duplicate records."
                ),
                status="SUCCESS"
            )


# =================================================
# CREATE IMPORT NOTIFICATION
# =================================================

        # =================================================
        # CREATE IMPORT NOTIFICATION
        # =================================================
        
        if history.status == "Completed":
        
            create_role_based_notifications(
                db=db,
                company_id=company_id,
                notification_type="Import Completed",
                title="Import Completed",
                message=(
                    f"{import_type.capitalize()} import "
                    f"'{history.filename}' completed successfully. "
                    f"{successful} records imported."
                ),
                priority="Low",
                resource_type="ImportHistory",
                resource_id=history.id,
                deduplication_key=(
                    f"import:{history.id}:completed"
                ),
                expires_in_days=7
            )
        
        elif history.status == "Completed with Errors":
        
            create_role_based_notifications(
                db=db,
                company_id=company_id,
                notification_type="Import Completed",
                title="Import Completed with Errors",
                message=(
                    f"{import_type.capitalize()} import "
                    f"'{history.filename}' completed with "
                    f"{failed} failed and "
                    f"{duplicate} duplicate records."
                ),
                priority="High",
                resource_type="ImportHistory",
                resource_id=history.id,
                deduplication_key=(
                    f"import:{history.id}:completed-errors"
                ),
                expires_in_days=7
            )
        
        return {

            "import_id":
                history.id,

            "status":
                history.status,

            "total_records":
                history.total_records,

            "successful_records":
                history.successful_records,

            "failed_records":
                history.failed_records,

            "duplicate_records":
                history.duplicate_records

        }


    except HTTPException:

        db.rollback()

        history.status = "Failed"

        db.commit()

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="Import Failed",
            resource_type="Import",
            resource_id=history.id,
            description=(
                f"{import_type.capitalize()} import "
                f"'{history.filename}' failed."
            ),
            status="FAILED"
        )

        create_role_based_notifications(
            db=db,
            company_id=company_id,
            notification_type="Import Failed",
            title="Import Failed",
            message=(
                f"{import_type.capitalize()} import "
                f"'{history.filename}' failed."
            ),
            priority="Critical",
            resource_type="ImportHistory",
            resource_id=history.id,
            deduplication_key=(
                f"import:{history.id}:failed"
            ),
            expires_in_days=7
        )

        raise


    except Exception as error:

        db.rollback()

        history.status = "Failed"

        db.commit()

        create_audit_log(
            db=db,
            company_id=company_id,
            user_id=user_id,
            action="Import Failed",
            resource_type="Import",
            resource_id=history.id,
            description=(
                f"{import_type.capitalize()} import "
                f"'{history.filename}' failed due to "
                f"an unexpected processing error."
            ),
            status="FAILED"
        )

        create_role_based_notifications(
            db=db,
            company_id=company_id,
            notification_type="Import Failed",
            title="Import Failed",
            message=(
                f"{import_type.capitalize()} import "
                f"'{history.filename}' failed due to "
                f"an unexpected processing error."
            ),
            priority="Critical",
            resource_type="ImportHistory",
            resource_id=history.id,
            deduplication_key=(
                f"import:{history.id}:failed"
            ),
            expires_in_days=7
        )

        print(
            "IMPORT ERROR:",
            error
        )

        raise HTTPException(

            status_code=500,

            detail=
                "Import processing failed."

        )

async def validate_import_file(
    db: Session,
    company_id: int,
    import_type: str,
    file: UploadFile
):

    columns, rows = await parse_csv(file)

    validate_columns(
        import_type,
        columns
    )

    total = len(rows)

    valid = 0

    invalid = 0

    duplicate = 0

    errors = []

    seen_records = set()

    for index, row in enumerate(rows, start=2):
        row_errors = []
        is_duplicate = False
    
        duplicate_key = get_duplicate_key(import_type, row)
    
        if duplicate_key:
            if duplicate_key in seen_records:
                is_duplicate = True
            else:
                seen_records.add(duplicate_key)
    
        if import_type == "products":
            row_errors, database_duplicate = validate_product_row(
                db,
                company_id,
                row
            )
    
            if database_duplicate:
                is_duplicate = True
    
        elif import_type == "inventory":
            row_errors, database_duplicate = validate_inventory_row(
                db,
                company_id,
                row
            )
    
            if database_duplicate:
                is_duplicate = True
    
        elif import_type == "customers":
            row_errors = validate_customer_row(
                db,
                company_id,
                row
            )
    
            if not row_errors:
                email = (row.get("Email") or "").strip()
    
                if email:
                    existing_customer = (
                        db.query(Customer)
                        .filter(
                            Customer.company_id == company_id,
                            Customer.email == email
                        )
                        .first()
                    )
    
                    if existing_customer:
                        is_duplicate = True
    
        elif import_type == "sales":
            row_errors = validate_sales_row(
                db,
                company_id,
                row
            )
    
            if not row_errors:
                invoice_number = (
                    row.get("Invoice Number") or ""
                ).strip()
    
                if invoice_number:
                    existing_sale = (
                        db.query(Sale)
                        .filter(
                            Sale.company_id == company_id,
                            Sale.invoice_number == invoice_number
                        )
                        .first()
                    )
    
                    if existing_sale:
                        is_duplicate = True
    
        if is_duplicate:
            duplicate += 1
    
            errors.append({
                "row_number": index,
                "error_type": "Duplicate",
                "error_message": "Duplicate record found in the uploaded file or database."
            })
    
        elif row_errors:
            invalid += 1
    
            errors.append({
                "row_number": index,
                "error_type": "Validation",
                "error_message": "; ".join(row_errors)
            })
    
        else:
            valid += 1

    return {

        "import_type": import_type,

        "total_records": total,

        "valid_records": valid,

        "invalid_records": invalid,

        "duplicate_records": duplicate,

        "errors": errors,

        "can_import":
            valid > 0

    }