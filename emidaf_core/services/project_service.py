from pathlib import Path
import json

from emidaf_core.entities.project import Project
from emidaf_core.repositories.project_repository import ProjectRepository


class ProjectService:

    def __init__(self):

        self.repository = ProjectRepository()

    # =======================================
    # Création d'un projet
    # =======================================

    def create_project(
        self,
        name,
        description,
        author,
        workspace
    ):

        project = Project(
            name=name,
            description=description,
            author=author,
            workspace=workspace
        )

        project_path = self._create_project_directory(
            workspace,
            name
        )

        self._create_subdirectories(project_path)

        self._create_config_file(
            project,
            project_path
        )

        self._create_readme(
            project,
            project_path
        )

        return self.repository.create(project)

    # =======================================
    # Création du dossier principal
    # =======================================

    def _create_project_directory(
        self,
        workspace,
        project_name
    ):

        project_path = Path(workspace) / project_name

        if project_path.exists():
            raise FileExistsError(
                f"Le projet '{project_name}' existe déjà."
            )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return project_path

    # =======================================
    # Création des sous-dossiers
    # =======================================

    def _create_subdirectories(self, project_path):

        folders = [

            "config",

            "data/raw",

            "data/processed",

            "data/external",

            "data/exports",

            "models",

            "reports",

            "figures",

            "logs",

            "notebooks",

            "scripts"

        ]

        for folder in folders:

            (project_path / folder).mkdir(
                parents=True,
                exist_ok=True
            )

    # =======================================
    # Création du fichier config.json
    # =======================================

    def _create_config_file(
        self,
        project,
        project_path
    ):

        config = {

            "project_name": project.name,

            "author": project.author,

            "description": project.description,

            "version": "1.0",

            "created_at": str(project.created_at),

            "status": "NEW"

        }

        with open(
            project_path / "config.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =======================================
    # Création du README
    # =======================================

    def _create_readme(
        self,
        project,
        project_path
    ):

        content = f"""# {project.name}

Created with EMIDAF Research Lab

Author

{project.author}

Description

{project.description}
"""

        with open(
            project_path / "README.md",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

    # =======================================
    # Récupération de tous les projets
    # =======================================

    def get_projects(self):

        return self.repository.get_all()