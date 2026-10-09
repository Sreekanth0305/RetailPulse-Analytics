from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.config.database import Base


class WorkflowConfig(Base):

    __tablename__ = "workflow_configs"

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

    request_type = Column(
        String(100),
        nullable=False
    )

    approver_role = Column(
        String(50),
        nullable=False,
        default="Admin"
    )

    approval_required = Column(
        Boolean,
        default=True
    )

    allow_self_approval = Column(
        Boolean,
        default=False
    )

    is_active = Column(
        Boolean,
        default=True
    )