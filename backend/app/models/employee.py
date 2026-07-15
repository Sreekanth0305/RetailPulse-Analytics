from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.config.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    department = Column(String(100))

    designation = Column(String(100))

    phone = Column(String(20))

    status = Column(
        String(20),
        default="Active"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )