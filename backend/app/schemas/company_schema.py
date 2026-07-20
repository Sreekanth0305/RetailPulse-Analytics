from pydantic import BaseModel, EmailStr
from datetime import datetime


class CompanyCreateSchema(BaseModel):
    # Company Details
    name: str
    industry: str
    email: EmailStr
    address: str
    phone: str
    role: str 

    # First Admin Details
    admin_name: str
    admin_email: EmailStr
    admin_password: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: str
    email: EmailStr
    address: str
    phone: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class CompanyRegisterResponse(BaseModel):
    message: str
    company_id: int
    admin_email: EmailStr