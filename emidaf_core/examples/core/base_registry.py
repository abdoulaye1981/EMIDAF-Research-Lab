"""
=========================================================
EMIDAF Framework
Base Registry
=========================================================
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from .base_object import BaseObject

T = TypeVar("T")


class BaseRegistry(BaseObject, Generic[T]):
    """
    Registre générique de composants.

    Le registre garantit :
        - unicité des noms
        - ordre d'enregistrement
        - recherche rapide
    """

    def __init__(self) -> None:

        super().__init__()

        self._items: dict[str, T] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        name: str,
        item: T,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Enregistre un composant.
        """

        if not overwrite and name in self._items:

            raise ValueError(

                f"'{name}' is already registered."

            )

        self._items[name] = item

    # =====================================================
    # UNREGISTER
    # =====================================================

    def unregister(
        self,
        name: str,
    ) -> None:

        self._items.pop(name, None)

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        name: str,
    ) -> T:

        if name not in self._items:

            raise KeyError(

                f"'{name}' not found."

            )

        return self._items[name]

    # =====================================================
    # FIND
    # =====================================================

    def find(
        self,
        name: str,
        default: T | None = None,
    ) -> T | None:

        return self._items.get(name, default)

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._items

    # =====================================================
    # REMOVE ALL
    # =====================================================

    def clear(self) -> None:

        self._items.clear()

    # =====================================================
    # INFORMATION
    # =====================================================

    @property
    def names(self) -> list[str]:

        return list(self._items.keys())

    @property
    def values(self) -> list[T]:

        return list(self._items.values())

    @property
    def size(self) -> int:

        return len(self._items)

    @property
    def is_empty(self) -> bool:

        return self.size == 0

    # =====================================================
    # SORT
    # =====================================================

    def sort(self) -> None:

        self._items = dict(

            sorted(

                self._items.items()

            )

        )

    # =====================================================
    # ITERATION
    # =====================================================

    def __iter__(self) -> Iterator[T]:

        return iter(

            self._items.values()

        )

    def __len__(self) -> int:

        return self.size

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self):

        data = super().to_dict()

        data.update(

            {

                "size": self.size,

                "items": self.names,

            }

        )

        return data