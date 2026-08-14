"""
=========================================================
EMIDAF Framework
Base Repository
=========================================================

Classe de base des repositories.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .base_object import BaseObject


class BaseRepository(BaseObject, ABC):
    """
    Classe abstraite des repositories.
    """

    @abstractmethod
    def save(
        self,
        obj: Any,
    ) -> Any:
        """
        Sauvegarde un objet.
        """
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        identifier: Any,
    ) -> Any:
        """
        Charge un objet.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        identifier: Any,
        obj: Any,
    ) -> Any:
        """
        Met à jour un objet.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        identifier: Any,
    ) -> None:
        """
        Supprime un objet.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        identifier: Any,
    ) -> bool:
        """
        Vérifie si un objet existe.
        """
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """
        Nombre d'objets.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Vide le repository.
        """
        raise NotImplementedError