from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee_schema import EmployeeCreate


def create_employee(
    db: Session,
    employee: EmployeeCreate,
    company_id: int
):

    existing_employee = (
        db.query(Employee)
        .filter(Employee.email == employee.email)
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee already exists."
        )

    db_employee = Employee(
        company_id=company_id,
        name=employee.name,
        email=employee.email,
        department=employee.department,
        designation=employee.designation,
        phone=employee.phone,
        status="Active"
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_all_employees(
    db: Session,
    company_id: int
):

    return (
        db.query(Employee)
        .filter(Employee.company_id == company_id)
        .all()
    )

def get_employee_by_id(
    db: Session,
    employee_id: int,
    company_id: int
):

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id,
            Employee.company_id == company_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    return employee

def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeCreate,
    company_id: int
):

    employee = get_employee_by_id(
        db,
        employee_id,
        company_id
    )

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department = employee_data.department
    employee.designation = employee_data.designation
    employee.phone = employee_data.phone

    db.commit()
    db.refresh(employee)

    return employee

def delete_employee(
    db: Session,
    employee_id: int,
    company_id: int
):

    employee = get_employee_by_id(
        db,
        employee_id,
        company_id
    )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully."
    }