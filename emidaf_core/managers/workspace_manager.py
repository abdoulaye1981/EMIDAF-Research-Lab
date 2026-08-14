"""
=========================================================
EMIDAF Framework v1.0
Workspace Manager
---------------------------------------------------------
Gestion des espaces de travail et des projets EMIDAF
=========================================================
"""

from pathlib import Path
from typing import List, Optional
import shutil


class WorkspaceManager:
    """
    Gestionnaire du Workspace EMIDAF.

    Responsabilités
    ----------------
    - Initialiser le workspace
    - Gérer les projets
    - Gérer les archives
    - Gérer la corbeille
    - Fournir les chemins de travail
    """

    PROJECT_FOLDERS = [
        "config",
        "datasets",
        "exports",
        "logs",
        "metadata",
        "models",
        "notebooks",
        "reports",
        "scripts",
        "temp",
    ]

    def __init__(self, workspace: Optional[Path] = None):
        """
        Initialise le WorkspaceManager.
        """

        self.workspace = workspace or Path("workspace")

        self.projects = self.workspace / "projects"
        self.templates = self.workspace / "templates"
        self.archives = self.workspace / "archives"
        self.trash = self.workspace / "trash"

        self.current_project: Optional[Path] = None

        self.initialize()

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialise l'arborescence du workspace.
        """

        folders = [
            self.workspace,
            self.projects,
            self.templates,
            self.archives,
            self.trash,
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # ACCES
    # =====================================================

    def get_workspace(self) -> Path:
        return self.workspace

    def get_projects(self) -> Path:
        return self.projects

    def get_templates(self) -> Path:
        return self.templates

    def get_archives(self) -> Path:
        return self.archives

    def get_trash(self) -> Path:
        return self.trash

    # =====================================================
    # INFORMATIONS
    # =====================================================

    def project_exists(self, project_name: str) -> bool:
        """
        Vérifie si un projet existe.
        """
        return (self.projects / project_name).exists()

    def get_project_path(self, project_name: str) -> Path:
        """
        Retourne le chemin d'un projet.
        """
        return self.projects / project_name

    def list_projects(self) -> List[str]:
        """
        Retourne la liste des projets.
        """
        return sorted(
            [
                folder.name
                for folder in self.projects.iterdir()
                if folder.is_dir()
            ]
        )

    def count_projects(self) -> int:
        """
        Retourne le nombre de projets.
        """
        return len(self.list_projects())

    # =====================================================
    # CREATION
    # =====================================================

    def create_project(self, project_name: str) -> bool:
        """
        Crée un nouveau projet.
        """

        project_path = self.projects / project_name

        if project_path.exists():
            return False

        project_path.mkdir(parents=True)

        for folder in self.PROJECT_FOLDERS:
            (project_path / folder).mkdir(exist_ok=True)

        return True

    # =====================================================
    # RENOMMAGE
    # =====================================================

    def rename_project(
        self,
        old_name: str,
        new_name: str,
    ) -> bool:
        """
        Renomme un projet.
        """

        old_path = self.projects / old_name
        new_path = self.projects / new_name

        if not old_path.exists():
            return False

        if new_path.exists():
            return False

        old_path.rename(new_path)

        if self.current_project == old_path:
            self.current_project = new_path

        return True

    # =====================================================
    # DUPLICATION
    # =====================================================

    def duplicate_project(
        self,
        project_name: str,
        new_name: str,
    ) -> bool:
        """
        Duplique un projet.
        """

        source = self.projects / project_name
        destination = self.projects / new_name

        if not source.exists():
            return False

        if destination.exists():
            return False

        shutil.copytree(source, destination)

        return True

    # =====================================================
    # ARCHIVAGE
    # =====================================================

    def archive_project(
        self,
        project_name: str,
    ) -> bool:
        """
        Archive un projet.
        """

        source = self.projects / project_name
        destination = self.archives / project_name

        if not source.exists():
            return False

        if destination.exists():
            return False

        source.rename(destination)

        if self.current_project == source:
            self.current_project = None

        return True

    # =====================================================
    # RESTAURATION
    # =====================================================

    def restore_project(
        self,
        project_name: str,
    ) -> bool:
        """
        Restaure un projet depuis les archives
        ou la corbeille.
        """

        archive = self.archives / project_name
        trash = self.trash / project_name
        destination = self.projects / project_name

        if destination.exists():
            return False

        if archive.exists():
            archive.rename(destination)
            return True

        if trash.exists():
            trash.rename(destination)
            return True

        return False

    # =====================================================
    # CORBEILLE
    # =====================================================

    def move_to_trash(
        self,
        project_name: str,
    ) -> bool:
        """
        Déplace un projet dans la corbeille.
        """

        source = self.projects / project_name
        destination = self.trash / project_name

        if not source.exists():
            return False

        if destination.exists():
            shutil.rmtree(destination)

        source.rename(destination)

        if self.current_project == source:
            self.current_project = None

        return True

    # =====================================================
    # SUPPRESSION
    # =====================================================

    def delete_project(
        self,
        project_name: str,
    ) -> bool:
        """
        Effectue une suppression logique.
        """

        return self.move_to_trash(project_name)