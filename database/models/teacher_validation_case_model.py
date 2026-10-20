"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Case Model
=========================================================

Observation sélectionnée dans un échantillon expert HITL.

La prédiction est figée au moment de l'échantillonnage
afin de préserver la reproductibilité scientifique.
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class TeacherValidationCaseModel(Base):

    __tablename__ = "teacher_validation_cases"

    __table_args__ = (
        UniqueConstraint(
            "study_id",
            "observation_id",
            name="uq_teacher_validation_case_study_observation",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    study_id: Mapped[int] = mapped_column(
        ForeignKey("teacher_validation_studies.id"),
        nullable=False,
        index=True,
    )

    observation_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    student_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    predicted_class: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    predicted_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    probability_band: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    distance_to_threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        index=True,
    )

    sampling_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_common: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    prediction_snapshot: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            "TeacherValidationCaseModel("
            f"id={self.id}, "
            f"study_id={self.study_id}, "
            f"observation_id='{self.observation_id}', "
            f"probability={self.predicted_probability})"
        )
