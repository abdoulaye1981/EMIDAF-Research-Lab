"""
=========================================================
EMIDAF Framework v1.0
Base Command
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseCommand(ABC):
    """
    Classe de base de toutes les commandes.
    """

    @abstractmethod
    def execute(self):
        """
        Exécute la commande.
        """
        raise NotImplementedError