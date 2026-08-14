"""
=========================================================
EMIDAF Framework
Linear Correlation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Corrélations linéaires.

Contient :

- Pearson
- Spearman
- Kendall

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.stats import kendalltau
from scipy.stats import pearsonr
from scipy.stats import spearmanr

from ..base.correlation_statistic import CorrelationStatistic


# =====================================================
# BASE
# =====================================================

class LinearCorrelation(CorrelationStatistic, ABC):
    """
    Classe de base des corrélations linéaires.
    """

    category = "Linear Correlation"


# =====================================================
# PEARSON
# =====================================================

class Pearson(LinearCorrelation):

    name = "Pearson"

    description = "Pearson Linear Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        coefficient, pvalue = pearsonr(x, y)

        return cls.build_result(

            coefficient=coefficient,

            p_value=pvalue,

            method="Pearson",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# =====================================================
# SPEARMAN
# =====================================================

class Spearman(LinearCorrelation):

    name = "Spearman"

    description = "Spearman Rank Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        coefficient, pvalue = spearmanr(x, y)

        return cls.build_result(

            coefficient=coefficient,

            p_value=pvalue,

            method="Spearman",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# =====================================================
# KENDALL
# =====================================================

class Kendall(LinearCorrelation):

    name = "Kendall"

    description = "Kendall Tau Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        coefficient, pvalue = kendalltau(x, y)

        return cls.build_result(

            coefficient=coefficient,

            p_value=pvalue,

            method="Kendall",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# =====================================================
# SERVICE
# =====================================================

class LinearCorrelationStatistics:
    """
    Calcul de toutes les corrélations linéaires.
    """

    @staticmethod
    def compute(
        x,
        y,
    ):

        return {

            "pearson":

                Pearson.compute(x, y),

            "spearman":

                Spearman.compute(x, y),

            "kendall":

                Kendall.compute(x, y)

        }


# =====================================================
# MATRIX
# =====================================================

class LinearCorrelationMatrix:
    """
    Matrice de corrélation.
    """

    @staticmethod
    def compute(
        dataframe: pd.DataFrame,
        method: str = "pearson",
    ) -> pd.DataFrame:

        dataframe = dataframe.select_dtypes(

            include="number"

        )

        return dataframe.corr(

            method=method

        )


# =====================================================
# INTERPRETATION
# =====================================================

class CorrelationInterpretation:
    """
    Outils d'interprétation.
    """

    @staticmethod
    def strength(value: float) -> str:

        value = abs(value)

        if value < 0.20:
            return "Very Weak"

        if value < 0.40:
            return "Weak"

        if value < 0.60:
            return "Moderate"

        if value < 0.80:
            return "Strong"

        return "Very Strong"

    @staticmethod
    def direction(value: float) -> str:

        if value > 0:
            return "Positive"

        if value < 0:
            return "Negative"

        return "Null"

    @staticmethod
    def interpretation(value: float) -> str:

        return (

            f"{CorrelationInterpretation.strength(value)} "

            f"{CorrelationInterpretation.direction(value)} "

            f"Correlation"

        )