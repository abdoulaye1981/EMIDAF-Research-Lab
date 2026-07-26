from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime


from database.database import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False)

    description = Column(String(500))

    author = Column(String(200))

    created_at = Column(DateTime, default=datetime.now)

    updated_at = Column(DateTime, default=datetime.now)