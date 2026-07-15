from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.company_schema import (
    CompanyCreateSchema,
     CompanyResponse
)
from app.services.company_service import register_company
router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "/register",
    response_model=CompanyResponse,
    status_code=201
)
def register_company_api(
    company: CompanyCreateSchema,
    db: Session = Depends(get_db)
):
    return register_company(db, company)