from pathlib import Path
import shutil

from emidaf_core.builders.project_builder import ProjectBuilder
from emidaf_core.entities.project import Project
from emidaf_core.managers.workspace_manager import WorkspaceManager


def create_builder():

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

    return builder, project, project_path


def test_builder_creation():

    builder, _, _ = create_builder()

    assert builder is not None


def test_build_project():

    builder, project, project_path = create_builder()

    result = builder.build(project)

    assert result == project_path
    assert project_path.exists()
    assert project_path.is_dir()

    shutil.rmtree(project_path)


def test_project_structure():

    builder, project, project_path = create_builder()

    builder.build(project)

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
        "templates",
    ]

    for folder in folders:
        assert (project_path / folder).exists()
        assert (project_path / folder).is_dir()

    shutil.rmtree(project_path)


def test_readme_created():

    builder, project, project_path = create_builder()

    builder.build(project)

    readme = project_path / "README.md"

    assert readme.exists()
    assert readme.is_file()

    content = readme.read_text(encoding="utf-8")

    assert project.name in content
    assert project.author in content
    assert project.description in content

    shutil.rmtree(project_path)


def test_config_created():

    builder, project, project_path = create_builder()

    builder.build(project)

    config = project_path / "config.json"

    assert config.exists()
    assert config.is_file()

    shutil.rmtree(project_path)
