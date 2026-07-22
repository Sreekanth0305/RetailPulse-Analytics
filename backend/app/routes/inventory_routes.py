from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.inventory_schema import (
    StockAdjustment,
    ReorderLevelUpdate
)

from app.services.inventory_service import (

    get_inventory,

    search_inventory,

    filter_inventory,

    sort_inventory,

    get_inventory_by_product,

    add_stock,

    remove_stock,

    adjust_stock,

    update_reorder_level,

    get_inventory_movements

)

router = APIRouter(

    prefix="/inventory",

    tags=["Inventory"]

)

# =====================================================
# Get All Inventory
# =====================================================

@router.get("/")
def get_all_inventory(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return get_inventory(

        db,

        current_user.company_id

    )

# =====================================================
# Search Inventory
# =====================================================

@router.get("/search")
def search_inventory_api(

    keyword: str,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return search_inventory(

        db,

        current_user.company_id,

        keyword

    )

# =====================================================
# Filter Inventory
# =====================================================

@router.get("/filter")
def filter_inventory_api(

    category_id: int | None = None,

    brand: str | None = None,

    stock_status: str | None = None,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return filter_inventory(

        db,

        current_user.company_id,

        category_id,

        brand,

        stock_status

    )

# =====================================================
# Sort Inventory
# =====================================================

@router.get("/sort")
def sort_inventory_api(

    sort_by: str,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return sort_inventory(

        db,

        current_user.company_id,

        sort_by

    )

# =====================================================
# Get Inventory By Product
# =====================================================

@router.get("/{product_id}")
def get_inventory_product(

    product_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return get_inventory_by_product(

        db,

        current_user.company_id,

        product_id

    )

# =====================================================
# Add Stock
# =====================================================

@router.post("/{product_id}/add")
def add_product_stock(

    product_id: int,

    data: StockAdjustment,

    request: Request,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return add_stock(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        product_id=product_id,

        data=data,

        request=request

    )

# =====================================================
# Remove Stock
# =====================================================

@router.post("/{product_id}/remove")
def remove_product_stock(

    product_id: int,

    data: StockAdjustment,

    request: Request,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return remove_stock(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        product_id=product_id,

        data=data,

        request=request

    )

# =====================================================
# Manual Adjustment
# =====================================================

@router.put("/{product_id}/adjust")
def adjust_product_stock(

    product_id: int,

    data: StockAdjustment,

    request: Request,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return adjust_stock(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        product_id=product_id,

        data=data,

        request=request

    )

# =====================================================
# Update Reorder Level
# =====================================================

@router.put("/{product_id}/reorder-level")
def update_reorder(

    product_id: int,

    data: ReorderLevelUpdate,

    request: Request,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return update_reorder_level(

        db=db,

        company_id=current_user.company_id,

        user_id=current_user.id,

        product_id=product_id,

        data=data,

        request=request

    )

# =====================================================
# Inventory Movement History
# =====================================================

@router.get("/{product_id}/movements")
def inventory_history(

    product_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return get_inventory_movements(

        db,

        current_user.company_id,

        product_id

    )