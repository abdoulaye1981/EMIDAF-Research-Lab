"""
=========================================================
EMIDAF Framework v1.0
Project Manager
---------------------------------------------------------
Gestion des projets
=========================================================
"""

from __future__ import annotations

from typing import List, Optional

from database.models.project_model import ProjectModel
from emidaf_core.services.project_service import ProjectService
from emidaf_core.core.base_manager import BaseManager

class ProjectManager(BaseManager):
    """
    Gestionnaire des projets.

    Le Manager constitue le point d'entrée
    du module Project.
    """

    def __init__(self, service: ProjectService) -> None:
        super().__init__(service)

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        project: Optional[ProjectModel] = None,
    ):
        """
        Exécute l'opération principale du manager.

        Sans projet : retourne la liste des projets.
        Avec projet : crée le projet.
        """

        if project is None:
            return self.get_all()

        return self.create(project)

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, project: ProjectModel) -> ProjectModel:
        return self.service.create_project(project)

    # =====================================================
    # READ
    # =====================================================

    def get(self, project_id: int) -> Optional[ProjectModel]:
        return self.service.get_project(project_id)

    def get_all(self) -> List[ProjectModel]:
        return self.service.get_all_projects()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, project: ProjectModel) -> ProjectModel:
        return self.service.update_project(project)

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, project_id: int) -> bool:
        return self.service.delete_project(project_id)

    def clear(self) -> None:
        self.service.delete_all()

    # =====================================================
    # SHORTCUTS
    # =====================================================

    def exists(self, project_id: int) -> bool:
        return self.service.project_exists(project_id)

    def count(self) -> int:
        return self.service.count_projects()
