from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.config.database import Base


class ReportHistory(Base):

    __tablename__ = "report_history"

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
        nullable=False,
        index=True
    )

    filters = Column(
        Text,
        nullable=True
    )

    export_format = Column(
        String(20),
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="Success",
        index=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    generated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True
    )