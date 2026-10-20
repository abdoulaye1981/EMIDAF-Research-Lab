"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Study Model
=========================================================

Décrit une étude quantitative de validation enseignante
Human-in-the-Loop.

Une étude fige notamment :
- le projet et le dataset ;
- le modèle évalué ;
- la cible ;
- le seuil ;
- le plan d'échantillonnage ;
- la graine aléatoire ;
- la taille prévue de l'échantillon.
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class TeacherValidationStudyModel(Base):

    __tablename__ = "teacher_validation_studies"

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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    target: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.5,
    )

    sampling_method: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="stratified_probability",
    )

    requested_sample_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    teachers_required: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    common_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    random_state: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=42,
    )

    sampling_config: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        index=True,
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            "TeacherValidationStudyModel("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"status='{self.status}', "
            f"model_name='{self.model_name}')"
        )
