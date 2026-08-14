"""
=========================================================
EMIDAF Framework v1.0
Workspace Service
---------------------------------------------------------
Logique métier des espaces de travail.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import List
from typing import Optional

from database.models.workspace_model import WorkspaceModel
from emidaf_core.repositories.workspace_repository import WorkspaceRepository


class WorkspaceService:
    """
    Service métier des espaces de travail.
    """

    def __init__(self, repository: WorkspaceRepository):

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create_workspace(
        self,
        workspace: WorkspaceModel
    ) -> WorkspaceModel:

        self._validate(workspace)

        return self._repository.add(workspace)

    # =====================================================
    # READ
    # =====================================================

    def get_workspace(
        self,
        workspace_id: int
    ) -> Optional[WorkspaceModel]:

        return self._repository.get_by_id(workspace_id)

    def get_all_workspaces(self) -> List[WorkspaceModel]:

        return self._repository.get_all()

    def workspace_exists(
        self,
        workspace_id: int
    ) -> bool:

        return self._repository.exists(workspace_id)

    def count_workspaces(self) -> int:

        return self._repository.count()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_workspace(
        self,
        workspace: WorkspaceModel
    ) -> WorkspaceModel:

        self._validate(workspace)

        return self._repository.update(workspace)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_workspace(
        self,
        workspace_id: int
    ) -> bool:

        return self._repository.delete(workspace_id)

    def delete_all(self) -> None:

        self._repository.delete_all()

    # =====================================================
    # VALIDATION
    # =====================================================

    def _validate(
        self,
        workspace: WorkspaceModel
    ) -> None:

        if not workspace.name.strip():
            raise ValueError(
                "Workspace name cannot be empty."
            )

        if not workspace.path.strip():
            raise ValueError(
                "Workspace path cannot be empty."
            )

        path = Path(workspace.path)

        if not path.is_absolute():
            raise ValueError(
                "Workspace path must be absolute."
            )