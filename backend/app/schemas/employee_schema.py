from pydantic import BaseModel, EmailStr
from datetime import datetime


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: str
    phone: str


class EmployeeResponse(BaseModel):
    id: int
    company_id: int
    name: str
    email: EmailStr
    department: str
    designation: str
    phone: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True