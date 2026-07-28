from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.services.customer_timeline_service import (
    get_customer_timeline
)

router = APIRouter(
    prefix="/customer-timeline",
    tags=["Customer Timeline"]
)


@router.get("/{customer_id}")
def customer_timeline(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_customer_timeline(

        db=db,

        company_id=current_user.company_id,

        customer_id=customer_id

    )