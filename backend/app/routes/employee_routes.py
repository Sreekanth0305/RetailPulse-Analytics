from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.jwt import get_current_user

from app.config.roles import require_roles
from app.config.role_checker import require_roles

from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeResponse
)

from app.services.employee_service import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201
)
def add_employee(
    employee: EmployeeCreate,
    current_user=Depends(
        require_roles(
            "Company Admin",
            "Super Admin"
        )
    ),
    db: Session = Depends(get_db)
):

    return create_employee(
        db,
        employee,
        current_user.company_id
    )


@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_employees(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_all_employees(
        db,
        current_user.company_id
    )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_employee_by_id(
        db,
        employee_id,
        current_user.company_id
    )

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def edit_employee(
    employee_id: int,
    employee: EmployeeCreate,
    current_user=Depends(
        require_roles(
            "Company Admin",
            "Super Admin"
        )
    ),
    db: Session = Depends(get_db)
):

    return update_employee(
        db,
        employee_id,
        employee,
        current_user.company_id
    )

@router.delete(
    "/{employee_id}"
)
def remove_employee(
    employee_id: int,
    current_user=Depends(
        require_roles(
            "Company Admin",
            "Super Admin"
        )
    ),
    db: Session = Depends(get_db)
):

    return delete_employee(
        db,
        employee_id,
        current_user.company_id
    )