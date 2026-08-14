"""
=========================================================
EMIDAF Framework
Hypothesis Test
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Classe abstraite de tous les tests d'hypothèses.

Toutes les classes suivantes héritent de cette classe :

- ShapiroWilk
- AndersonDarling
- JarqueBera
- KolmogorovSmirnov
- StudentTTest
- WelchTTest
- ANOVA
- MannWhitney
- Wilcoxon
- KruskalWallis
- Friedman
- ChiSquare
- FisherExact
- McNemar
- Levene
- Bartlett
- LittleMCAR
=========================================================
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from .inferential_statistic import InferentialStatistic


class HypothesisTest(InferentialStatistic):
    """
    Classe mère de tous les tests d'hypothèses.
    """

    category: str = "Hypothesis Test"

    default_alpha: float = 0.05

    # =====================================================
    # API
    # =====================================================

    @classmethod
    @abstractmethod
    def compute(
        cls,
        *samples: Any,
        alpha: float = 0.05,
        **kwargs,
    ) -> dict:
        """
        Exécute le test d'hypothèse.

        Parameters
        ----------
        samples :
            Echantillons.

        alpha :
            Niveau de significativité.

        Returns
        -------
        dict
        """

        raise NotImplementedError

    # =====================================================
    # Decision
    # =====================================================

    @classmethod
    def reject_null(
        cls,
        p_value: float,
        alpha: float = 0.05,
    ) -> bool:
        """
        Décision statistique.
        """

        return p_value < alpha

    @classmethod
    def decision(
        cls,
        p_value: float,
        alpha: float = 0.05,
    ) -> str:
        """
        Décision textuelle.
        """

        if p_value < alpha:

            return "Reject H0"

        return "Fail to Reject H0"

    @classmethod
    def significance(
        cls,
        p_value: float,
    ) -> str:
        """
        Niveau de significativité.
        """

        if p_value < 0.001:
            return "***"

        if p_value < 0.01:
            return "**"

        if p_value < 0.05:
            return "*"

        return "ns"

    # =====================================================
    # Interpretation
    # =====================================================

    @classmethod
    def interpretation(
        cls,
        p_value: float,
        alpha: float = 0.05,
    ) -> str:
        """
        Interprétation automatique.
        """

        if p_value < alpha:

            return (
                "The null hypothesis is rejected."
            )

        return (
            "The null hypothesis cannot be rejected."
        )

    # =====================================================
    # Result Builder
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
        Construit un résultat standardisé.
        """

        result = {

            "test": cls.name,

            "category": cls.category,

            "statistic": float(statistic),

            "p_value": float(p_value),

            "alpha": alpha,

            "reject_null": cls.reject_null(
                p_value,
                alpha
            ),

            "decision": cls.decision(
                p_value,
                alpha
            ),

            "significance": cls.significance(
                p_value
            ),

            "interpretation": cls.interpretation(
                p_value,
                alpha
            )

        }

        result.update(extra)

        return result

    # =====================================================
    # Validation
    # =====================================================

    @classmethod
    def validate_alpha(
        cls,
        alpha: float,
    ) -> float:
        """
        Vérifie alpha.
        """

        if not 0 < alpha < 1:

            raise ValueError(
                "Alpha must belong to ]0,1[."
            )

        return alpha

    # =====================================================
    # Metadata
    # =====================================================

    @classmethod
    def info(cls) -> dict:
        """
        Informations sur le test.
        """

        return {

            "name": cls.name,

            "description": cls.description,

            "category": cls.category,

            "version": cls.version,

            "default_alpha": cls.default_alpha

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