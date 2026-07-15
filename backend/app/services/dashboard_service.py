from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_dashboard_data(db: Session, company_id: int):

    total_employees = db.query(Employee).filter(
        Employee.company_id == company_id
    ).count()

    active_employees = db.query(Employee).filter(
        Employee.company_id == company_id,
        Employee.status == "Active"
    ).count()

    departments = db.query(
        Employee.department
    ).filter(
        Employee.company_id == company_id
    ).distinct().count()

    attendance = 96

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "departments": departments,
        "attendance": attendance
    }