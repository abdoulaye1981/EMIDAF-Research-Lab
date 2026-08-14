"""
=========================================================
EMIDAF Framework v1.0
---------------------------------------------------------
Module : kernel.py

Description :
    Entry point of the EMIDAF Framework.

Author :
    EMIDAF Development Team

Version :
    1.0.0
=========================================================
"""

from __future__ import annotations

from emidaf_core.bootstrap import Bootstrap
from emidaf_core.registry import Registry


class Kernel:
    """
    Entry point of the EMIDAF Framework.

    The Kernel is responsible for starting the framework
    through the Bootstrap and exposing the Registry
    containing all initialized components.

    Responsibilities
    ----------------
    - Create the Bootstrap.
    - Start the Framework.
    - Provide access to the Registry.

    The Kernel contains no business logic.
    """

    def __init__(self) -> None:
        """
        Create a new Kernel instance.

        The Framework is not initialized until
        the ``start()`` method is called.
        """
        self._bootstrap: Bootstrap = Bootstrap()
        self._registry: Registry | None = None

    # ======================================================
    # Framework lifecycle
    # ======================================================

    def start(self) -> Registry:
        """
        Start the EMIDAF Framework.

        This method delegates the initialization
        process to the Bootstrap.

        Returns
        -------
        Registry
            Registry containing all initialized
            framework components.
        """
        self._registry = self._bootstrap.initialize()
        return self._registry

    # ======================================================
    # Registry access
    # ======================================================

    @property
    def registry(self) -> Registry | None:
        """
        Return the current Registry.

        Returns
        -------
        Registry | None
            The initialized Registry or ``None`` if the
            Framework has not yet been started.
        """
        return self._registry