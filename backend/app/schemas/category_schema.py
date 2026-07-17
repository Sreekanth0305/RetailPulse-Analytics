from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Create Category
# -----------------------------
class CategoryCreate(BaseModel):

    name: str
    description: str
    status: str = "Active"


# -----------------------------
# Update Category
# -----------------------------
class CategoryUpdate(BaseModel):

    name: str
    description: str
    status: str


# -----------------------------
# Category Response
# -----------------------------
class CategoryResponse(BaseModel):

    id: int
    company_id: int
    name: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Category List Response
# -----------------------------
class CategoryListResponse(BaseModel):

    id: int
    name: str
    description: str
    status: str
    total_products: int

    class Config:
        from_attributes = True