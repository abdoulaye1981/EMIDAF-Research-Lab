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

from scipy.stats import pointbiserialr, norm

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
        """
        Compute the biserial correlation.

        The binary variable ``x`` is assumed to represent
        an artificial dichotomization of an underlying
        continuous latent variable.

        Parameters
        ----------
        x :
            Dichotomous variable with exactly two levels.

        y :
            Continuous numeric variable.

        Notes
        -----
        The coefficient is computed as:

            r_b = ((M1 - M0) / s_y) * (p*q / phi(z))

        where ``p`` and ``q`` are the proportions of the two
        groups and ``phi(z)`` is the standard-normal density
        at the dichotomization threshold.

        No exact p-value is supplied because SciPy does not
        provide a dedicated biserial-correlation significance
        test.
        """

        x, y = cls.validate_pair(
            x,
            y
        )

        x = np.asarray(x)
        y = np.asarray(
            y,
            dtype=float
        )

        levels = np.unique(x)

        if len(levels) != 2:
            raise ValueError(
                "Biserial correlation requires "
                "a dichotomous variable with "
                "exactly two levels."
            )

        # Deterministic coding:
        # first ordered level -> group 0
        # second ordered level -> group 1

        group0 = y[
            x == levels[0]
        ]

        group1 = y[
            x == levels[1]
        ]

        n = len(y)

        if n < 3:
            raise ValueError(
                "At least three observations are "
                "required for biserial correlation."
            )

        p = len(group1) / n
        q = 1.0 - p

        if (
            p <= 0.0
            or q <= 0.0
        ):
            raise ValueError(
                "Both groups must contain observations."
            )

        standard_deviation = np.std(
            y,
            ddof=1
        )

        if (
            not np.isfinite(
                standard_deviation
            )
            or standard_deviation == 0
        ):
            raise ValueError(
                "The continuous variable must have "
                "non-zero variance."
            )

        mean0 = np.mean(
            group0
        )

        mean1 = np.mean(
            group1
        )

        threshold = norm.ppf(
            q
        )

        ordinate = norm.pdf(
            threshold
        )

        if (
            not np.isfinite(
                ordinate
            )
            or ordinate == 0
        ):
            raise ValueError(
                "Unable to compute the normal-density "
                "correction for the group proportions."
            )

        coefficient = (
            (
                mean1
                - mean0
            )
            / standard_deviation
        ) * (
            p
            * q
            / ordinate
        )

        coefficient = float(
            coefficient
        )

        return cls.build_result(
            coefficient=coefficient,
            p_value=np.nan,
            method="Biserial",
            strength=cls.strength(
                coefficient
            ),
            direction=cls.direction(
                coefficient
            )
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