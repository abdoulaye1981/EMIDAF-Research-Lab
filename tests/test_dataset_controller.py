from pathlib import Path

from database.providers.sqlite_provider import SQLiteProvider
from database.database_manager import DatabaseManager

from database.models.workspace_model import WorkspaceModel
from database.models.project_model import ProjectModel
from database.models.dataset_model import DatasetModel

from emidaf_core.repositories.workspace_repository import WorkspaceRepository
from emidaf_core.repositories.project_repository import ProjectRepository
from emidaf_core.repositories.dataset_repository import DatasetRepository

from emidaf_core.services.dataset_service import DatasetService
from emidaf_core.controllers.dataset_controller import DatasetController


def create_controller():

    db_path = Path("database/test_emidaf_controller.db")

    if db_path.exists():
        db_path.unlink()

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf_controller.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    workspace_repository = WorkspaceRepository(database)

    workspace = WorkspaceModel(
        name="Controller Test Workspace",
        path=str(Path.cwd() / "controller_dataset_workspace"),
        description="Workspace de test"
    )

    workspace = workspace_repository.add(workspace)

    project_repository = ProjectRepository(database)

    project = ProjectModel(
        workspace_id=workspace.id,
        name="Controller Test Project",
        description="Projet de test"
    )

    project = project_repository.add(project)

    repository = DatasetRepository(database)

    service = DatasetService(repository)

    controller = DatasetController(service)

    return controller, project.id


def create_dataset(project_id, name="Dataset Controller Test"):

    return DatasetModel(
        project_id=project_id,
        name=name,
        original_filename="controller.csv",
        stored_filename="controller_dataset.csv",
        extension=".csv",
        separator=",",
        encoding="utf-8",
        rows=10,
        columns=2,
        size=100
    )


def test_controller_creation():

    controller, _ = create_controller()

    assert controller is not None


def test_create():

    controller, project_id = create_controller()

    dataset = create_dataset(project_id)

    created = controller.create(dataset)

    assert created is not None
    assert created.id is not None
    assert created.name == "Dataset Controller Test"


def test_get():

    controller, project_id = create_controller()

    dataset = create_dataset(project_id)

    created = controller.create(dataset)

    result = controller.get(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == created.name


def test_get_all():

    controller, project_id = create_controller()

    dataset1 = controller.create(
        create_dataset(
            project_id,
            "Dataset 1"
        )
    )

    dataset2 = controller.create(
        create_dataset(
            project_id,
            "Dataset 2"
        )
    )

    datasets = controller.get_all()

    assert isinstance(datasets, list)
    assert len(datasets) == 2
    assert dataset1.id is not None
    assert dataset2.id is not None


def test_exists():

    controller, project_id = create_controller()

    dataset = controller.create(
        create_dataset(project_id)
    )

    assert controller.exists(dataset.id)


def test_count():

    controller, project_id = create_controller()

    controller.create(
        create_dataset(project_id, "Dataset 1")
    )

    controller.create(
        create_dataset(project_id, "Dataset 2")
    )

    assert controller.count() == 2


def test_update():

    controller, project_id = create_controller()

    dataset = controller.create(
        create_dataset(project_id)
    )

    dataset.name = "Dataset Updated"

    updated = controller.update(dataset)

    assert updated.name == "Dataset Updated"


def test_delete():

    controller, project_id = create_controller()

    dataset = controller.create(
        create_dataset(project_id)
    )

    dataset_id = dataset.id

    assert controller.exists(dataset_id)

    deleted = controller.delete(dataset_id)

    assert deleted is True
    assert not controller.exists(dataset_id)


def test_delete_all():

    controller, project_id = create_controller()

    controller.create(
        create_dataset(project_id, "Dataset 1")
    )

    controller.create(
        create_dataset(project_id, "Dataset 2")
    )

    assert controller.count() == 2

    controller.delete_all()

    assert controller.count() == 0
