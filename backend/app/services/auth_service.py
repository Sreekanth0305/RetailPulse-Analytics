from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from app.models.user import User
from jose import JWTError
from app.config.jwt import decode_token
from app.models.refresh_token import RefreshToken
from app.schemas.auth_schema import LoginRequest
from app.services.audit_service import create_audit_log
from fastapi.security import OAuth2PasswordRequestForm
from app.config.security import verify_password, hash_password

from app.config.settings import settings

from datetime import datetime, timedelta

from app.config.jwt import (
    create_access_token,
    create_refresh_token
)


def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def generate_tokens(db: Session, user: User):

    payload = {
    "user_id": user.id,
    "company_id": user.company_id,
    "email": user.email,
    "role": user.role,
    }
    
    access_token = create_access_token(payload)

    refresh_token = create_refresh_token(payload)

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


def login_user(
    db: Session,
    credentials: OAuth2PasswordRequestForm
):

    user = authenticate_user(
        db,
        credentials.username,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)

    create_audit_log(
    db=db,
    company_id=user.company_id,
    user_id=user.id,
    action="User Login"
    )
    
    return generate_tokens(db, user)

def logout_user(
    db: Session,
    user: User,
    request: Request
):

    create_audit_log(
        db=db,
        company_id=user.company_id,
        user_id=user.id,
        action="User Logout",
        ip_address=request.client.host,
        browser=request.headers.get("user-agent")
    )

    return {
        "message": "Logged out successfully."
    }

def change_user_password(
    db: Session,
    user: User,
    data
):

    if not verify_password(data.old_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect."
        )

    user.password = hash_password(data.new_password)

    db.commit()

    create_audit_log(
        db=db,
        company_id=user.company_id,
        user_id=user.id,
        action="Password Changed",
        ip_address="127.0.0.1",
        browser="Swagger UI"
    )

    return {
        "message": "Password changed successfully."
    }

def refresh_access_token(
    db: Session,
    data
):
    # Check if refresh token exists in database
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == data.refresh_token)
        .first()
    )

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token."
        )

    # Check if refresh token is expired
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired."
        )

    # Decode the refresh token
    try:
        payload = decode_token(data.refresh_token)

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token."
        )

    # Create a new access token
    new_payload = {
        "user_id": payload["user_id"],
        "company_id": payload["company_id"],
        "email": payload["email"],
        "role": payload["role"]
    }

    access_token = create_access_token(new_payload)

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }