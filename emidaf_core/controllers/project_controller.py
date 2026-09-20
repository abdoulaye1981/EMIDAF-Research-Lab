"""
=========================================================
EMIDAF Framework v1.0
Project Controller
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from database.models.project_model import ProjectModel
from emidaf_core.services.project_service import ProjectService


class ProjectController:

    def __init__(self, service: ProjectService):

        self._service = service

    def create(self, project: ProjectModel) -> ProjectModel:

        return self._service.create_project(project)

    def get(self, project_id: int) -> Optional[ProjectModel]:

        return self._service.get_project(project_id)

    def get_all(self) -> List[ProjectModel]:

        return self._service.get_all_projects()

    def get_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> Optional[ProjectModel]:
        return self._service.get_project_for_user(
            project_id,
            user_id,
        )

    def get_all_for_user(
        self,
        user_id: int,
    ) -> List[ProjectModel]:
        return self._service.get_all_projects_for_user(
            user_id
        )

    def exists_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> bool:
        return self._service.project_exists_for_user(
            project_id,
            user_id,
        )

    def count_for_user(
        self,
        user_id: int,
    ) -> int:
        return self._service.count_projects_for_user(
            user_id
        )

    def delete_for_user(
        self,
        project_id: int,
        user_id: int,
    ) -> bool:
        return self._service.delete_project_for_user(
            project_id,
            user_id,
        )

    def exists(self, project_id: int) -> bool:

        return self._service.project_exists(project_id)

    def count(self) -> int:

        return self._service.count_projects()

    def update(self, project: ProjectModel) -> ProjectModel:

        return self._service.update_project(project)

    def delete(self, project_id: int) -> bool:

        return self._service.delete_project(project_id)

    def delete_all(self) -> None:

        self._service.delete_all()