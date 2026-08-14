"""
=========================================================
EMIDAF Framework
Inferential Statistic
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe de base des statistiques inférentielles.

Toutes les méthodes d'inférence statistique héritent
de cette classe.

Exemples
---------
StudentTTest
WelchTTest
ANOVA
MannWhitney
Wilcoxon
KruskalWallis
Friedman
ChiSquare
Levene
Bartlett
Shapiro
JarqueBera
=========================================================
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

import numpy as np
import pandas as pd

from .base_statistic import BaseStatistic


class InferentialStatistic(BaseStatistic):
    """
    Classe de base des méthodes statistiques
    inférentielles.

    Elle fournit :

    - validation automatique
    - validation de plusieurs échantillons
    - calcul sécurisé
    - résumé standardisé
    """

    category: str = "Inferential"

    # =====================================================
    # API
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        *samples: Any,
        **kwargs,
    ) -> dict:
        """
        Effectue le calcul statistique.

        Returns
        -------
        dict
        """

        raise NotImplementedError

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate_sample(
        cls,
        values: Any,
    ) -> pd.Series:
        """
        Valide un échantillon.
        """

        values = cls.validate(values)

        if cls.is_empty(values):

            raise ValueError(

                "Empty sample."

            )

        return values

    @classmethod
    def validate_samples(
        cls,
        *samples: Any,
    ) -> list[pd.Series]:
        """
        Valide plusieurs échantillons.
        """

        validated = []

        for sample in samples:

            validated.append(

                cls.validate_sample(sample)

            )

        return validated

    # =====================================================
    # Sample Information
    # =====================================================

    @classmethod
    def sample_size(
        cls,
        values: pd.Series,
    ) -> int:
        """
        Taille d'un échantillon.
        """

        return len(values)

    @classmethod
    def sample_mean(
        cls,
        values: pd.Series,
    ) -> float:
        """
        Moyenne.
        """

        return float(values.mean())

    @classmethod
    def sample_variance(
        cls,
        values: pd.Series,
    ) -> float:
        """
        Variance.
        """

        return float(values.var())

    @classmethod
    def sample_std(
        cls,
        values: pd.Series,
    ) -> float:
        """
        Ecart-type.
        """

        return float(values.std())

    # =====================================================
    # Utilities
    # =====================================================

    @classmethod
    def check_same_size(
        cls,
        sample1: pd.Series,
        sample2: pd.Series,
    ) -> bool:
        """
        Vérifie si les tailles sont identiques.
        """

        return len(sample1) == len(sample2)

    @classmethod
    def safe_compute(
        cls,
        *samples,
        default=None,
        **kwargs,
    ):
        """
        Calcul sécurisé.
        """

        try:

            return cls.compute(

                *samples,

                **kwargs

            )

        except Exception:

            return default

    # =====================================================
    # Result
    # =====================================================

    @classmethod
    def build_result(
        cls,
        statistic: float,
        p_value: float,
        alpha: float = 0.05,
        **extra,
    ) -> dict:
        """
        Construit un résultat standard.
        """

        return {

            "test": cls.name,

            "category": cls.category,

            "statistic": float(statistic),

            "p_value": float(p_value),

            "alpha": alpha,

            "reject_null":

                p_value < alpha,

            **extra,

        }

    # =====================================================
    # Summary
    # =====================================================

    @classmethod
    def summary(
        cls,
        result: dict,
    ) -> dict:
        """
        Résumé du test.
        """

        return {

            "test": result.get("test"),

            "statistic": result.get("statistic"),

            "p_value": result.get("p_value"),

            "reject_null":

                result.get("reject_null"),

            "alpha":

                result.get("alpha"),

        }

    # =====================================================
    # Information
    # =====================================================

    @classmethod
    def info(cls) -> dict:
        """
        Métadonnées du test.
        """

        return {

            "name": cls.name,

            "description": cls.description,

            "category": cls.category,

            "version": cls.version,

        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name='{self.name}', "

            f"category='{self.category}')"

        )

    def __str__(self):

        return self.__repr__()