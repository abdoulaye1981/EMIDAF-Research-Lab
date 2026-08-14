"""
=========================================================
EMIDAF Framework v1.0
Registry
---------------------------------------------------------
Conteneur central des composants du Framework
=========================================================
"""

from __future__ import annotations

from typing import Any, Iterator


class Registry:
    """
    Registre central des composants.

    Responsabilités
    ----------------
    - Enregistrer des composants
    - Les retrouver
    - Les supprimer
    - Les lister

    Aucune logique métier.
    """

    def __init__(self) -> None:

        self._components: dict[str, Any] = {}

    # =====================================================
    # ENREGISTREMENT
    # =====================================================

    def register(self, name: str, component: Any) -> None:
        """
        Enregistre un composant.

        Raises
        ------
        ValueError
            Si un composant possède déjà ce nom.
        """

        if name in self._components:
            raise ValueError(f"Component '{name}' already registered.")

        self._components[name] = component

    # =====================================================
    # CONSULTATION
    # =====================================================

    def get(self, name: str) -> Any:
        """
        Retourne un composant.
        """

        if name not in self._components:
            raise KeyError(f"Unknown component '{name}'.")

        return self._components[name]

    def exists(self, name: str) -> bool:

        return name in self._components

    # =====================================================
    # SUPPRESSION
    # =====================================================

    def remove(self, name: str) -> bool:

        if name not in self._components:
            return False

        del self._components[name]

        return True

    def clear(self) -> None:

        self._components.clear()

    # =====================================================
    # ITERATION
    # =====================================================

    def keys(self):

        return self._components.keys()

    def values(self):

        return self._components.values()

    def items(self):

        return self._components.items()

    # =====================================================
    # MAGIC METHODS
    # =====================================================

    def __contains__(self, name: str) -> bool:

        return name in self._components

    def __len__(self) -> int:

        return len(self._components)

    def __iter__(self) -> Iterator[str]:

        return iter(self._components)

    def __getitem__(self, name: str) -> Any:

        return self.get(name)

    def __repr__(self) -> str:

        return f"Registry({list(self._components.keys())})"