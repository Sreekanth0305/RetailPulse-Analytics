import json
from datetime import datetime

from app.config.database import SessionLocal
from app.models.scheduled_report import ScheduledReport
from app.services.report_service import generate_report
from app.services.report_export_service import export_report_csv, export_report_pdf
from app.services.scheduled_report_service import calculate_next_run


def execute_scheduled_report(scheduled_report_id: int):
    db = SessionLocal()

    try:
        scheduled_report = (
            db.query(ScheduledReport)
            .filter(ScheduledReport.id == scheduled_report_id)
            .first()
        )

        if not scheduled_report:
            return

        # Convert stored filters JSON into dictionary
        filters = {}

        if scheduled_report.filters:
            try:
                filters = json.loads(scheduled_report.filters)
            except json.JSONDecodeError:
                filters = {}

        # Generate the report
        report_data = generate_report(
            db=db,
            report_type=scheduled_report.report_type,
            company_id=scheduled_report.company_id,
            user_id=scheduled_report.user_id,
            filters=filters,
            page=1,
            limit=10000,
            sort_by="id",
            sort_order="desc"
        )

        # Generate requested export format
        if scheduled_report.export_format.upper() == "CSV":
            export_report_csv(
                report_data,
                scheduled_report.report_type,
                filters
            )

        elif scheduled_report.export_format.upper() == "PDF":
            export_report_pdf(
                report_data,
                scheduled_report.report_type,
                filters
            )

        # At this stage recipients are recorded,
        # but actual email sending will be added later.
        print(
            f"Scheduled report generated successfully. "
            f"Recipients: {scheduled_report.recipients}"
        )

        # Update execution status
        scheduled_report.last_run_at = datetime.utcnow()
        scheduled_report.last_run_status = "Success"
        scheduled_report.last_error_message = None
        
        # Calculate the next execution time
        scheduled_report.next_run_at = calculate_next_run(
            frequency=scheduled_report.frequency,
            execution_time=scheduled_report.execution_time,
            current_time=scheduled_report.last_run_at
        )
        
        db.commit()

    except Exception as e:
        scheduled_report = (
            db.query(ScheduledReport)
            .filter(ScheduledReport.id == scheduled_report_id)
            .first()
        )

        if scheduled_report:
            scheduled_report.last_run_at = datetime.utcnow()
            scheduled_report.last_run_status = "Failed"
            scheduled_report.last_error_message = str(e)
            
            # Schedule the next attempt even if this execution failed
            scheduled_report.next_run_at = calculate_next_run(
                frequency=scheduled_report.frequency,
                execution_time=scheduled_report.execution_time,
                current_time=scheduled_report.last_run_at
            )
            
            db.commit()

        print(
            f"Scheduled report {scheduled_report_id} failed: {str(e)}"
        )

    finally:
        db.close()