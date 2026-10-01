"""
=========================================================
EMIDAF Framework v1.0
EMIX - Source Adapter Base
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..sources import MixedMethodSource


class BaseSourceAdapter(ABC):
    """
    Contrat commun des adaptateurs de sources EMIX.
    """

    engine_name: str

    @abstractmethod
    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:
        """
        Convertit un résultat persistant d'un moteur
        EMIDAF en MixedMethodSource.
        """
        raise NotImplementedError
