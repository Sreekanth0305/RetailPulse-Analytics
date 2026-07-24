from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.analytics_schema import (
    AnalyticsKPIResponse,
    RevenueTrendResponse, 
    SalesTrendResponse,
    TopSellingProductResponse,
    TopCategoryResponse,
    PaymentMethodResponse,
    SalesChannelResponse,
    InventoryDistributionResponse,
    StockStatusSummaryResponse,
    LowStockProductResponse,
    OutOfStockProductResponse,
    InventoryValueCategoryResponse,
    DrilldownCategoryResponse,
    DrilldownProductResponse,
    DrilldownSaleResponse
)

from app.services.analytics_service import (
    get_dashboard_kpis,
    get_revenue_trend,
    get_sales_trend,
    get_top_selling_products,
    get_top_categories,
    get_sales_by_payment_method,
    get_sales_by_sales_channel,
    get_inventory_distribution,
    get_stock_status_summary,
    get_low_stock_products,
    get_out_of_stock_products,
    get_inventory_value_by_category,
    get_drilldown_categories,
    get_drilldown_products,
    get_drilldown_sales
)

router = APIRouter(

    prefix="/analytics",

    tags=["Analytics"]

)


# =====================================================
# Dashboard KPI Cards
# =====================================================

@router.get(
    "/kpis",
    response_model=AnalyticsKPIResponse
)
def analytics_kpis_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_dashboard_kpis(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -------------------------------------------------
# Revenue Trend
# -------------------------------------------------

@router.get(
    "/revenue-trend",
    response_model=list[RevenueTrendResponse]
)
def revenue_trend_api(

    period: str,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_revenue_trend(

        db=db,

        company_id=current_user.company_id,

        period=period,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Sales Trend
# -----------------------------
@router.get(
    "/sales-trend",
    response_model=list[SalesTrendResponse]
)
def sales_trend_api(

    period: str,

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_sales_trend(

        db=db,

        company_id=current_user.company_id,

        period=period,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Top 10 Best Selling Products
# -----------------------------
@router.get(
    "/top-selling-products",
    response_model=list[TopSellingProductResponse]
)
def top_selling_products_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_top_selling_products(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Top Performing Categories
# -----------------------------
@router.get(
    "/top-categories",
    response_model=list[TopCategoryResponse]
)
def top_categories_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_top_categories(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Sales By Payment Method
# -----------------------------
@router.get(
    "/sales-by-payment-method",
    response_model=list[PaymentMethodResponse]
)
def sales_by_payment_method_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_sales_by_payment_method(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Sales By Sales Channel
# -----------------------------
@router.get(
    "/sales-by-sales-channel",
    response_model=list[SalesChannelResponse]
)
def sales_by_sales_channel_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_sales_by_sales_channel(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Inventory Distribution
# -----------------------------
@router.get(
    "/inventory-distribution",
    response_model=list[InventoryDistributionResponse]
)
def inventory_distribution_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_inventory_distribution(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Stock Status Summary
# -----------------------------
@router.get(
    "/stock-status-summary",
    response_model=list[StockStatusSummaryResponse]
)
def stock_status_summary_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_stock_status_summary(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Top Low Stock Products
# -----------------------------
@router.get(
    "/low-stock-products",
    response_model=list[LowStockProductResponse]
)
def low_stock_products_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_low_stock_products(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

# -----------------------------
# Out Of Stock Products
# -----------------------------
@router.get(
    "/out-of-stock-products",
    response_model=list[OutOfStockProductResponse]
)
def out_of_stock_products_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_out_of_stock_products(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )
# -----------------------------
# Inventory Value By Category
# -----------------------------
@router.get(
    "/inventory-value-by-category",
    response_model=list[InventoryValueCategoryResponse]
)
def inventory_value_by_category_api(

    start_date: str | None = None,

    end_date: str | None = None,

    category_id: int | None = None,

    product_id: int | None = None,

    brand: str | None = None,

    sales_channel: str | None = None,

    payment_method: str | None = None,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_inventory_value_by_category(

        db=db,

        company_id=current_user.company_id,

        start_date=start_date,

        end_date=end_date,

        category_id=category_id,

        product_id=product_id,

        brand=brand,

        sales_channel=sales_channel,

        payment_method=payment_method

    )

@router.get(
    "/drilldown/categories",
    response_model=list[DrilldownCategoryResponse]
)
def drilldown_categories_api(

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_drilldown_categories(

        db,

        current_user.company_id

    )

@router.get(
    "/drilldown/products/{category_id}",
    response_model=list[DrilldownProductResponse]
)
def drilldown_products_api(

    category_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_drilldown_products(

        db,

        current_user.company_id,

        category_id

    )

@router.get(
    "/drilldown/sales/{product_id}",
    response_model=list[DrilldownSaleResponse]
)
def drilldown_sales_api(

    product_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_drilldown_sales(

        db,

        current_user.company_id,

        product_id

    )