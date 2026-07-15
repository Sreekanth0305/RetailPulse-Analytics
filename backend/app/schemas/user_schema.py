from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    company_id: int
    name: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    company_id: int
    name: str
    email: EmailStr
    role: str
    status: str
    last_login: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):

    name: str
    email: EmailStr
    role: str
    company: str
    last_login: datetime | None
    status: str

    class Config:
        from_attributes = True    