from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database.database import Base


class ProjectModel(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False)

    description = Column(String(500))

    author = Column(String(200))

    created_at = Column(DateTime, default=datetime.now)

    updated_at = Column(DateTime, default=datetime.now)

# ==========================================================
# Dataset
# ==========================================================

class DatasetModel(Base):

    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True
    )

    project_id = Column(
        Integer,
        nullable=False
    )

    name = Column(
        String(200),
        nullable=False
    )

    original_filename = Column(
        String(255),
        nullable=False
    )

    stored_filename = Column(
        String(255),
        nullable=False
    )

    extension = Column(
        String(20),
        nullable=False
    )

    separator = Column(
        String(20),
        default=","
    )

    encoding = Column(
        String(50),
        default="utf-8"
    )

    rows = Column(
        Integer,
        default=0
    )

    columns = Column(
        Integer,
        default=0
    )

    size = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )