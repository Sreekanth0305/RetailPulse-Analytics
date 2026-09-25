from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from app.config.database import Base


class ReconciliationHistory(Base):
    __tablename__ = "reconciliation_history"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    execution_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    started_at = Column(
        DateTime,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    triggered_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    records_checked = Column(
        Integer,
        default=0
    )

    issues_detected = Column(
        Integer,
        default=0
    )

    issues_resolved = Column(
        Integer,
        default=0
    )

    failed_checks = Column(
        Integer,
        default=0
    )

    execution_status = Column(
        String(40),
        nullable=False,
        default="Running"
    )

    error_message = Column(
        String(1000),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )