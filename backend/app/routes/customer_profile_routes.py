from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.schemas.customer_profile_schema import CustomerProfileResponse

from app.services.customer_profile_service import get_customer_profile


router = APIRouter(

    prefix="/customer-profile",

    tags=["Customer Profile"]

)


@router.get(

    "/{customer_id}",

    response_model=CustomerProfileResponse

)

def get_customer_profile_api(

    customer_id: int,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)

):

    return get_customer_profile(

        db=db,

        company_id=current_user.company_id,

        customer_id=customer_id

    )