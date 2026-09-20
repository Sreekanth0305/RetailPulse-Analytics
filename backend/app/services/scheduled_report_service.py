import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.scheduled_report import ScheduledReport


# ---------------------------------------------------------
# Allowed values
# ---------------------------------------------------------

ALLOWED_FREQUENCIES = [
    "Daily",
    "Weekly",
    "Monthly",
]

ALLOWED_FORMATS = [
    "CSV",
    "PDF",
]


# ---------------------------------------------------------
# Calculate next run time
# ---------------------------------------------------------

def calculate_next_run(
    frequency: str,
    execution_time: str,
    from_time=None,
):
    """
    Calculates the next scheduled execution time.

    execution_time format:
        HH:MM

    frequency:
        Daily
        Weekly
        Monthly
    """

    if from_time is None:
        from_time = datetime.utcnow()

    try:
        hour, minute = map(
            int,
            execution_time.split(":")
        )

    except Exception:
        raise ValueError(
            "Execution time must be in HH:MM format"
        )

    next_run = from_time.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

    # If today's execution time has already passed,
    # move to the next occurrence.
    if next_run <= from_time:

        if frequency == "Daily":

            next_run += timedelta(days=1)

        elif frequency == "Weekly":

            next_run += timedelta(days=7)

        elif frequency == "Monthly":

            # Simple monthly calculation.
            # Move approximately to the next month.
            if next_run.month == 12:
                next_run = next_run.replace(
                    year=next_run.year + 1,
                    month=1,
                )
            else:
                next_run = next_run.replace(
                    month=next_run.month + 1
                )

        else:
            raise ValueError(
                "Invalid frequency"
            )

    return next_run


# ---------------------------------------------------------
# Create Scheduled Report
# ---------------------------------------------------------

def create_scheduled_report(
    db: Session,
    company_id: int,
    user_id: int,
    report_type: str,
    filters: dict | None,
    frequency: str,
    execution_time: str,
    recipients: list[str],
    export_format: str,
):
    """
    Creates a scheduled report belonging to
    the current company/user.
    """

    if frequency not in ALLOWED_FREQUENCIES:

        raise ValueError(
            "Frequency must be Daily, Weekly, or Monthly"
        )

    if export_format not in ALLOWED_FORMATS:

        raise ValueError(
            "Export format must be CSV or PDF"
        )

    if not recipients:

        raise ValueError(
            "At least one recipient is required"
        )

    # Validate execution time
    try:

        hour, minute = map(
            int,
            execution_time.split(":")
        )

        if not (
            0 <= hour <= 23
            and 0 <= minute <= 59
        ):
            raise ValueError

    except Exception:

        raise ValueError(
            "Execution time must be in HH:MM format"
        )

    next_run_at = calculate_next_run(
        frequency=frequency,
        execution_time=execution_time,
    )

    scheduled_report = ScheduledReport(
        company_id=company_id,
        user_id=user_id,
        report_type=report_type,
        filters=json.dumps(
            filters or {}
        ),
        frequency=frequency,
        execution_time=execution_time,
        recipients=json.dumps(
            recipients
        ),
        export_format=export_format,
        is_active=True,
        last_run_at=None,
        last_run_status=None,
        last_error_message=None,
        next_run_at=next_run_at,
    )

    db.add(scheduled_report)
    db.commit()
    db.refresh(scheduled_report)

    return scheduled_report


# ---------------------------------------------------------
# Get Scheduled Reports
# ---------------------------------------------------------

def get_scheduled_reports(
    db: Session,
    company_id: int,
):
    """
    Returns scheduled reports belonging only
    to the current company.
    """

    return (
        db.query(ScheduledReport)
        .filter(
            ScheduledReport.company_id
            == company_id
        )
        .order_by(
            ScheduledReport.created_at.desc()
        )
        .all()
    )


# ---------------------------------------------------------
# Get One Scheduled Report
# ---------------------------------------------------------

def get_scheduled_report(
    db: Session,
    company_id: int,
    scheduled_report_id: int,
):
    """
    Returns one scheduled report if it belongs
    to the current company.
    """

    return (
        db.query(ScheduledReport)
        .filter(
            ScheduledReport.id
            == scheduled_report_id,
            ScheduledReport.company_id
            == company_id,
        )
        .first()
    )


# ---------------------------------------------------------
# Update Scheduled Report
# ---------------------------------------------------------

def update_scheduled_report(
    db: Session,
    company_id: int,
    scheduled_report_id: int,
    data: dict,
):
    """
    Updates an existing scheduled report.
    """

    scheduled_report = get_scheduled_report(
        db=db,
        company_id=company_id,
        scheduled_report_id=scheduled_report_id,
    )

    if not scheduled_report:
        return None

    # ---------------------------------------------
    # Update report type
    # ---------------------------------------------

    if data.get("report_type") is not None:

        scheduled_report.report_type = (
            data["report_type"]
        )

    # ---------------------------------------------
    # Update filters
    # ---------------------------------------------

    if data.get("filters") is not None:

        scheduled_report.filters = json.dumps(
            data["filters"]
        )

    # ---------------------------------------------
    # Update frequency
    # ---------------------------------------------

    if data.get("frequency") is not None:

        if (
            data["frequency"]
            not in ALLOWED_FREQUENCIES
        ):
            raise ValueError(
                "Invalid frequency"
            )

        scheduled_report.frequency = (
            data["frequency"]
        )

    # ---------------------------------------------
    # Update execution time
    # ---------------------------------------------

    if data.get("execution_time") is not None:

        execution_time = data[
            "execution_time"
        ]

        try:

            hour, minute = map(
                int,
                execution_time.split(":")
            )

            if not (
                0 <= hour <= 23
                and 0 <= minute <= 59
            ):
                raise ValueError

        except Exception:

            raise ValueError(
                "Execution time must be in HH:MM format"
            )

        scheduled_report.execution_time = (
            execution_time
        )

    # ---------------------------------------------
    # Update recipients
    # ---------------------------------------------

    if data.get("recipients") is not None:

        if not data["recipients"]:

            raise ValueError(
                "At least one recipient is required"
            )

        scheduled_report.recipients = json.dumps(
            data["recipients"]
        )

    # ---------------------------------------------
    # Update format
    # ---------------------------------------------

    if data.get("export_format") is not None:

        if (
            data["export_format"]
            not in ALLOWED_FORMATS
        ):
            raise ValueError(
                "Invalid export format"
            )

        scheduled_report.export_format = (
            data["export_format"]
        )

    # ---------------------------------------------
    # Update active status
    # ---------------------------------------------

    if data.get("is_active") is not None:

        scheduled_report.is_active = (
            data["is_active"]
        )

    # ---------------------------------------------
    # Recalculate next run
    # ---------------------------------------------

    if (
        data.get("frequency") is not None
        or data.get("execution_time") is not None
        or data.get("is_active") is not None
    ):

        if scheduled_report.is_active:

            scheduled_report.next_run_at = (
                calculate_next_run(
                    frequency=scheduled_report.frequency,
                    execution_time=scheduled_report.execution_time,
                )
            )

        else:

            scheduled_report.next_run_at = None

    scheduled_report.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(scheduled_report)

    return scheduled_report


# ---------------------------------------------------------
# Enable / Disable Scheduled Report
# ---------------------------------------------------------

def set_scheduled_report_status(
    db: Session,
    company_id: int,
    scheduled_report_id: int,
    is_active: bool,
):
    """
    Enables or disables a scheduled report.
    """

    scheduled_report = get_scheduled_report(
        db=db,
        company_id=company_id,
        scheduled_report_id=scheduled_report_id,
    )

    if not scheduled_report:
        return None

    scheduled_report.is_active = is_active

    if is_active:

        scheduled_report.next_run_at = (
            calculate_next_run(
                frequency=scheduled_report.frequency,
                execution_time=scheduled_report.execution_time,
            )
        )

    else:

        scheduled_report.next_run_at = None

    db.commit()
    db.refresh(scheduled_report)

    return scheduled_report


# ---------------------------------------------------------
# Delete Scheduled Report
# ---------------------------------------------------------

def delete_scheduled_report(
    db: Session,
    company_id: int,
    scheduled_report_id: int,
):
    """
    Deletes a scheduled report belonging
    to the current company.
    """

    scheduled_report = get_scheduled_report(
        db=db,
        company_id=company_id,
        scheduled_report_id=scheduled_report_id,
    )

    if not scheduled_report:
        return False

    db.delete(scheduled_report)
    db.commit()

    return True