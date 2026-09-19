from pathlib import Path

from database.database_manager import DatabaseManager
from database.models.project_model import ProjectModel
from database.models.workspace_model import WorkspaceModel
from database.providers.sqlite_provider import SQLiteProvider

from emidaf_core.managers.project_manager import ProjectManager
from emidaf_core.repositories.project_repository import ProjectRepository
from emidaf_core.repositories.workspace_repository import WorkspaceRepository
from emidaf_core.services.project_service import ProjectService


def create_manager():

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    workspace_repository = WorkspaceRepository(database)

    workspace = WorkspaceModel(
       name="Project Manager Workspace",
       path=str(
           Path.cwd()
           / f"project_manager_workspace_{__import__('uuid').uuid4().hex}"
       ),
       description="Workspace de test"
    )
    workspace = workspace_repository.add(workspace)

    repository = ProjectRepository(database)

    service = ProjectService(repository)

    return ProjectManager(service), workspace.id


def create_project(
    workspace_id,
    name="Manager Project"
):

    return ProjectModel(
        workspace_id=workspace_id,
        name=name,
        description="Projet de test"
    )


def test_manager_creation():

    manager, _ = create_manager()

    assert manager is not None


def test_manager_service():

    manager, _ = create_manager()

    assert manager.service is not None


def test_run_without_project():

    manager, _ = create_manager()

    result = manager.run()

    assert isinstance(result, list)


def test_create_project():

    manager, workspace_id = create_manager()

    project = create_project(workspace_id)

    created = manager.create(project)

    assert created is not None
    assert created.id is not None
    assert created.name == "Manager Project"


def test_run_with_project():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "Run Project"
    )

    created = manager.run(project)

    assert created is not None
    assert created.name == "Run Project"


def test_get_project():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "Get Project"
    )

    created = manager.create(project)

    result = manager.get(created.id)

    assert result is not None
    assert result.id == created.id


def test_get_all_projects():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "All Project"
    )

    manager.create(project)

    result = manager.get_all()

    assert isinstance(result, list)


def test_exists():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "Exists Project"
    )

    created = manager.create(project)

    assert manager.exists(created.id)


def test_count():

    manager, workspace_id = create_manager()

    initial = manager.count()

    project = create_project(
        workspace_id,
        "Count Project"
    )

    manager.create(project)

    assert manager.count() == initial + 1


def test_update():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "Before Update"
    )

    created = manager.create(project)

    created.name = "After Update"

    updated = manager.update(created)

    assert updated.name == "After Update"


def test_delete():

    manager, workspace_id = create_manager()

    project = create_project(
        workspace_id,
        "Delete Project"
    )

    created = manager.create(project)

    project_id = created.id

    assert manager.exists(project_id)

    result = manager.delete(project_id)

    assert result is True
    assert not manager.exists(project_id)


def test_clear():

    manager, workspace_id = create_manager()

    manager.create(
        create_project(
            workspace_id,
            "Clear Project"
        )
    )

    manager.clear()

    assert manager.count() == 0
