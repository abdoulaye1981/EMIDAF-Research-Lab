"""
=========================================================
EMIDAF Framework v1.0
Workspace ORM Model
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class WorkspaceModel(Base):
    """
    Modèle ORM représentant un espace de travail.
    """

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        default=""
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
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
            f"WorkspaceModel("
            f"id={self.id}, "
            f"name='{self.name}')"
        )