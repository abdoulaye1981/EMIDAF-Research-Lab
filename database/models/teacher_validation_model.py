"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Model
=========================================================

Persistance de la validation humaine des résultats
produits par EMIDAF.
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


class TeacherValidationModel(Base):
    """
    Validation humaine d'une prédiction ou d'un diagnostic EMIDAF.
    """

    __tablename__ = "teacher_validations"

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

    validator_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    educational_teacher_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    task: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    target: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    threshold: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    predicted_class: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    predicted_probability: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Jugement humain indépendant du résultat EMIDAF.
    #
    # Valeurs attendues :
    # - difficulty
    # - no_difficulty
    # - not_evaluable
    teacher_detected_class: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )


    # =====================================================
    # HUMAN-IN-THE-LOOP
    # =====================================================

    # Degré de confiance du jugement indépendant :
    # 1 = très faible ; 5 = très élevé.
    teacher_confidence: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Commentaire produit AVANT révélation du modèle.
    teacher_initial_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Commentaire produit APRÈS révélation du modèle.
    teacher_post_model_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Raisons structurées d'un désaccord ou d'une réserve.
    disagreement_reasons: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # Etats possibles :
    # locked
    # model_revealed
    # completed
    validation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="completed",
    )

    # Instant où le jugement humain devient immuable.
    judgment_locked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Instant de première révélation du résultat algorithmique.
    model_revealed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Fin de la procédure de validation.
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    detection_validation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    diagnosis_validation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    difficulty_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    teacher_factors: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    teacher_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    algorithmic_diagnosis: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
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
            "TeacherValidationModel("
            f"id={self.id}, "
            f"project_id={self.project_id}, "
            f"dataset_id={self.dataset_id}, "
            f"observation_id='{self.observation_id}', "
            f"detection_validation='{self.detection_validation}')"
        )
