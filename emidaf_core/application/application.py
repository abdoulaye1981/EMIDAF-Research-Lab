"""
=========================================================
EMIDAF Framework
Application
=========================================================
"""

from __future__ import annotations

from emidaf_core.bootstrap import Bootstrap
from emidaf_core.container import Container


class EMIDAFApplication:
    """
    Classe principale du Framework.

    Responsable du cycle de vie
    complet de l'application.
    """

    def __init__(self) -> None:

        self._bootstrap = Bootstrap()

        self._container: Container | None = None

        self._initialized = False

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialise entièrement le Framework.
        """

        if self._initialized:

            return

        self._container = self._bootstrap.initialize()

        self._initialized = True

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def container(self) -> Container:

        if self._container is None:

            raise RuntimeError(
                "Application has not been initialized."
            )

        return self._container

    @property
    def initialized(self) -> bool:

        return self._initialized

    # =====================================================
    # SHUTDOWN
    # =====================================================

    def shutdown(self) -> None:
        """
        Libère les ressources du Framework.
        """

        if self._container is not None:

            self._container.clear()

        self._initialized = False

    # =====================================================
    # RESTART
    # =====================================================

    def restart(self) -> None:

        self.shutdown()

        self.initialize()

    # =====================================================
    # RUN
    # =====================================================

    def run(self) -> None:
        """
        Point d'entrée de l'application.

        Cette méthode sera complétée lorsque
        EMIDAF Studio sera développé.
        """

        self.initialize()