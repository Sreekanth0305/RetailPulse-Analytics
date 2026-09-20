from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.config.database import SessionLocal
from app.models.scheduled_report import ScheduledReport
from app.services.scheduled_report_execution_service import (
    execute_scheduled_report
)


scheduler = BackgroundScheduler()


def check_scheduled_reports():
    db = SessionLocal()

    try:
        current_time = datetime.utcnow()

        scheduled_reports = (
            db.query(ScheduledReport)
            .filter(
                ScheduledReport.is_active == True,
                ScheduledReport.next_run_at <= current_time
            )
            .all()
        )

        for report in scheduled_reports:
            print(
                f"Executing scheduled report: {report.id}"
            )

            execute_scheduled_report(report.id)

    except Exception as e:
        print(
            f"Scheduler check failed: {str(e)}"
        )

    finally:
        db.close()


def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        check_scheduled_reports,
        "interval",
        minutes=1,
        id="scheduled_reports_checker",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduled report scheduler started.")


def stop_scheduler():
    if not scheduler.running:
        return

    scheduler.shutdown()

    print("Scheduled report scheduler stopped.")