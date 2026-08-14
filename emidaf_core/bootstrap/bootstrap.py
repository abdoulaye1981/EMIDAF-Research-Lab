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

        pass

    def _create_database(self):

        pass

    def _create_managers(self):

        pass

    def _create_mappers(self):

        pass

    def _create_repositories(self):

        pass

    def _create_services(self):

        pass

    def _create_controllers(self):

        pass

    def _register_components(self):

        pass