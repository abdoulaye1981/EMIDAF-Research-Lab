"""
=========================================================
EMIDAF Framework
Cache
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from typing import Any


class Cache:
    """
    Cache mémoire générique.
    """

    def __init__(self) -> None:

        self._storage: dict[str, Any] = {}

    # =====================================================
    # CRUD
    # =====================================================

    def put(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._storage[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._storage.get(key, default)

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self._storage

    def remove(
        self,
        key: str,
    ) -> None:

        self._storage.pop(key, None)

    def clear(self) -> None:

        self._storage.clear()

    # =====================================================
    # INFORMATION
    # =====================================================

    @property
    def size(self) -> int:

        return len(self._storage)

    @property
    def is_empty(self) -> bool:

        return self.size == 0

    @property
    def keys(self) -> list[str]:

        return list(self._storage.keys())

    @property
    def values(self) -> list[Any]:

        return list(self._storage.values())

    def to_dict(self) -> dict[str, Any]:

        return dict(self._storage)

    # =====================================================
    # MAGIC METHODS
    # =====================================================

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return self.exists(key)

    def __len__(self) -> int:

        return self.size

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(size={self.size})"

        )