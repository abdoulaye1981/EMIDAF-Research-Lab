"""
=========================================================
EMIDAF Framework v1.0
Workspace Controller
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from database.models.workspace_model import WorkspaceModel
from emidaf_core.services.workspace_service import WorkspaceService


class WorkspaceController:

    def __init__(self, service: WorkspaceService):

        self._service = service

    def create(self, workspace: WorkspaceModel) -> WorkspaceModel:

        return self._service.create_workspace(workspace)

    def get(self, workspace_id: int) -> Optional[WorkspaceModel]:

        return self._service.get_workspace(workspace_id)

    def get_all(self) -> List[WorkspaceModel]:

        return self._service.get_all_workspaces()

    def exists(self, workspace_id: int) -> bool:

        return self._service.workspace_exists(workspace_id)

    def count(self) -> int:

        return self._service.count_workspaces()

    def update(self, workspace: WorkspaceModel) -> WorkspaceModel:

        return self._service.update_workspace(workspace)

    def delete(self, workspace_id: int) -> bool:

        return self._service.delete_workspace(workspace_id)

    def delete_all(self) -> None:

        self._service.delete_all()