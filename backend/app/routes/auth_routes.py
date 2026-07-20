from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth_schema import (
    ChangePasswordRequest,
    RefreshTokenRequest,
    UserProfileResponse
)
from app.config.database import get_db
from app.services.auth_service import (
    login_user,
    logout_user,
    change_user_password,
    refresh_access_token,
    get_current_user_profile
)
from app.config.jwt import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data, request)

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

@router.get(
    "/me",
    response_model=UserProfileResponse
)
def get_profile(

    current_user=Depends(get_current_user)

):

    return get_current_user_profile(current_user)

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