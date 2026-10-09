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


class WorkflowHistory(Base):

    __tablename__ = "workflow_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflow_requests.id"),
        nullable=False,
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
        nullable=False
    )

    action = Column(
        String(50),
        nullable=False
    )

    from_status = Column(
        String(30),
        nullable=True
    )

    to_status = Column(
        String(30),
        nullable=True
    )

    comment = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )