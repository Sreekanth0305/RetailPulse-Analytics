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


class DataQualityIssue(Base):
    __tablename__ = "data_quality_issues"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )

    issue_type = Column(String(100), nullable=False, index=True)

    severity = Column(
        String(20),
        nullable=False,
        default="Warning",
        index=True
    )

    module = Column(
        String(50),
        nullable=False,
        index=True
    )

    affected_record = Column(String(100), nullable=True)

    description = Column(Text, nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="Open",
        index=True
    )

    detected_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    resolved_at = Column(DateTime, nullable=True)

    resolved_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    resolution_note = Column(Text, nullable=True)

    previous_status = Column(String(30), nullable=True)

    new_status = Column(String(30), nullable=True)

    # Used to prevent duplicate unresolved issues
    issue_key = Column(
        String(255),
        nullable=False,
        index=True
    )