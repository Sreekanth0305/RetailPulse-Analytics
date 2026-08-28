from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.config.database import Base


class ImportErrorRecord(Base):

    __tablename__ = "import_errors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    import_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    row_number = Column(
        Integer,
        nullable=False
    )

    error_type = Column(
        String(50),
        nullable=False
    )

    error_message = Column(
        Text,
        nullable=False
    )

    row_data = Column(
        Text,
        nullable=True
    )