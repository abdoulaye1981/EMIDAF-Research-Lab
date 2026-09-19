"""
=========================================================
EMIDAF Framework
Bootstrap
=========================================================
"""

from __future__ import annotations

from emidaf_core.container import Container


class Bootstrap:
    """
    Point d'entrée du Framework.

    Construit l'ensemble des composants
    de l'application.
    """

    def __init__(self):

        self._container = Container()

    @property
    def container(self) -> Container:

        return self._container

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> Container:

        self._load_configuration()

        self._create_database()

        self._create_managers()

        self._create_mappers()

        self._create_repositories()

        self._create_services()

        self._create_controllers()

        self._register_components()

        return self._container

    # =====================================================
    # PRIVATE
    # =====================================================

    def _load_configuration(self):
        from emidaf_core.managers.configuration_manager import ConfigurationManager

        self.configuration_manager = ConfigurationManager()
    def _create_database(self):
        from pathlib import Path

        from database.database_manager import DatabaseManager
        from database.providers.sqlite_provider import SQLiteProvider

        database_path = Path(
        self.configuration_manager.database
        )

        database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        provider = SQLiteProvider(
            f"sqlite:///{database_path}"
        )

        self.database_manager = DatabaseManager(provider)
        self.database_manager.create_database(database_path)

    def _create_managers(self):
        from emidaf_core.managers.workspace_manager import WorkspaceManager

        self.workspace_manager = WorkspaceManager()

    def _create_mappers(self):
        from emidaf_core.mappers.workspace_mapper import WorkspaceMapper
        from emidaf_core.mappers.project_mapper import ProjectMapper
        from emidaf_core.mappers.dataset_mapper import DatasetMapper

        self.workspace_mapper = WorkspaceMapper()
        self.project_mapper = ProjectMapper()
        self.dataset_mapper = DatasetMapper()

    def _create_repositories(self):
        from emidaf_core.repositories.workspace_repository import WorkspaceRepository
        from emidaf_core.repositories.project_repository import ProjectRepository
        from emidaf_core.repositories.dataset_repository import DatasetRepository

        self.workspace_repository = WorkspaceRepository(
             self.database_manager
        )

        self.project_repository = ProjectRepository(
             self.database_manager
        )

        self.dataset_repository = DatasetRepository(
             self.database_manager
        )

    def _create_services(self):
        from emidaf_core.services.workspace_service import WorkspaceService
        from emidaf_core.services.project_service import ProjectService
        from emidaf_core.services.dataset_service import DatasetService

        self.workspace_service = WorkspaceService(
             self.workspace_repository
        )

        self.project_service = ProjectService(
             self.project_repository
        )

        self.dataset_service = DatasetService(
             self.dataset_repository
        )

        from emidaf_core.managers.project_manager import ProjectManager
        from emidaf_core.managers.dataset_manager import DatasetManager

        self.project_manager = ProjectManager(
             self.project_service
        )

        self.dataset_manager = DatasetManager(
             self.dataset_service
        )

    def _create_controllers(self):
        from emidaf_core.controllers.workspace_controller import WorkspaceController
        from emidaf_core.controllers.project_controller import ProjectController
        from emidaf_core.controllers.dataset_controller import DatasetController

        self.workspace_controller = WorkspaceController(
             self.workspace_service
        )

        self.project_controller = ProjectController(
             self.project_service
        )

        self.dataset_controller = DatasetController(
             self.dataset_service
        )

    def _register_components(self):
      components = [
        self.configuration_manager,
        self.database_manager,
        self.workspace_manager,

        self.workspace_mapper,
        self.project_mapper,
        self.dataset_mapper,

        self.workspace_repository,
        self.project_repository,
        self.dataset_repository,

        self.workspace_service,
        self.project_service,
        self.dataset_service,

        self.project_manager,
        self.dataset_manager,

        self.workspace_controller,
        self.project_controller,
        self.dataset_controller,
      ]

      for component in components:
        self._container.register(component)
