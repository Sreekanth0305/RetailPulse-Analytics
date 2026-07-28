from sqlalchemy.orm import Session

from app.models.customer_timeline import CustomerTimeline


# ----------------------------------------
# Add Activity
# ----------------------------------------
def add_customer_activity(

    db: Session,

    company_id: int,

    customer_id: int,

    activity: str,

    description: str

):

    timeline = CustomerTimeline(

        company_id=company_id,

        customer_id=customer_id,

        activity=activity,

        description=description

    )

    db.add(timeline)

    db.commit()

    db.refresh(timeline)

    return timeline


# ----------------------------------------
# Get Timeline
# ----------------------------------------
def get_customer_timeline(

    db: Session,

    company_id: int,

    customer_id: int

):

    return (

        db.query(CustomerTimeline)

        .filter(

            CustomerTimeline.company_id == company_id,

            CustomerTimeline.customer_id == customer_id

        )

        .order_by(CustomerTimeline.created_at.desc())

        .all()

    )