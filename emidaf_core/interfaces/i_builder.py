"""
EMIDAF Framework v1.0
Builder Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IBuilder(ABC):
    """
    Interface générale des Builders EMIDAF.
    """

    @abstractmethod
    def build(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Construit l'objet ou la ressource demandée.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        Réinitialise le builder.
        """
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> None:
        """
        Valide le résultat construit.
        """
        raise NotImplementedError

    @abstractmethod
    def finalize(self) -> Any:
        """
        Retourne le résultat final.
        """
        raise NotImplementedError
