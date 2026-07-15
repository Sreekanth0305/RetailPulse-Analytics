from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth_schema import ChangePasswordRequest
from app.config.database import get_db
from app.services.auth_service import login_user
from app.config.jwt import get_current_user
from app.services.auth_service import logout_user
from app.services.auth_service import change_user_password
from app.schemas.auth_schema import RefreshTokenRequest
from app.services.auth_service import refresh_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data)

@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token(
        db,
        data
    )

@router.post("/logout")
def logout(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return logout_user(
        db,
        current_user,
        request
    )

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return change_user_password(
        db,
        current_user,
        data
    )