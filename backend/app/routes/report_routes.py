from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.models.user import User
from app.services.report_service import (
    generate_report,
    REPORT_TYPES,
)

from app.services.report_export_service import (
    export_report_csv,
    export_report_pdf,
)

import io
import json


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


# ---------------------------------------------------------
# Generate Report
# ---------------------------------------------------------

@router.get("/{report_type}")
def get_report(
    report_type: str,
    filters: str | None = Query(
        default=None,
        description="JSON string containing report filters"
    ),
    page: int = Query(
        default=1,
        ge=1
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    sort_by: str = Query(
        default=""
    ),
    sort_order: str = Query(
        default="desc"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate one of the supported reports.
    """

    # -----------------------------------------------------
    # Check report type
    # -----------------------------------------------------

    if report_type not in REPORT_TYPES:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid report type",
                "available_reports": REPORT_TYPES,
            },
        )

    # -----------------------------------------------------
    # Parse filters
    # -----------------------------------------------------

    report_filters = {}

    if filters:
        import json

        try:
            report_filters = json.loads(filters)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid filters JSON"
            )

    # -----------------------------------------------------
    # Company isolation
    # -----------------------------------------------------

    if not current_user.company_id:
        raise HTTPException(
            status_code=403,
            detail="User is not associated with a company"
        )

    # -----------------------------------------------------
    # Generate report
    # -----------------------------------------------------

    try:

        result = generate_report(
            db=db,
            company_id=current_user.company_id,
            user_id=current_user.id,
            report_type=report_type,
            filters=report_filters,
            page=page,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Report generation failed: {str(e)}"
        )
    
    


# ---------------------------------------------------------
# Get Available Report Types
# ---------------------------------------------------------

@router.get("/")
def get_report_types(
    current_user: User = Depends(get_current_user),
):
    """
    Returns all available report types.
    """

    return {
        "report_types": REPORT_TYPES
    }

# ---------------------------------------------------------
# Export Report as CSV
# ---------------------------------------------------------

@router.get("/{report_type}/export/csv")
def export_csv(
    report_type: str,
    filters: str | None = Query(
        default=None
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download report as CSV.
    """

    if report_type not in REPORT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid report type"
        )

    report_filters = {}

    if filters:

        try:
            report_filters = json.loads(filters)

        except json.JSONDecodeError:

            raise HTTPException(
                status_code=400,
                detail="Invalid filters JSON"
            )

    try:

        # Get report data
        report = generate_report(
            db=db,
            company_id=current_user.company_id,
            user_id=current_user.id,
            report_type=report_type,
            filters=report_filters,
            page=1,
            limit=10000,
            sort_by="",
            sort_order="desc",
        )

        csv_content = export_report_csv(
            report_type=report_type,
            filters=report_filters,
            items=report["items"],
        )

        filename = (
            report_type
            .lower()
            .replace(" ", "_")
            + ".csv"
        )

        return StreamingResponse(
            io.BytesIO(
                csv_content.encode("utf-8")
            ),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            },
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"CSV export failed: {str(e)}"
        )

# ---------------------------------------------------------
# Export Report as PDF
# ---------------------------------------------------------

@router.get("/{report_type}/export/pdf")
def export_pdf(
    report_type: str,
    filters: str | None = Query(
        default=None
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download report as PDF.
    """

    if report_type not in REPORT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid report type"
        )

    report_filters = {}

    if filters:

        try:
            report_filters = json.loads(filters)

        except json.JSONDecodeError:

            raise HTTPException(
                status_code=400,
                detail="Invalid filters JSON"
            )

    try:

        # Get report data
        report = generate_report(
            db=db,
            company_id=current_user.company_id,
            user_id=current_user.id,
            report_type=report_type,
            filters=report_filters,
            page=1,
            limit=10000,
            sort_by="",
            sort_order="desc",
        )

        pdf_content = export_report_pdf(
            report_type=report_type,
            filters=report_filters,
            items=report["items"],
        )

        filename = (
            report_type
            .lower()
            .replace(" ", "_")
            + ".pdf"
        )

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    f'attachment; filename="{filename}"'
            },
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed: {str(e)}"
        )