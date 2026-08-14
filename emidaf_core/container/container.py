"""
=========================================================
EMIDAF Framework v1.0
Dependency Injection Container
=========================================================
"""

from __future__ import annotations

from typing import Any
from typing import Type


class Container:
    """
    Conteneur d'injection de dépendances.

    Stocke les instances uniques utilisées par
    l'application.
    """

    def __init__(self) -> None:

        self._instances: dict[Type[Any], Any] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        instance: Any
    ) -> None:
        """
        Enregistre une instance.
        """

        self._instances[type(instance)] = instance

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        cls: Type[Any]
    ) -> Any:
        """
        Retourne une instance.
        """

        if cls not in self._instances:

            raise KeyError(
                f"{cls.__name__} not registered."
            )

        return self._instances[cls]

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        cls: Type[Any]
    ) -> bool:

        return cls in self._instances

    # =====================================================
    # REMOVE
    # =====================================================

    def remove(
        self,
        cls: Type[Any]
    ) -> None:

        self._instances.pop(cls, None)

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self) -> None:

        self._instances.clear()

    # =====================================================
    # ITERATION
    # =====================================================

    def items(self):

        return self._instances.items()

    def values(self):

        return self._instances.values()

    def keys(self):

        return self._instances.keys()

    # =====================================================
    # MAGIC
    # =====================================================

    def __contains__(
        self,
        cls: Type[Any]
    ) -> bool:

        return self.exists(cls)

    def __getitem__(
        self,
        cls: Type[Any]
    ) -> Any:

        return self.get(cls)

    def __len__(self) -> int:

        return len(self._instances)