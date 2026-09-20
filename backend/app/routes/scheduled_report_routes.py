from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.models.user import User

from app.schemas.scheduled_report_schema import (
    ScheduledReportCreate,
    ScheduledReportUpdate,
)

from app.services.scheduled_report_service import (
    create_scheduled_report,
    get_scheduled_reports,
    get_scheduled_report,
    update_scheduled_report,
    set_scheduled_report_status,
    delete_scheduled_report,
)


router = APIRouter(
    prefix="/scheduled-reports",
    tags=["Scheduled Reports"],
)


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

@router.post("/")
def create_report_schedule(
    data: ScheduledReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        return create_scheduled_report(
            db=db,
            company_id=current_user.company_id,
            user_id=current_user.id,
            report_type=data.report_type,
            filters=data.filters,
            frequency=data.frequency,
            execution_time=data.execution_time,
            recipients=data.recipients,
            export_format=data.export_format,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ---------------------------------------------------------
# Get all
# ---------------------------------------------------------

@router.get("/")
def list_scheduled_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_scheduled_reports(
        db=db,
        company_id=current_user.company_id,
    )


# ---------------------------------------------------------
# Get one
# ---------------------------------------------------------

@router.get("/{scheduled_report_id}")
def get_one_scheduled_report(
    scheduled_report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_scheduled_report(
        db=db,
        company_id=current_user.company_id,
        scheduled_report_id=scheduled_report_id,
    )

    if not report:

        raise HTTPException(
            status_code=404,
            detail="Scheduled report not found",
        )

    return report


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put("/{scheduled_report_id}")
def update_report_schedule(
    scheduled_report_id: int,
    data: ScheduledReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        updated_report = update_scheduled_report(
            db=db,
            company_id=current_user.company_id,
            scheduled_report_id=scheduled_report_id,
            data=data.model_dump(
                exclude_unset=True
            ),
        )

        if not updated_report:

            raise HTTPException(
                status_code=404,
                detail="Scheduled report not found",
            )

        return updated_report

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ---------------------------------------------------------
# Enable / Disable
# ---------------------------------------------------------

@router.patch("/{scheduled_report_id}/status")
def change_report_status(
    scheduled_report_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = set_scheduled_report_status(
        db=db,
        company_id=current_user.company_id,
        scheduled_report_id=scheduled_report_id,
        is_active=is_active,
    )

    if not report:

        raise HTTPException(
            status_code=404,
            detail="Scheduled report not found",
        )

    return report


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------

@router.delete("/{scheduled_report_id}")
def remove_scheduled_report(
    scheduled_report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_scheduled_report(
        db=db,
        company_id=current_user.company_id,
        scheduled_report_id=scheduled_report_id,
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Scheduled report not found",
        )

    return {
        "message": "Scheduled report deleted successfully"
    }