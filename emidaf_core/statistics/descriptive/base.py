"""
=========================================================
EMIDAF Framework
Compatibilité des statistiques descriptives
=========================================================

Ce module assure la compatibilité avec les statistiques
descriptives historiques utilisant :

    BaseStatistic
    StatisticResult

La base statistique actuelle reste définie dans :

    emidaf_core.statistics.base.base_statistic

Ce fichier ne modifie pas l'architecture actuelle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..base.base_statistic import BaseStatistic


@dataclass
class StatisticResult:
    """
    Résultat standard des anciennes statistiques descriptives.

    Parameters
    ----------
    statistic : str
        Nom de la statistique.
    value : Any
        Valeur calculée.
    interpretation : str
        Interprétation éventuelle du résultat.
    recommendation : str
        Recommandation éventuelle.
    metadata : dict
        Métadonnées complémentaires.
    """

    statistic: str = ""
    value: Any = None
    interpretation: str = ""
    recommendation: str = ""
    metadata: dict = field(default_factory=dict)


__all__ = [
    "BaseStatistic",
    "StatisticResult",
]
