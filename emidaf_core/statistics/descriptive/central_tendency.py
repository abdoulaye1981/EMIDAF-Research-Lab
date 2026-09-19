"""
=========================================================
EMIDAF Framework
Central Tendency Statistics
=========================================================

Module de compatibilité pour les statistiques
de tendance centrale.
"""

from __future__ import annotations

from .location import (
    Mean,
    Median,
    Mode,
)


class CentralTendency:

    registry = {
        "mean": Mean,
        "median": Median,
        "mode": Mode,
    }

    @classmethod
    def compute(
        cls,
        method,
        values,
    ):

        if method not in cls.registry:
            raise ValueError(
                f"Unknown central tendency method: {method}"
            )

        model = cls.registry[method]

        return model.compute(values)

    @classmethod
    def all(
        cls,
        values,
    ):

        return {
            "mean": Mean.compute(values),
            "median": Median.compute(values),
            "mode": Mode.compute(values),
        }


__all__ = [
    "CentralTendency",
]
