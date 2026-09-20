"""
=========================================================
EMIDAF Framework v1.0
Project Repository
---------------------------------------------------------
Gestion de la persistance des projets.
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy import select

from database.database_manager import DatabaseManager
from database.models.project_model import ProjectModel


class ProjectRepository:
    """
    Repository des projets.
    """

    def __init__(self, database_manager: DatabaseManager) -> None:

        self._database = database_manager

    # =====================================================
    # CREATE
    # =====================================================

    def add(self, project: ProjectModel) -> ProjectModel:

        with self._database.session_scope() as session:

            session.add(project)

            session.flush()

            session.refresh(project)

            return project

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(self, project_id: int) -> Optional[ProjectModel]:

        with self._database.session_scope() as session:

            return session.get(ProjectModel, project_id)

    def get_all(self) -> List[ProjectModel]:

        with self._database.session_scope() as session:

            statement = select(ProjectModel)

            return list(session.scalars(statement).all())

    def get_by_id_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> Optional[ProjectModel]:
        with self._database.session_scope() as session:
            statement = select(ProjectModel).where(
                ProjectModel.id == project_id,
                ProjectModel.user_id == user_id,
            )

            return session.scalar(statement)

    def get_all_for_user(
        self,
        user_id: int,
    ) -> List[ProjectModel]:
        with self._database.session_scope() as session:
            statement = (
                select(ProjectModel)
                .where(
                    ProjectModel.user_id == user_id
                )
                .order_by(
                    ProjectModel.created_at.desc()
                )
            )

            return list(
                session.scalars(statement).all()
            )

    def exists_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> bool:
        with self._database.session_scope() as session:
            statement = select(
                exists().where(
                    ProjectModel.id == project_id,
                    ProjectModel.user_id == user_id,
                )
            )

            return bool(
                session.scalar(statement)
            )

    def count_for_user(
        self,
        user_id: int,
    ) -> int:
        with self._database.session_scope() as session:
            statement = select(
                func.count(ProjectModel.id)
            ).where(
                ProjectModel.user_id == user_id
            )

            return int(
                session.scalar(statement) or 0
            )

    def delete_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> bool:
        with self._database.session_scope() as session:
            statement = select(ProjectModel).where(
                ProjectModel.id == project_id,
                ProjectModel.user_id == user_id,
            )

            project = session.scalar(statement)

            if project is None:
                return False

            session.delete(project)

            return True

    def exists(self, project_id: int) -> bool:

        with self._database.session_scope() as session:

            statement = select(
                exists().where(ProjectModel.id == project_id)
            )

            return bool(session.scalar(statement))

    def count(self) -> int:

        with self._database.session_scope() as session:

            statement = select(func.count(ProjectModel.id))

            return session.scalar(statement) or 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, project: ProjectModel) -> ProjectModel:

        with self._database.session_scope() as session:

            project = session.merge(project)

            session.flush()

            session.refresh(project)

            return project

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, project_id: int) -> bool:

        with self._database.session_scope() as session:

            project = session.get(ProjectModel, project_id)

            if project is None:
                return False

            session.delete(project)

            return True

    def delete_all(self) -> None:

        with self._database.session_scope() as session:

            session.execute(delete(ProjectModel))