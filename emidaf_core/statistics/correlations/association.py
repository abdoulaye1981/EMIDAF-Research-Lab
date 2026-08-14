"""
=========================================================
EMIDAF Framework
Association Measures
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Mesures générales d'association.

Contient

- Mutual Information
- Distance Correlation
- Concordance Correlation Coefficient

=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.spatial.distance import pdist
from sklearn.metrics import mutual_info_score

from ..base.correlation_statistic import CorrelationStatistic


# =========================================================
# BASE
# =========================================================

class AssociationStatistic(CorrelationStatistic, ABC):
    """
    Classe mère des mesures d'association.
    """

    category = "Association"


# =========================================================
# MUTUAL INFORMATION
# =========================================================

class MutualInformation(AssociationStatistic):

    name = "Mutual Information"

    description = "Mutual Information Score"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        score = mutual_info_score(

            x,

            y

        )

        return cls.build_result(

            coefficient=float(score),

            p_value=np.nan,

            method="Mutual Information",

            strength="N/A",

            direction="None"

        )


# =========================================================
# DISTANCE CORRELATION
# =========================================================

class DistanceCorrelation(AssociationStatistic):

    """
    Distance Correlation.

    Implémentation basée sur Székely.
    """

    name = "Distance Correlation"

    description = "Distance Correlation"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        x = np.asarray(x).reshape(-1, 1)

        y = np.asarray(y).reshape(-1, 1)

        a = pdist(x)

        b = pdist(y)

        coefficient = np.corrcoef(

            a,

            b

        )[0, 1]

        return cls.build_result(

            coefficient=float(coefficient),

            p_value=np.nan,

            method="Distance Correlation",

            strength=cls.strength(coefficient),

            direction=cls.direction(coefficient)

        )


# =========================================================
# CONCORDANCE CORRELATION
# =========================================================

class ConcordanceCorrelation(AssociationStatistic):

    """
    Concordance Correlation Coefficient.

    Lin (1989)
    """

    name = "Concordance Correlation"

    description = "CCC"

    @classmethod
    def compute(
        cls,
        x,
        y,
    ):

        x, y = cls.validate_pair(x, y)

        mean_x = np.mean(x)

        mean_y = np.mean(y)

        var_x = np.var(x)

        var_y = np.var(y)

        covariance = np.cov(

            x,

            y

        )[0, 1]

        ccc = (

            2 * covariance

        ) / (

            var_x

            + var_y

            + (mean_x - mean_y) ** 2

        )

        return cls.build_result(

            coefficient=float(ccc),

            p_value=np.nan,

            method="CCC",

            strength=cls.strength(ccc),

            direction=cls.direction(ccc)

        )


# =========================================================
# SERVICE
# =========================================================

class AssociationStatistics:
    """
    Calcul de toutes les mesures
    d'association.
    """

    @staticmethod
    def compute(
        x,
        y,
    ):

        return {

            "mutual_information":

                MutualInformation.compute(

                    x,

                    y

                ),

            "distance_correlation":

                DistanceCorrelation.compute(

                    x,

                    y

                ),

            "concordance":

                ConcordanceCorrelation.compute(

                    x,

                    y

                )

        }