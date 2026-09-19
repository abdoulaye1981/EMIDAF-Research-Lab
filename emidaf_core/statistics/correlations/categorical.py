"""
=========================================================
EMIDAF Framework
Categorical Correlation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Mesures d'association entre variables catégorielles.

Contient

- ChiSquare
- PhiCoefficient
- CramerV
- ContingencyCoefficient
=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency

from ..base.correlation_statistic import CorrelationStatistic


# ==========================================================
# BASE
# ==========================================================

class CategoricalCorrelation(CorrelationStatistic, ABC):

    """
    Classe mère des corrélations catégorielles.
    """

    category = "Categorical Correlation"


# ==========================================================
# CHI-SQUARE
# ==========================================================

class ChiSquare(CategoricalCorrelation):

    """
    Test du Chi².
    """

    name = "Chi Square"

    description = "Chi-square test"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        table = pd.crosstab(

            x,

            y

        )

        chi2, p, dof, expected = chi2_contingency(

            table

        )

        return {

            "method": "Chi Square",

            "chi2": float(chi2),

            "p_value": float(p),

            "degrees_of_freedom": int(dof),

            "expected": expected,

            "table": table

        }


# ==========================================================
# PHI COEFFICIENT
# ==========================================================

class PhiCoefficient(CategoricalCorrelation):

    """
    Coefficient Phi pour deux variables dichotomiques.

    Le coefficient est calculé directement à partir
    d'une table de contingence 2 x 2 :

        phi = (ad - bc) /
              sqrt((a+b)(c+d)(a+c)(b+d))

    Cette formulation préserve le signe et évite que
    la valeur du coefficient dépende d'une éventuelle
    correction de continuité appliquée au test du
    Khi-deux.
    """

    name = "Phi"

    description = "Phi Coefficient"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        result = ChiSquare.compute(
            x,
            y
        )

        table = result["table"]

        if table.shape != (2, 2):
            raise ValueError(
                "Phi coefficient requires "
                "a 2 x 2 contingency table."
            )

        values = table.to_numpy(
            dtype=float
        )

        a = values[0, 0]
        b = values[0, 1]
        c = values[1, 0]
        d = values[1, 1]

        denominator = np.sqrt(
            (a + b)
            * (c + d)
            * (a + c)
            * (b + d)
        )

        if (
            not np.isfinite(denominator)
            or denominator == 0
        ):
            raise ValueError(
                "Phi coefficient is undefined "
                "because at least one marginal "
                "frequency is zero."
            )

        phi = (
            (a * d) - (b * c)
        ) / denominator

        phi = float(phi)

        return cls.build_result(
            coefficient=phi,
            p_value=result["p_value"],
            method="Phi",
            strength=cls.strength(phi),
            direction=cls.direction(phi)
        )


# ==========================================================
# CRAMER V
# ==========================================================

class CramerV(CategoricalCorrelation):

    """
    V de Cramer.
    """

    name = "Cramer's V"

    description = "Cramer's Association"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        result = ChiSquare.compute(

            x,

            y

        )

        table = result["table"]

        n = table.values.sum()

        r, c = table.shape

        value = np.sqrt(

            result["chi2"]

            /

            (

                n

                *

                min(r - 1, c - 1)

            )

        )

        return cls.build_result(

            coefficient=float(value),

            p_value=result["p_value"],

            method="Cramer's V",

            strength=cls.strength(value),

            direction="None"

        )


# ==========================================================
# CONTINGENCY COEFFICIENT
# ==========================================================

class ContingencyCoefficient(CategoricalCorrelation):

    """
    Coefficient de contingence.
    """

    name = "Contingency Coefficient"

    description = "Pearson Contingency"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        result = ChiSquare.compute(

            x,

            y

        )

        table = result["table"]

        n = table.values.sum()

        value = np.sqrt(

            result["chi2"]

            /

            (

                result["chi2"]

                + n

            )

        )

        return cls.build_result(

            coefficient=float(value),

            p_value=result["p_value"],

            method="Contingency",

            strength=cls.strength(value),

            direction="None"

        )


# ==========================================================
# SERVICE
# ==========================================================

class CategoricalCorrelationStatistics:

    """
    Calcul de toutes les mesures
    d'association catégorielles.
    """

    @staticmethod
    def compute(
        x,
        y,
    ):

        return {

            "chi_square":

                ChiSquare.compute(

                    x,

                    y

                ),

            "phi":

                PhiCoefficient.compute(

                    x,

                    y

                ),

            "cramers_v":

                CramerV.compute(

                    x,

                    y

                ),

            "contingency":

                ContingencyCoefficient.compute(

                    x,

                    y

                )

        }