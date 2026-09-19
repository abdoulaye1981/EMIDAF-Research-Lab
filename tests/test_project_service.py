from database.providers.sqlite_provider import SQLiteProvider
from database.database_manager import DatabaseManager

from emidaf_core.repositories.project_repository import ProjectRepository
from emidaf_core.services.project_service import ProjectService


def create_service():

    provider = SQLiteProvider(
        "sqlite:///database/test_emidaf.db"
    )

    database = DatabaseManager(provider)

    database.create_tables()

    repository = ProjectRepository(database)

    return ProjectService(repository)


def test_project_service_creation():

    service = create_service()

    assert service is not None


def test_project_service_count():

    service = create_service()

    assert service.count_projects() >= 0


def test_get_all_projects():

    service = create_service()

    projects = service.get_all_projects()

    assert isinstance(projects, list)
