from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    industry = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    address = Column(String(255), nullable=False)

    phone = Column(String(20), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship(
        "User",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    # employees = relationship(
    #     "Employee",
    #     back_populates="company"
    #     cascade="all, delete-orphan"
    # )

    audit_logs = relationship(
        "AuditLog",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    categories = relationship(
    "Category",
    back_populates="company",
    cascade="all, delete-orphan"
    )
    
    products = relationship(
        "Product",
        back_populates="company",
        cascade="all, delete-orphan"
    )