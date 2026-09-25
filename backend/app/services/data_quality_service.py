from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement
from app.models.customer import Customer
from app.models.data_quality_issue import DataQualityIssue
from app.models.reconciliation_history import ReconciliationHistory


ISSUE_OPEN_STATUSES = [
    "Open",
    "Investigating"
]


def create_or_update_issue(
    db: Session,
    company_id: int,
    issue_type: str,
    severity: str,
    module: str,
    affected_record: str,
    description: str,
    issue_key: str
):
    existing = (
        db.query(DataQualityIssue)
        .filter(
            DataQualityIssue.company_id == company_id,
            DataQualityIssue.issue_key == issue_key,
            DataQualityIssue.status.in_(ISSUE_OPEN_STATUSES)
        )
        .first()
    )

    if existing:
        return existing, False

    issue = DataQualityIssue(
        company_id=company_id,
        issue_type=issue_type,
        severity=severity,
        module=module,
        affected_record=affected_record,
        description=description,
        status="Open",
        detected_at=datetime.utcnow(),
        issue_key=issue_key
    )

    db.add(issue)

    return issue, True


# ---------------------------------------------------------
# 1. INVALID / INACTIVE PRODUCTS IN SALES
# ---------------------------------------------------------

def check_invalid_products(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    rows = (
        db.query(
            SaleItem,
            Sale,
            Product
        )
        .join(Sale, SaleItem.sale_id == Sale.id)
        .outerjoin(Product, SaleItem.product_id == Product.id)
        .filter(
            Sale.company_id == company_id
        )
        .all()
    )

    for sale_item, sale, product in rows:

        checked += 1

        if product is None:

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Invalid Product Reference",
                severity="Error",
                module="Sales",
                affected_record=f"SaleItem #{sale_item.id}",
                description=(
                    f"Sale #{sale.id} references product "
                    f"ID {sale_item.product_id}, but that product "
                    f"does not exist."
                ),
                issue_key=(
                    f"INVALID_PRODUCT:"
                    f"{sale.id}:{sale_item.id}:"
                    f"{sale_item.product_id}"
                )
            )

            if is_new:
                created += 1

        elif product.status != "Active":

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Inactive Product Sold",
                severity="Warning",
                module="Sales",
                affected_record=f"Sale #{sale.id}",
                description=(
                    f"Sale #{sale.id} contains product "
                    f"'{product.name}' which is currently "
                    f"marked as {product.status}."
                ),
                issue_key=(
                    f"INACTIVE_PRODUCT:"
                    f"{sale.id}:{product.id}"
                )
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# 2. INVALID CUSTOMER REFERENCES
# ---------------------------------------------------------

def check_invalid_customers(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    sales = (
        db.query(Sale)
        .filter(
            Sale.company_id == company_id
        )
        .all()
    )

    customers = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.is_deleted == False
        )
        .all()
    )

    customer_names = {
        customer.full_name.strip().lower()
        for customer in customers
    }

    for sale in sales:

        checked += 1

        sale_customer = sale.customer_name.strip().lower()

        if sale_customer not in customer_names:

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Invalid Customer Reference",
                severity="Warning",
                module="Sales",
                affected_record=f"Sale #{sale.id}",
                description=(
                    f"Sale #{sale.id} references customer "
                    f"'{sale.customer_name}', but no matching "
                    f"customer exists."
                ),
                issue_key=(
                    f"INVALID_CUSTOMER:"
                    f"{sale.id}:{sale_customer}"
                )
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# 3. DUPLICATE / INVALID PRODUCT SKU
# ---------------------------------------------------------

def check_product_skus(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    products = (
        db.query(Product)
        .filter(
            Product.company_id == company_id
        )
        .all()
    )

    sku_map = {}

    for product in products:

        checked += 1

        if not product.sku or not product.sku.strip():

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Missing Product SKU",
                severity="Error",
                module="Products",
                affected_record=f"Product #{product.id}",
                description=(
                    f"Product '{product.name}' "
                    f"does not have a valid SKU."
                ),
                issue_key=f"MISSING_SKU:{product.id}"
            )

            if is_new:
                created += 1

            continue

        sku = product.sku.strip().lower()

        sku_map.setdefault(sku, []).append(product)

    for sku, duplicate_products in sku_map.items():

        if len(duplicate_products) > 1:

            product_ids = ",".join(
                str(product.id)
                for product in duplicate_products
            )

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Duplicate Product SKU",
                severity="Error",
                module="Products",
                affected_record=product_ids,
                description=(
                    f"SKU '{sku}' is assigned to multiple "
                    f"products: {product_ids}."
                ),
                issue_key=f"DUPLICATE_SKU:{sku}"
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# 4. MISSING CUSTOMER INFORMATION
# ---------------------------------------------------------

def check_customer_information(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    customers = (
        db.query(Customer)
        .filter(
            Customer.company_id == company_id,
            Customer.is_deleted == False
        )
        .all()
    )

    for customer in customers:

        checked += 1

        missing_fields = []

        if not customer.full_name:
            missing_fields.append("full_name")

        if not customer.email:
            missing_fields.append("email")

        if not customer.phone:
            missing_fields.append("phone")

        if not customer.customer_type:
            missing_fields.append("customer_type")

        if missing_fields:

            fields = ", ".join(missing_fields)

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Missing Customer Information",
                severity="Error",
                module="Customers",
                affected_record=f"Customer #{customer.id}",
                description=(
                    f"Customer #{customer.id} is missing "
                    f"mandatory information: {fields}."
                ),
                issue_key=(
                    f"MISSING_CUSTOMER_FIELDS:"
                    f"{customer.id}:{fields}"
                )
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# 5. INVENTORY / STOCK MOVEMENT CONSISTENCY
# ---------------------------------------------------------

def check_inventory_movements(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    inventories = (
        db.query(Inventory)
        .filter(
            Inventory.company_id == company_id
        )
        .all()
    )

    for inventory in inventories:

        movements = (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.inventory_id == inventory.id
            )
            .order_by(
                InventoryMovement.created_at.asc(),
                InventoryMovement.id.asc()
            )
            .all()
        )

        previous_updated_quantity = None

        for movement in movements:

            checked += 1

            # Check individual movement arithmetic
            expected_updated = (
                movement.previous_quantity
                + movement.quantity_changed
            )

            if movement.updated_quantity != expected_updated:

                _, is_new = create_or_update_issue(
                    db=db,
                    company_id=company_id,
                    issue_type="Invalid Stock Movement",
                    severity="Error",
                    module="Inventory",
                    affected_record=(
                        f"Movement #{movement.id}"
                    ),
                    description=(
                        f"Movement #{movement.id} has previous "
                        f"quantity {movement.previous_quantity}, "
                        f"change {movement.quantity_changed}, "
                        f"but updated quantity is "
                        f"{movement.updated_quantity}. "
                        f"Expected {expected_updated}."
                    ),
                    issue_key=(
                        f"INVALID_MOVEMENT:"
                        f"{movement.id}"
                    )
                )

                if is_new:
                    created += 1

            # Check chain consistency
            if (
                previous_updated_quantity is not None
                and movement.previous_quantity
                != previous_updated_quantity
            ):

                _, is_new = create_or_update_issue(
                    db=db,
                    company_id=company_id,
                    issue_type="Stock Movement Chain Mismatch",
                    severity="Error",
                    module="Inventory",
                    affected_record=(
                        f"Movement #{movement.id}"
                    ),
                    description=(
                        f"Movement #{movement.id} starts from "
                        f"{movement.previous_quantity}, but the "
                        f"previous movement ended at "
                        f"{previous_updated_quantity}."
                    ),
                    issue_key=(
                        f"MOVEMENT_CHAIN:"
                        f"{inventory.id}:{movement.id}"
                    )
                )

                if is_new:
                    created += 1

            previous_updated_quantity = (
                movement.updated_quantity
            )

        # Compare latest movement with inventory
        if (
            previous_updated_quantity is not None
            and inventory.current_stock
            != previous_updated_quantity
        ):

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Inventory Quantity Mismatch",
                severity="Error",
                module="Inventory",
                affected_record=f"Inventory #{inventory.id}",
                description=(
                    f"Product ID {inventory.product_id} has "
                    f"current inventory quantity "
                    f"{inventory.current_stock}, while the latest "
                    f"stock movement shows "
                    f"{previous_updated_quantity}."
                ),
                issue_key=(
                    f"INVENTORY_MOVEMENT_MISMATCH:"
                    f"{inventory.id}"
                )
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# 6. SALE QUANTITY VS CURRENT INVENTORY
# ---------------------------------------------------------

def check_sales_against_inventory(
    db: Session,
    company_id: int
):
    created = 0
    checked = 0

    sales_data = (
        db.query(
            SaleItem.product_id,
            Product.name,
            Inventory.current_stock
        )
        .join(
            Sale,
            SaleItem.sale_id == Sale.id
        )
        .join(
            Product,
            SaleItem.product_id == Product.id
        )
        .outerjoin(
            Inventory,
            Inventory.product_id == Product.id
        )
        .filter(
            Sale.company_id == company_id
        )
        .all()
    )

    quantity_by_product = {}

    for product_id, product_name, current_stock in sales_data:

        quantity_by_product.setdefault(
            product_id,
            {
                "name": product_name,
                "quantity": 0,
                "stock": current_stock or 0
            }
        )

    sale_items = (
        db.query(
            SaleItem.product_id,
            SaleItem.quantity
        )
        .join(
            Sale,
            SaleItem.sale_id == Sale.id
        )
        .filter(
            Sale.company_id == company_id
        )
        .all()
    )

    for product_id, quantity in sale_items:

        checked += 1

        if product_id in quantity_by_product:
            quantity_by_product[product_id]["quantity"] += quantity

    for product_id, data in quantity_by_product.items():

        # This is an aggregate sanity check, not a
        # historical stock-at-exact-sale-time calculation.
        if data["quantity"] > data["stock"]:

            _, is_new = create_or_update_issue(
                db=db,
                company_id=company_id,
                issue_type="Sales Quantity Exceeds Inventory",
                severity="Warning",
                module="Sales",
                affected_record=f"Product #{product_id}",
                description=(
                    f"Product '{data['name']}' has total recorded "
                    f"sales quantity of {data['quantity']} while "
                    f"current inventory is {data['stock']}."
                ),
                issue_key=(
                    f"SALES_INVENTORY:"
                    f"{product_id}:{data['quantity']}:{data['stock']}"
                )
            )

            if is_new:
                created += 1

    return checked, created


# ---------------------------------------------------------
# MAIN RECONCILIATION
# ---------------------------------------------------------

def run_reconciliation(
    db: Session,
    company_id: int,
    user_id: int
):

    execution_id = str(uuid4())

    history = ReconciliationHistory(
        company_id=company_id,
        execution_id=execution_id,
        started_at=datetime.utcnow(),
        triggered_by=user_id,
        execution_status="Running"
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    total_checked = 0
    total_issues = 0
    failed_checks = 0

    checks = [
        check_invalid_products,
        check_invalid_customers,
        check_product_skus,
        check_customer_information,
        check_inventory_movements,
        check_sales_against_inventory
    ]

    try:

        for check in checks:

            try:

                checked, issues = check(
                    db=db,
                    company_id=company_id
                )

                total_checked += checked
                total_issues += issues

            except Exception as e:

                failed_checks += 1

                print(
                    f"Data quality check failed: "
                    f"{check.__name__}: {str(e)}"
                )

        history.completed_at = datetime.utcnow()
        history.records_checked = total_checked
        history.issues_detected = total_issues
        history.failed_checks = failed_checks

        if failed_checks > 0:
            history.execution_status = "Failed"
        elif total_issues > 0:
            history.execution_status = "Completed with Issues"
        else:
            history.execution_status = "Completed"

        db.commit()

        return {
            "execution_id": execution_id,
            "status": history.execution_status,
            "records_checked": total_checked,
            "issues_detected": total_issues,
            "failed_checks": failed_checks
        }

    except Exception as e:

        history.completed_at = datetime.utcnow()
        history.execution_status = "Failed"
        history.error_message = str(e)

        db.commit()

        raise