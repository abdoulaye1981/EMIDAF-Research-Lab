"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Assignment Model
=========================================================

Affectation d'un cas HITL à un enseignant évaluateur.
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class TeacherValidationAssignmentModel(Base):

    __tablename__ = "teacher_validation_assignments"

    __table_args__ = (
        UniqueConstraint(
            "study_id",
            "case_id",
            "teacher_user_id",
            name="uq_teacher_validation_assignment",
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

    case_id: Mapped[int] = mapped_column(
        ForeignKey("teacher_validation_cases.id"),
        nullable=False,
        index=True,
    )

    teacher_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    validation_id: Mapped[int | None] = mapped_column(
        ForeignKey("teacher_validations.id"),
        nullable=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            "TeacherValidationAssignmentModel("
            f"id={self.id}, "
            f"study_id={self.study_id}, "
            f"case_id={self.case_id}, "
            f"teacher_user_id={self.teacher_user_id}, "
            f"status='{self.status}')"
        )
