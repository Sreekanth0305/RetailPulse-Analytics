from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.config.database import Base


class ScheduledReport(Base):

    __tablename__ = "scheduled_reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    report_type = Column(
        String(100),
        nullable=False
    )

    filters = Column(
        Text,
        nullable=True
    )

    frequency = Column(
        String(20),
        nullable=False
    )

    execution_time = Column(
        String(10),
        nullable=False
    )

    recipients = Column(
        Text,
        nullable=False
    )

    export_format = Column(
        String(20),
        nullable=False
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )

    last_run_at = Column(
        DateTime,
        nullable=True
    )

    last_run_status = Column(
        String(30),
        nullable=True
    )

    last_error_message = Column(
        Text,
        nullable=True
    )

    next_run_at = Column(
        DateTime,
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )