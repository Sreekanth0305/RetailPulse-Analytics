from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.company import Company
from app.schemas.user_schema import UserCreate
from app.config.security import hash_password


def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(db: Session, user: UserCreate):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists."
        )

    hashed_password = hash_password(user.password)

    db_user = User(
        company_id=user.company_id,
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        status="Active"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_all_users(db: Session):

    return db.query(User).all()

def get_users_by_company(db: Session, company_id: int):

    return (
        db.query(User)
        .filter(User.company_id == company_id)
        .all()
    )

def get_user_profile(
    db: Session,
    user_id: int
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "company": user.company.name,
        "last_login": user.last_login,
        "status": user.status
    }