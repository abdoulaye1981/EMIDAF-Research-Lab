"""
=========================================================
EMIDAF Framework
Base Service
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .base_object import BaseObject
from .base_repository import BaseRepository


class BaseService(BaseObject, ABC):
    """
    Classe de base de tous les services métier.
    """

    def __init__(
        self,
        repository: BaseRepository,
    ) -> None:

        super().__init__()

        self._repository = repository

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def repository(self) -> BaseRepository:
        """
        Repository associé au service.
        """
        return self._repository

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        obj: Any,
    ) -> None:
        """
        Validation métier.

        Les classes filles peuvent redéfinir cette méthode.
        """
        return None

    # =====================================================
    # CRUD
    # =====================================================

    def save(
        self,
        obj: Any,
    ) -> Any:

        self.validate(obj)

        return self.repository.save(obj)

    def load(
        self,
        identifier: Any,
    ) -> Any:

        return self.repository.load(identifier)

    def update(
        self,
        identifier: Any,
        obj: Any,
    ) -> Any:

        self.validate(obj)

        return self.repository.update(identifier, obj)

    def delete(
        self,
        identifier: Any,
    ) -> None:

        self.repository.delete(identifier)

    def exists(
        self,
        identifier: Any,
    ) -> bool:

        return self.repository.exists(identifier)

    def count(self) -> int:

        return self.repository.count()

    def clear(self) -> None:

        self.repository.clear()

    # =====================================================
    # EXECUTION
    # =====================================================

    @abstractmethod
    def execute(
        self,
        *args,
        **kwargs,
    ):
        """
        Point d'entrée métier.

        Chaque service doit implémenter cette méthode.
        """
        raise NotImplementedError