from pathlib import Path
import shutil

from emidaf_core.builders.project_builder import ProjectBuilder
from emidaf_core.entities.project import Project
from emidaf_core.managers.workspace_manager import WorkspaceManager


def main():

    print()
    print("=" * 60)
    print("TEST PROJECT BUILDER")
    print("=" * 60)
    print()

    workspace_manager = WorkspaceManager()

    builder = ProjectBuilder(workspace_manager)

    project = Project(

        name="TEST_PROJECT",

        description="Projet de test",

        author="EMIDAF",

        workspace=str(
            workspace_manager.get_projects()
        )

    )

    project_path = workspace_manager.get_project_path(
        project.name
    )

    if project_path.exists():

        shutil.rmtree(project_path)

    builder.build(project)

    print("Projet créé :", project_path.exists())

    print()

    print("Structure créée")

    print("----------------")

    folders = [

        "config",

        "data",

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

        "figures",

        "logs",

        "metadata",

        "notebooks",

        "scripts"

    ]

    for folder in folders:

        exists = (project_path / folder).exists()

        print(f"{folder:<20} : {'OK' if exists else 'ERREUR'}")

    print()

    print("README.md :", (project_path / "README.md").exists())

    print("config.json :", (project_path / "config.json").exists())

    shutil.rmtree(project_path)

    print()

    print("Projet supprimé.")

    print()

    print("ProjectBuilder OK")


if __name__ == "__main__":

    main()