"""
=========================================================
EMIDAF Framework v1.0
Database Provider
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine


class DatabaseProvider(ABC):
    """
    Classe abstraite représentant un fournisseur de base
    de données.
    """

    def __init__(self, url: str) -> None:

        self._url = url

    @property
    def url(self) -> str:
        return self._url

    @abstractmethod
    def create_engine(self) -> Engine:
        """
        Crée le moteur SQLAlchemy.
        """
        raise NotImplementedError