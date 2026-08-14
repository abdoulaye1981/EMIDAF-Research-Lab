"""
=========================================================
EMIDAF Framework v1.0
Bootstrap
---------------------------------------------------------
Initialisation complète du Framework
=========================================================
"""

from __future__ import annotations

from emidaf_core.registry import Registry

from emidaf_core.managers.configuration_manager import ConfigurationManager
from emidaf_core.managers.dataset_manager import DatasetManager
from emidaf_core.managers.event_manager import EventManager
from emidaf_core.managers.logger_manager import LoggerManager
from emidaf_core.managers.navigation_manager import NavigationManager
from emidaf_core.managers.resource_manager import ResourceManager
from emidaf_core.managers.session_manager import SessionManager
from emidaf_core.managers.theme_manager import ThemeManager
from emidaf_core.managers.workspace_manager import WorkspaceManager


class Bootstrap:
    """
    Point d'entrée du Framework EMIDAF.
    """

    def __init__(self):

        self.registry = Registry()

    # =====================================================
    # PUBLIC
    # =====================================================

    def initialize(self):

        self._create_managers()

        self._initialize_managers()

        self._register_components()

        return self.registry

    # =====================================================
    # MANAGERS
    # =====================================================

    def _create_managers(self):

        self.configuration_manager = ConfigurationManager()

        self.logger_manager = LoggerManager()

        self.workspace_manager = WorkspaceManager()

        self.dataset_manager = DatasetManager()

        self.navigation_manager = NavigationManager()

        self.resource_manager = ResourceManager()

        self.session_manager = SessionManager()

        self.theme_manager = ThemeManager()

        self.event_manager = EventManager()

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def _initialize_managers(self):

        managers = [

            self.configuration_manager,

            self.logger_manager,

            self.workspace_manager,

            self.dataset_manager,

            self.navigation_manager,

            self.resource_manager,

            self.session_manager,

            self.theme_manager,

            self.event_manager

        ]

        for manager in managers:

            if hasattr(manager, "initialize"):

                manager.initialize()

    # =====================================================
    # REGISTRY
    # =====================================================

    def _register_components(self):

        self.registry.register(
            "configuration_manager",
            self.configuration_manager
        )

        self.registry.register(
            "logger_manager",
            self.logger_manager
        )

        self.registry.register(
            "workspace_manager",
            self.workspace_manager
        )

        self.registry.register(
            "dataset_manager",
            self.dataset_manager
        )

        self.registry.register(
            "navigation_manager",
            self.navigation_manager
        )

        self.registry.register(
            "resource_manager",
            self.resource_manager
        )

        self.registry.register(
            "session_manager",
            self.session_manager
        )

        self.registry.register(
            "theme_manager",
            self.theme_manager
        )

        self.registry.register(
            "event_manager",
            self.event_manager
        )