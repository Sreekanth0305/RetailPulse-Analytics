from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text
)
from sqlalchemy.sql import func

from app.config.database import Base


class Notification(Base):

    __tablename__ = "notifications"

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
        nullable=True,
        index=True
    )

    type = Column(
        String(50),
        nullable=False,
        index=True
    )

    title = Column(
        String(100),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    priority = Column(
        String(20),
        nullable=False,
        default="Medium",
        index=True
    )

    resource_type = Column(
        String(100),
        nullable=True,
        index=True
    )

    resource_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True
    )

    read_at = Column(
        DateTime,
        nullable=True
    )

    expires_at = Column(
        DateTime,
        nullable=True,
        index=True
    )

    deduplication_key = Column(
        String(255),
        nullable=True,
        index=True
    )