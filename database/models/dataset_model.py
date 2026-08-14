"""
=========================================================
EMIDAF Framework v1.0
Dataset ORM Model
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class DatasetModel(Base):
    """
    Modèle ORM représentant un jeu de données.
    """

    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    extension: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    separator: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default=","
    )

    encoding: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="utf-8"
    )

    rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    columns: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0
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
            f"DatasetModel("
            f"id={self.id}, "
            f"name='{self.name}')"
        )