"""
=========================================================
EMIDAF Framework v1.0
Workspace Repository
---------------------------------------------------------
Gestion de la persistance des espaces de travail.
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
from database.models.workspace_model import WorkspaceModel


class WorkspaceRepository:
    """
    Repository des espaces de travail.

    Responsabilités
    ----------------
    - Ajouter un workspace
    - Rechercher un workspace
    - Modifier un workspace
    - Supprimer un workspace
    - Lister les workspaces

    Aucune logique métier.
    """

    def __init__(self, database_manager: DatabaseManager) -> None:

        self._database = database_manager

    # =====================================================
    # CREATE
    # =====================================================

    def add(self, workspace: WorkspaceModel) -> WorkspaceModel:

        with self._database.session_scope() as session:

            session.add(workspace)

            session.flush()

            session.refresh(workspace)

            return workspace

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(self, workspace_id: int) -> Optional[WorkspaceModel]:

        with self._database.session_scope() as session:

            return session.get(WorkspaceModel, workspace_id)

    def get_all(self) -> List[WorkspaceModel]:

        with self._database.session_scope() as session:

            statement = select(WorkspaceModel)

            return list(session.scalars(statement).all())

    def exists(self, workspace_id: int) -> bool:

        with self._database.session_scope() as session:

            statement = select(
                exists().where(WorkspaceModel.id == workspace_id)
            )

            return bool(session.scalar(statement))

    def count(self) -> int:

        with self._database.session_scope() as session:

            statement = select(func.count(WorkspaceModel.id))

            return session.scalar(statement) or 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, workspace: WorkspaceModel) -> WorkspaceModel:

        with self._database.session_scope() as session:

            workspace = session.merge(workspace)

            session.flush()

            session.refresh(workspace)

            return workspace

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, workspace_id: int) -> bool:

        with self._database.session_scope() as session:

            workspace = session.get(WorkspaceModel, workspace_id)

            if workspace is None:
                return False

            session.delete(workspace)

            return True

    def delete_all(self) -> None:

        with self._database.session_scope() as session:

            session.execute(delete(WorkspaceModel))