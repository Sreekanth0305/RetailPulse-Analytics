from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.services.user_service import (
    get_user_profile,
    get_users_by_company
)
from app.schemas.user_schema import UserResponse, UserProfileResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_user_profile(
        db,
        current_user.id
    )

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_users_by_company(
        db,
        current_user.company_id
    )