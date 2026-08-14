"""
=========================================================
EMIDAF Framework v1.0
Project Service
---------------------------------------------------------
Logique métier des projets.
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from database.models.project_model import ProjectModel
from emidaf_core.repositories.project_repository import ProjectRepository


class ProjectService:
    """
    Service métier des projets.
    """

    def __init__(self, repository: ProjectRepository):

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create_project(
        self,
        project: ProjectModel
    ) -> ProjectModel:

        self._validate(project)

        return self._repository.add(project)

    # =====================================================
    # READ
    # =====================================================

    def get_project(
        self,
        project_id: int
    ) -> Optional[ProjectModel]:

        return self._repository.get_by_id(project_id)

    def get_all_projects(self) -> List[ProjectModel]:

        return self._repository.get_all()

    def project_exists(
        self,
        project_id: int
    ) -> bool:

        return self._repository.exists(project_id)

    def count_projects(self) -> int:

        return self._repository.count()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_project(
        self,
        project: ProjectModel
    ) -> ProjectModel:

        self._validate(project)

        return self._repository.update(project)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_project(
        self,
        project_id: int
    ) -> bool:

        return self._repository.delete(project_id)

    def delete_all(self) -> None:

        self._repository.delete_all()

    # =====================================================
    # VALIDATION
    # =====================================================

    def _validate(
        self,
        project: ProjectModel
    ) -> None:

        if not project.name.strip():

            raise ValueError(
                "Project name cannot be empty."
            )

        if project.workspace_id <= 0:

            raise ValueError(
                "Invalid workspace identifier."
            )