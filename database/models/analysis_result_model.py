"""
=========================================================
EMIDAF Framework
Persistent Analysis Result Model
=========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class AnalysisResultModel(Base):
    """
    Résultat persistant d'une étape analytique EMIDAF.

    Un seul résultat courant est conservé pour le triplet :
    (project_id, dataset_id, stage).
    """

    __tablename__ = "analysis_results"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "dataset_id",
            "stage",
            name="uq_analysis_result_dataset_stage",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )

    stage: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    payload: Mapped[Any] = mapped_column(
        PickleType,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            "AnalysisResultModel("
            f"id={self.id}, "
            f"project_id={self.project_id}, "
            f"dataset_id={self.dataset_id}, "
            f"stage='{self.stage}')"
        )
