"""
=========================================================
EMIDAF Framework
Base Manager
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .base_object import BaseObject
from .base_service import BaseService


class BaseManager(BaseObject, ABC):
    """
    Classe de base des managers.

    Le Manager constitue le point d'entrée d'un module.
    """

    def __init__(
        self,
        service: BaseService,
    ) -> None:

        super().__init__()

        self._service = service

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def service(self) -> BaseService:
        """
        Service associé.
        """
        return self._service

    # =====================================================
    # EXECUTION
    # =====================================================

    @abstractmethod
    def run(
        self,
        *args,
        **kwargs,
    ) -> Any:
        """
        Point d'entrée du manager.
        """
        raise NotImplementedError

    # =====================================================
    # SHORTCUTS
    # =====================================================

    def exists(
        self,
        identifier: Any,
    ) -> bool:

        return self.service.exists(identifier)

    def count(self) -> int:

        return self.service.count()

    def clear(self) -> None:

        self.service.clear()

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(service={self.service.__class__.__name__})"

        )