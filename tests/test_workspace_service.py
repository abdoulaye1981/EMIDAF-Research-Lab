from pathlib import Path

from database.providers.sqlite_provider import SQLiteProvider
from database.database_manager import DatabaseManager

from database.models.workspace_model import WorkspaceModel

from emidaf_core.repositories.workspace_repository import WorkspaceRepository
from emidaf_core.services.workspace_service import WorkspaceService


def create_service():

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    repository = WorkspaceRepository(database)

    repository.delete_all()

    return WorkspaceService(repository)


def test_workspace_service_creation():

    service = create_service()

    assert service is not None


def test_count_workspaces():

    service = create_service()

    assert service.count_workspaces() >= 0


def test_get_all_workspaces():

    service = create_service()

    workspaces = service.get_all_workspaces()

    assert isinstance(workspaces, list)


def test_create_workspace():

    service = create_service()

    workspace = WorkspaceModel(
        name="Test Workspace",
        path=str(Path.cwd() / "test_workspace"),
        description="Workspace de test"
    )

    created = service.create_workspace(workspace)

    assert created is not None
    assert created.id is not None
    assert created.name == "Test Workspace"


def test_get_workspace():

    service = create_service()

    workspace = WorkspaceModel(
        name="Workspace Get",
        path=str(Path.cwd() / "workspace_get"),
        description="Test"
    )

    created = service.create_workspace(workspace)

    result = service.get_workspace(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Workspace Get"


def test_workspace_exists():

    service = create_service()

    workspace = WorkspaceModel(
        name="Workspace Exists",
        path=str(Path.cwd() / "workspace_exists")
    )

    created = service.create_workspace(workspace)

    assert service.workspace_exists(created.id)


def test_update_workspace():

    service = create_service()

    workspace = WorkspaceModel(
        name="Workspace Before",
        path=str(Path.cwd() / "workspace_update")
    )

    created = service.create_workspace(workspace)

    created.name = "Workspace After"

    updated = service.update_workspace(created)

    assert updated.name == "Workspace After"


def test_delete_workspace():

    service = create_service()

    workspace = WorkspaceModel(
        name="Workspace Delete",
        path=str(Path.cwd() / "workspace_delete")
    )

    created = service.create_workspace(workspace)

    workspace_id = created.id

    assert service.workspace_exists(workspace_id)

    deleted = service.delete_workspace(workspace_id)

    assert deleted is True
    assert not service.workspace_exists(workspace_id)


def test_invalid_workspace_name():

    service = create_service()

    workspace = WorkspaceModel(
        name="   ",
        path=str(Path.cwd() / "workspace_invalid")
    )

    try:
        service.create_workspace(workspace)
        assert False
    except ValueError as error:
        assert "name" in str(error)


def test_invalid_workspace_path():

    service = create_service()

    workspace = WorkspaceModel(
        name="Invalid Path",
        path="relative/path"
    )

    try:
        service.create_workspace(workspace)
        assert False
    except ValueError as error:
        assert "absolute" in str(error)
