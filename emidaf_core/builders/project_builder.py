from pathlib import Path
import json
from datetime import datetime

from emidaf_core.entities.project import Project
from emidaf_core.managers.workspace_manager import WorkspaceManager


class ProjectBuilder:

    def __init__(self, workspace_manager):

        self.workspace_manager = workspace_manager

    # ==========================================================
    # Construction d'un projet
    # ==========================================================

    def build(self, project: Project):

        workspace = self.workspace_manager.get_projects()

        project_path = workspace / project.name

        project_path.mkdir(
            parents=True,
            exist_ok=False
        )

        self._create_structure(project_path)

        self._create_readme(
            project_path,
            project
        )

        self._create_config(
            project_path,
            project
        )

        return project_path

    # ==========================================================
    # Structure du projet
    # ==========================================================

    def _create_structure(self, project_path):

        folders = [

            "config",

            "data",

            "data/raw",

            "data/processed",

            "data/external",

            "data/exports",

            "datasets",

            "inspection",

            "eidpp",

            "elae",

            "ekde",

            "eaie",

            "exaie",

            "edse",

            "models",

            "reports",

            "reports/pdf",

            "reports/html",

            "reports/docx",

            "figures",

            "logs",

            "metadata",

            "notebooks",

            "scripts",

            "exports",

            "templates"

        ]

        for folder in folders:

            (project_path / folder).mkdir(
                parents=True,
                exist_ok=True
            )

    # ==========================================================
    # README
    # ==========================================================

    def _create_readme(self, path, project):

        content = f"""# {project.name}

Projet créé avec EMIDAF Research Lab

Auteur : {project.author}

Description :

{project.description}
"""

        (path / "README.md").write_text(
            content,
            encoding="utf-8"
        )

    # ==========================================================
    # config.json
    # ==========================================================

    def _create_config(self, path, project):

        config = {

            "name": project.name,

            "author": project.author,

            "description": project.description,

            "created_at": datetime.now().isoformat(),

            "version": "1.0.0",

            "framework": "EMIDAF Research Lab"

        }

        with open(

            path / "config.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                config,

                file,

                indent=4,

                ensure_ascii=False

            )