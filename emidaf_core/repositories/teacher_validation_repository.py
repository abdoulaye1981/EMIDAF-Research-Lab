"""
=========================================================
EMIDAF Framework v1.0
Teacher Validation Repository
=========================================================

Persistance des validations humaines des diagnostics
et prédictions produits par EMIDAF.
=========================================================
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import delete, func, select

from database.database_manager import DatabaseManager
from database.models.teacher_validation_model import (
    TeacherValidationModel,
)


class TeacherValidationRepository:
    """
    Repository des validations humaines.

    Contrairement à AnalysisResultRepository, aucune opération
    d'UPSERT n'est utilisée ici.

    Chaque validation est conservée afin de préserver
    l'historique scientifique et la traçabilité.
    """

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:

        self._database = database_manager

    # =====================================================
    # CREATE
    # =====================================================

    def add(
        self,
        validation: TeacherValidationModel,
    ) -> TeacherValidationModel:
        """
        Enregistre une nouvelle validation humaine.

        Une nouvelle ligne est systématiquement créée.
        Les validations antérieures ne sont jamais écrasées.
        """

        with self._database.session_scope() as session:

            session.add(validation)

            session.flush()
            session.refresh(validation)

            session.expunge(validation)

            return validation

    # =====================================================
    # GET BY ID
    # =====================================================

    def get_by_id(
        self,
        validation_id: int,
    ) -> Optional[TeacherValidationModel]:

        with self._database.session_scope() as session:

            validation = session.get(
                TeacherValidationModel,
                int(validation_id),
            )

            if validation is not None:
                session.expunge(validation)

            return validation

    # =====================================================
    # GET BY OBSERVATION
    # =====================================================

    def get_by_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> list[TeacherValidationModel]:
        """
        Retourne toutes les validations associées
        à une observation donnée.
        """

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.project_id
                    == int(project_id),

                    TeacherValidationModel.dataset_id
                    == int(dataset_id),

                    TeacherValidationModel.observation_id
                    == str(observation_id),
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
            )

            validations = list(
                session.scalars(statement).all()
            )

            for validation in validations:
                session.expunge(validation)

            return validations

    # =====================================================
    # GET LATEST BY OBSERVATION
    # =====================================================

    def get_latest_by_observation(
        self,
        project_id: int,
        dataset_id: int,
        observation_id: str,
    ) -> Optional[TeacherValidationModel]:
        """
        Retourne la validation la plus récente
        pour une observation.
        """

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.project_id
                    == int(project_id),

                    TeacherValidationModel.dataset_id
                    == int(dataset_id),

                    TeacherValidationModel.observation_id
                    == str(observation_id),
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
                .limit(1)
            )

            validation = session.scalar(statement)

            if validation is not None:
                session.expunge(validation)

            return validation

    # =====================================================
    # GET BY STUDENT
    # =====================================================

    def get_by_student(
        self,
        project_id: int,
        dataset_id: int,
        student_id: str,
    ) -> list[TeacherValidationModel]:
        """
        Retourne l'historique des validations
        associées à un élève.
        """

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.project_id
                    == int(project_id),

                    TeacherValidationModel.dataset_id
                    == int(dataset_id),

                    TeacherValidationModel.student_id
                    == str(student_id),
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
            )

            validations = list(
                session.scalars(statement).all()
            )

            for validation in validations:
                session.expunge(validation)

            return validations

    # =====================================================
    # GET BY VALIDATOR
    # =====================================================

    def get_by_validator(
        self,
        validator_user_id: int,
    ) -> list[TeacherValidationModel]:
        """
        Retourne les validations réalisées
        par un utilisateur EMIDAF donné.
        """

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.validator_user_id
                    == int(validator_user_id)
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
            )

            validations = list(
                session.scalars(statement).all()
            )

            for validation in validations:
                session.expunge(validation)

            return validations

    # =====================================================
    # GET BY DATASET
    # =====================================================

    def get_by_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> list[TeacherValidationModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.project_id
                    == int(project_id),

                    TeacherValidationModel.dataset_id
                    == int(dataset_id),
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
            )

            validations = list(
                session.scalars(statement).all()
            )

            for validation in validations:
                session.expunge(validation)

            return validations

    # =====================================================
    # GET BY PROJECT
    # =====================================================

    def get_by_project(
        self,
        project_id: int,
    ) -> list[TeacherValidationModel]:

        with self._database.session_scope() as session:

            statement = (
                select(TeacherValidationModel)
                .where(
                    TeacherValidationModel.project_id
                    == int(project_id)
                )
                .order_by(
                    TeacherValidationModel.created_at.desc()
                )
            )

            validations = list(
                session.scalars(statement).all()
            )

            for validation in validations:
                session.expunge(validation)

            return validations

    # =====================================================
    # COUNT
    # =====================================================

    def count(
        self,
        project_id: int,
        dataset_id: int,
    ) -> int:

        with self._database.session_scope() as session:

            statement = select(
                func.count(
                    TeacherValidationModel.id
                )
            ).where(
                TeacherValidationModel.project_id
                == int(project_id),

                TeacherValidationModel.dataset_id
                == int(dataset_id),
            )

            return int(
                session.scalar(statement) or 0
            )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        validation: TeacherValidationModel,
    ) -> TeacherValidationModel:
        """
        Met à jour une validation existante.

        À utiliser uniquement pour corriger une validation.
        Une nouvelle évaluation scientifique doit normalement
        être enregistrée avec add().
        """

        with self._database.session_scope() as session:

            validation = session.merge(validation)

            session.flush()
            session.refresh(validation)

            session.expunge(validation)

            return validation

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        validation_id: int,
    ) -> None:

        with self._database.session_scope() as session:

            statement = delete(
                TeacherValidationModel
            ).where(
                TeacherValidationModel.id
                == int(validation_id)
            )

            session.execute(statement)

    # =====================================================
    # DELETE DATASET
    # =====================================================

    def delete_dataset(
        self,
        project_id: int,
        dataset_id: int,
    ) -> None:

        with self._database.session_scope() as session:

            statement = delete(
                TeacherValidationModel
            ).where(
                TeacherValidationModel.project_id
                == int(project_id),

                TeacherValidationModel.dataset_id
                == int(dataset_id),
            )

            session.execute(statement)
