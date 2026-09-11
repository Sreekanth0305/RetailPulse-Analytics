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

from app.services.notification_service import (
    create_role_based_notifications
)


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
    }
}


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


        columns, rows = await parse_csv(file)


        validate_columns(
            import_type,
            columns
        )


        successful = 0

        failed = 0
        
        duplicate = 0

        # =================================================
        # PRODUCTS
        # =================================================

        if import_type == "products":

            for row in rows:

                row_errors, is_duplicate = (
                    validate_product_row(
                        db,
                        company_id,
                        row
                    )
                )


                if is_duplicate:

                    duplicate += 1

                    continue


                if row_errors:

                    failed += 1

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


        # =================================================
        # CUSTOMERS
        # =================================================

        elif import_type == "customers":

            for row in rows:
        
                row_errors = (
                    validate_customer_row(
                        db,
                        company_id,
                        row
                    )
                )


                if row_errors:

                    failed += 1

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

                    continue


                customer = Customer(

                    company_id=company_id,

                    customer_id=
                        f"IMP-{datetime.utcnow().timestamp()}",

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


        # =================================================
        # SALES
        # =================================================

        elif import_type == "sales":

            for row in rows:

                row_errors = (
                    validate_sales_row(
                        db,
                        company_id,
                        row
                    )
                )

                if row_errors:

                    failed += 1

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

                    continue


                quantity = int(
                    row["Quantity"]
                )


                if quantity > product.stock_quantity:

                    failed += 1

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


        elif import_type == "customers":

            row_errors = (
                validate_customer_row(
                    db,
                    company_id,
                    row
                )
            )


        elif import_type == "sales":

            row_errors = (
                validate_sales_row(
                    db,
                    company_id,
                    row
                )
            )


        if is_duplicate:

            duplicate += 1

            errors.append({

                "row_number": index,

                "error_type": "Duplicate",

                "error_message":
                    "Duplicate record."

            })


        elif row_errors:

            invalid += 1

            errors.append({

                "row_number": index,

                "error_type": "Validation",

                "error_message":
                    "; ".join(row_errors)

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