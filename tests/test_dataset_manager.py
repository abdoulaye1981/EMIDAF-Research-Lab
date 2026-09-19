from pathlib import Path
from uuid import uuid4

from database.database_manager import DatabaseManager
from database.models.dataset_model import DatasetModel
from database.models.project_model import ProjectModel
from database.models.workspace_model import WorkspaceModel
from database.providers.sqlite_provider import SQLiteProvider

from emidaf_core.managers.dataset_manager import DatasetManager
from emidaf_core.repositories.dataset_repository import DatasetRepository
from emidaf_core.repositories.project_repository import ProjectRepository
from emidaf_core.repositories.workspace_repository import WorkspaceRepository
from emidaf_core.services.dataset_service import DatasetService


def create_manager():

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    workspace_repository = WorkspaceRepository(database)

    workspace = WorkspaceModel(
        name=f"Manager Test Workspace {uuid4().hex}",
        path=str(
            Path.cwd()
            / f"manager_test_workspace_{uuid4().hex}"
        ),
        description="Workspace de test"
    )

    workspace = workspace_repository.add(workspace)

    project_repository = ProjectRepository(database)

    project = ProjectModel(
        workspace_id=workspace.id,
        name=f"Manager Test Project {uuid4().hex}",
        description="Projet de test"
    )

    project = project_repository.add(project)

    repository = DatasetRepository(database)

    service = DatasetService(repository)

    return DatasetManager(service), project.id


def create_dataset(
    project_id,
    name="Manager Dataset"
):

    return DatasetModel(
        project_id=project_id,
        name=name,
        original_filename="manager.csv",
        stored_filename="manager_dataset.csv",
        extension=".csv",
        separator=",",
        encoding="utf-8",
        rows=10,
        columns=2,
        size=100
    )


def test_manager_creation():

    manager, _ = create_manager()

    assert manager is not None


def test_manager_service():

    manager, _ = create_manager()

    assert manager.service is not None


def test_run_without_dataset():

    manager, _ = create_manager()

    result = manager.run()

    assert isinstance(result, list)


def test_create_dataset():

    manager, project_id = create_manager()

    dataset = create_dataset(project_id)

    created = manager.create(dataset)

    assert created is not None
    assert created.id is not None
    assert created.name == "Manager Dataset"


def test_run_with_dataset():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "Run Dataset"
    )

    created = manager.run(dataset)

    assert created is not None
    assert created.name == "Run Dataset"


def test_get_dataset():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "Get Dataset"
    )

    created = manager.create(dataset)

    result = manager.get(created.id)

    assert result is not None
    assert result.id == created.id


def test_get_all_datasets():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "All Dataset"
    )

    manager.create(dataset)

    result = manager.get_all()

    assert isinstance(result, list)


def test_exists():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "Exists Dataset"
    )

    created = manager.create(dataset)

    assert manager.exists(created.id)


def test_count():

    manager, project_id = create_manager()

    initial = manager.count()

    dataset = create_dataset(
        project_id,
        "Count Dataset"
    )

    manager.create(dataset)

    assert manager.count() == initial + 1


def test_update():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "Before Update"
    )

    created = manager.create(dataset)

    created.name = "After Update"

    updated = manager.update(created)

    assert updated.name == "After Update"


def test_delete():

    manager, project_id = create_manager()

    dataset = create_dataset(
        project_id,
        "Delete Dataset"
    )

    created = manager.create(dataset)

    dataset_id = created.id

    assert manager.exists(dataset_id)

    result = manager.delete(dataset_id)

    assert result is True
    assert not manager.exists(dataset_id)


def test_clear():

    manager, project_id = create_manager()

    manager.create(
        create_dataset(
            project_id,
            "Clear Dataset"
        )
    )

    manager.clear()

    assert manager.count() == 0
