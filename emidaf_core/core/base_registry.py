"""
=========================================================
EMIDAF Framework
Base Registry
=========================================================

Classe générique permettant d'enregistrer tous les
composants du framework :

- Analyzers
- Builders
- Engines
- Factories
- Services
- Plugins
- Exporters
- etc.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from .base_object import BaseObject

T = TypeVar("T")


class BaseRegistry(BaseObject, Generic[T]):
    """
    Registre générique.

    Le registre garantit :

    - unicité des composants
    - ordre d'insertion
    - recherche rapide
    - itération
    """

    def __init__(self) -> None:

        super().__init__()

        self._items: dict[str, T] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        item_or_name,
        component=None,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Enregistre un composant.

        Deux formes sont supportées :

        register(component)
            Le composant doit posséder un attribut ``name``.

        register(name, component)
            Enregistre explicitement le composant sous ``name``.
        """

        if component is None:
            item = item_or_name

            if not hasattr(item, "name"):
                raise AttributeError(
                    f"{item.__class__.__name__} must define a 'name' attribute."
                )

            name = item.name

        else:
            name = item_or_name
            item = component

            if not isinstance(name, str) or not name:
                raise ValueError(
                    "Registry name must be a non-empty string."
                )

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
        """
        Supprime un composant.
        """

        self._items.pop(name, None)

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        name: str,
    ) -> T:
        """
        Retourne un composant.
        """

        if name not in self._items:

            raise KeyError(

                f"'{name}' is not registered."

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
        """
        Recherche un composant.
        """

        return self._items.get(name, default)

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Vérifie si un composant existe.
        """

        return name in self._items

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self) -> None:
        """
        Vide complètement le registre.
        """

        self._items.clear()

    # =====================================================
    # SORT
    # =====================================================

    def sort(self) -> None:
        """
        Trie les composants par nom.
        """

        self._items = dict(

            sorted(

                self._items.items(),

                key=lambda item: item[0]

            )

        )

    # =====================================================
    # INFORMATION
    # =====================================================

    @property
    def names(self) -> list[str]:
        """
        Liste des noms enregistrés.
        """

        return list(self._items.keys())

    @property
    def values(self) -> list[T]:
        """
        Liste des composants.
        """

        return list(self._items.values())

    @property
    def items(self) -> list[tuple[str, T]]:
        """
        Liste des couples (nom, composant).
        """

        return list(self._items.items())

    @property
    def size(self) -> int:
        """
        Nombre de composants.
        """

        return len(self._items)

    @property
    def is_empty(self) -> bool:
        """
        Le registre est-il vide ?
        """

        return self.size == 0

    # =====================================================
    # ITERATION
    # =====================================================

    def __iter__(self) -> Iterator[T]:
        """
        Permet :

        for analyzer in registry:
        """

        return iter(self._items.values())

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

    def to_dict(self) -> dict:

        data = super().to_dict()

        data.update(

            {

                "size": self.size,

                "names": self.names,

            }

        )

        return data

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(size={self.size})"

        )