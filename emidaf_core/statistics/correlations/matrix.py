"""
=========================================================
EMIDAF Framework
Mixed Correlation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Mesures d'association entre variables de types différents.

Contient

- PointBiserial
- Biserial
- CorrelationRatio (Eta)
=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.stats import biserialr
from scipy.stats import pointbiserialr

from ..base.correlation_statistic import CorrelationStatistic


# ==========================================================
# BASE
# ==========================================================

class MixedCorrelation(CorrelationStatistic, ABC):
    """
    Classe mère des corrélations mixtes.
    """

    category = "Mixed Correlation"


# ==========================================================
# POINT BISERIAL
# ==========================================================

class PointBiserial(MixedCorrelation):

    name = "Point Biserial"

    description = "Point-Biserial Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        coefficient, pvalue = pointbiserialr(

            x,

            y

        )

        return cls.build_result(

            coefficient=coefficient,

            p_value=pvalue,

            method="Point Biserial",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# ==========================================================
# BISERIAL
# ==========================================================

class Biserial(MixedCorrelation):

    name = "Biserial"

    description = "Biserial Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        coefficient, pvalue = biserialr(

            x,

            y

        )

        return cls.build_result(

            coefficient=coefficient,

            p_value=pvalue,

            method="Biserial",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# ==========================================================
# ETA (Correlation Ratio)
# ==========================================================

class CorrelationRatio(MixedCorrelation):

    """
    Eta (η).

    Variable catégorielle
    contre variable numérique.
    """

    name = "Correlation Ratio"

    description = "Eta"

    @classmethod
    def compute(
        cls,
        categories,
        values,
    ):

        categories = pd.Series(categories)

        values = pd.Series(values)

        dataframe = pd.DataFrame(

            {

                "cat": categories,

                "value": values

            }

        ).dropna()

        grand_mean = dataframe["value"].mean()

        numerator = 0.0

        denominator = (

            (dataframe["value"] - grand_mean)

            ** 2

        ).sum()

        for _, group in dataframe.groupby("cat"):

            mean = group["value"].mean()

            numerator += (

                len(group)

                *

                (mean - grand_mean) ** 2

            )

        eta = np.sqrt(

            numerator / denominator

        )

        return cls.build_result(

            coefficient=float(eta),

            p_value=np.nan,

            method="Correlation Ratio",

            strength=cls.strength(eta),

            direction="None"

        )


# ==========================================================
# SERVICE
# ==========================================================

class MixedCorrelationStatistics:

    """
    Calcul de toutes les corrélations mixtes.
    """

    @staticmethod
    def compute(
        binary,
        numeric,
    ):

        return {

            "point_biserial":

                PointBiserial.compute(

                    binary,

                    numeric

                ),

            "biserial":

                Biserial.compute(

                    binary,

                    numeric

                )

        }

    @staticmethod
    def eta(
        categories,
        values,
    ):

        return CorrelationRatio.compute(

            categories,

            values

        )