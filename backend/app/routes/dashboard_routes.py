from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.services.dashboard_service import (
    get_dashboard_data
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_dashboard_data(
        db,
        current_user.company_id
    )