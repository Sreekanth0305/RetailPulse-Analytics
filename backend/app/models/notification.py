from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from app.config.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    title = Column(String(100), nullable=False)

    message = Column(String(255), nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=func.now()
    )