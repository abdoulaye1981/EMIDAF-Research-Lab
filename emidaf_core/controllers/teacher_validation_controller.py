"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Controller
=========================================================

Interface applicative entre EMIDAF Studio et le service
de validation humaine.
=========================================================
"""

from __future__ import annotations

from database.models.teacher_validation_model import (
    TeacherValidationModel,
)
from emidaf_core.services.teacher_validation_service import (
    TeacherValidationService,
)


class TeacherValidationController:
    """
    Contrôleur de validation humaine.
    """

    def __init__(
        self,
        service: TeacherValidationService,
    ) -> None:

        self._service = service

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        **kwargs,
    ) -> TeacherValidationModel:

        return self._service.create(
            **kwargs
        )

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        validation_id: int,
    ) -> TeacherValidationModel | None:

        return self._service.get(
            validation_id
        )

    def get_for_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> list[TeacherValidationModel]:

        return (
            self._service
            .get_for_observation(
                project_id,
                dataset_id,
                observation_id,
            )
        )

    def get_latest_for_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> TeacherValidationModel | None:

        return (
            self._service
            .get_latest_for_observation(
                project_id,
                dataset_id,
                observation_id,
            )
        )

    def get_for_student(
        self,
        project_id: int,
        dataset_id: int,
        student_id: str,
    ) -> list[TeacherValidationModel]:

        return (
            self._service
            .get_for_student(
                project_id,
                dataset_id,
                student_id,
            )
        )

    def get_for_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> list[TeacherValidationModel]:

        return (
            self._service
            .get_for_dataset(
                project_id,
                dataset_id,
            )
        )

    def count(
        self,
        project_id: int,
        dataset_id: int,
    ) -> int:

        return self._service.count(
            project_id,
            dataset_id,
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        validation: TeacherValidationModel,
    ) -> TeacherValidationModel:

        return self._service.update(
            validation
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        validation_id: int,
    ) -> None:

        self._service.delete(
            validation_id
        )
