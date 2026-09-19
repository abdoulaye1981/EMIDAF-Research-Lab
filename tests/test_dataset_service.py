
from database.providers.sqlite_provider import SQLiteProvider
from database.database_manager import DatabaseManager

from database.models.workspace_model import WorkspaceModel
from database.models.project_model import ProjectModel
from database.models.dataset_model import DatasetModel

from emidaf_core.repositories.workspace_repository import WorkspaceRepository
from emidaf_core.repositories.project_repository import ProjectRepository
from emidaf_core.repositories.dataset_repository import DatasetRepository

from emidaf_core.services.dataset_service import DatasetService


def create_service():

    from pathlib import Path

    db_path = Path("database/test_emidaf.db")

    if db_path.exists():
        db_path.unlink()

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    workspace_repository = WorkspaceRepository(database)

    workspace = WorkspaceModel(
        name="Dataset Test Workspace",
        path=str(Path.cwd() / "dataset_test_workspace"),
        description="Workspace de test"
    )

    workspace = workspace_repository.add(workspace)

    project_repository = ProjectRepository(database)

    project = ProjectModel(
        workspace_id=workspace.id,
        name="Dataset Test Project",
        description="Projet de test"
    )

    project = project_repository.add(project)

    repository = DatasetRepository(database)

    service = DatasetService(repository)

    return service, project.id

def create_dataset(project_id, name="Dataset Test"):

    return DatasetModel(
        project_id=project_id,
        name=name,
        original_filename="test.csv",
        stored_filename="test_dataset.csv",
        extension=".csv",
        separator=",",
        encoding="utf-8",
        rows=10,
        columns=2,
        size=100
    )


def test_dataset_service_creation():

    service, project_id = create_service()

    assert service is not None
    assert project_id is not None


def test_count_datasets():

    service, project_id = create_service()

    assert service.count_datasets() >= 0


def test_get_all_datasets():

    service, project_id = create_service()

    datasets = service.get_all_datasets()

    assert isinstance(datasets, list)


def test_create_dataset():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "Dataset Create"
    )

    created = service.create_dataset(dataset)

    assert created is not None
    assert created.id is not None
    assert created.project_id == project_id
    assert created.name == "Dataset Create"


def test_get_dataset():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "Dataset Get"
    )

    created = service.create_dataset(dataset)

    result = service.get_dataset(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Dataset Get"


def test_dataset_exists():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "Dataset Exists"
    )

    created = service.create_dataset(dataset)

    assert service.dataset_exists(created.id)


def test_update_dataset():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "Dataset Before"
    )

    created = service.create_dataset(dataset)

    created.name = "Dataset After"

    updated = service.update_dataset(created)

    assert updated.name == "Dataset After"


def test_delete_dataset():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "Dataset Delete"
    )

    created = service.create_dataset(dataset)

    dataset_id = created.id

    assert service.dataset_exists(dataset_id)

    deleted = service.delete_dataset(dataset_id)

    assert deleted is True
    assert not service.dataset_exists(dataset_id)


def test_invalid_dataset_name():

    service, project_id = create_service()

    dataset = create_dataset(
        project_id,
        "   "
    )

    try:

        service.create_dataset(dataset)

        assert False

    except ValueError as error:

        assert "name" in str(error)


def test_invalid_dataset_path():

    service, project_id = create_service()

    dataset = DatasetModel(
        project_id=project_id,
        name="Invalid Path",
        original_filename="test.csv",
        stored_filename="dataset_without_extension",
        extension=".csv",
        rows=10,
        columns=2,
        size=100
    )

    try:

        service.create_dataset(dataset)

        assert False

    except ValueError as error:

        assert "extension" in str(error)
