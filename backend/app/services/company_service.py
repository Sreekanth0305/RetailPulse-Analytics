from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.config.security import hash_password

from app.models.company import Company
from app.models.audit_log import AuditLog
from app.schemas.company_schema import CompanyCreateSchema


def get_company_by_email(db: Session, email: str):
    return db.query(Company).filter(
        Company.email == email
    ).first()


def create_company(db: Session, company: CompanyCreateSchema):

    existing_company = get_company_by_email(
        db,
        company.email
    )

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Company already exists."
        )

    db_company = Company(
        name=company.name,
        industry=company.industry,
        email=company.email,
        address=company.address,
        phone=company.phone
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


def register_company(db: Session, company: CompanyCreateSchema):

    existing_company = get_company_by_email(
        db,
        company.email
    )

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Company already exists."
        )

    # -----------------------------
    # Create Company
    # -----------------------------

    db_company = Company(
        name=company.name,
        industry=company.industry,
        email=company.email,
        address=company.address,
        phone=company.phone,
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    # -----------------------------
    # Create Company Admin
    # -----------------------------

    admin = User(
        company_id=db_company.id,
        name=company.admin_name,
        email=company.admin_email,
        password=hash_password(company.admin_password),
        role="Company Admin",
        status="Active"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # -----------------------------
    # Audit Log
    # -----------------------------
    audit = AuditLog(
        company_id=db_company.id,
        user_id=admin.id,
        action="Company Registered",
        ip_address="",
        browser=""
    )
    
    db.add(audit)
    db.commit()
    
    db.refresh(db_company)
    
    return db_company

def get_company_by_id(db: Session, company_id: int):

    return db.query(Company).filter(
        Company.id == company_id
    ).first()


def get_all_companies(db: Session):

    return db.query(Company).all()