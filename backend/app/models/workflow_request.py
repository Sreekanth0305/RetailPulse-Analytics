from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.sql import func

from app.config.database import Base


class WorkflowRequest(Base):

    __tablename__ = "workflow_requests"

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

    requested_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    approver_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    request_type = Column(
        String(100),
        nullable=False,
        index=True
    )

    related_record = Column(
        String(255),
        nullable=True
    )

    requested_changes = Column(
        JSON,
        nullable=True
    )

    reason = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(20),
        default="Normal"
    )

    status = Column(
        String(30),
        default="Draft",
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )