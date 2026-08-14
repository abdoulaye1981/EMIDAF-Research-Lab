"""
=========================================================
EMIDAF Framework v1.0
Project ORM Model
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class ProjectModel(Base):
    """
    Modèle ORM représentant un projet.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self) -> str:

        return (
            f"ProjectModel("
            f"id={self.id}, "
            f"name='{self.name}')"
        )