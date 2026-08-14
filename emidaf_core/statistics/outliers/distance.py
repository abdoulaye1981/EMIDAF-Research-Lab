"""
=========================================================
EMIDAF Framework
Distance Based Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détection des anomalies basée sur les distances.

Contient

- Mahalanobis
- Robust Mahalanobis
- Cook Distance
- Leverage

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import chi2

from sklearn.covariance import MinCovDet

from statsmodels.api import OLS
from statsmodels.api import add_constant

from .base import BaseOutlierDetector


# ==========================================================
# MAHALANOBIS
# ==========================================================

class Mahalanobis(BaseOutlierDetector):

    name = "Mahalanobis"

    @classmethod
    def detect(

        cls,

        dataframe,

        alpha=0.001,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        x = dataframe.values

        mean = np.mean(

            x,

            axis=0

        )

        covariance = np.cov(

            x,

            rowvar=False

        )

        inverse = np.linalg.inv(

            covariance

        )

        distance = []

        for row in x:

            d = row - mean

            value = np.sqrt(

                d.T

                @ inverse

                @ d

            )

            distance.append(value)

        distance = np.asarray(distance)

        threshold = np.sqrt(

            chi2.ppf(

                1-alpha,

                dataframe.shape[1]

            )

        )

        indices = dataframe.index[

            distance > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=distance,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ROBUST MAHALANOBIS
# ==========================================================

class RobustMahalanobis(BaseOutlierDetector):

    name = "Robust Mahalanobis"

    @classmethod
    def detect(

        cls,

        dataframe,

        alpha=0.001,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        estimator = MinCovDet()

        estimator.fit(

            dataframe

        )

        distance = estimator.mahalanobis(

            dataframe

        )

        threshold = chi2.ppf(

            1-alpha,

            dataframe.shape[1]

        )

        indices = dataframe.index[

            distance > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=distance,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# COOK DISTANCE
# ==========================================================

class CookDistance(BaseOutlierDetector):

    name = "Cook Distance"

    @classmethod
    def detect(

        cls,

        dataframe,

        target,

        threshold=None,

    ):

        dataframe = dataframe.dropna()

        X = dataframe.drop(

            columns=[target]

        )

        y = dataframe[target]

        X = add_constant(

            X

        )

        model = OLS(

            y,

            X

        ).fit()

        influence = model.get_influence()

        distance = influence.cooks_distance[0]

        if threshold is None:

            threshold = 4 / len(dataframe)

        indices = dataframe.index[

            distance > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=distance,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# LEVERAGE
# ==========================================================

class Leverage(BaseOutlierDetector):

    name = "Leverage"

    @classmethod
    def detect(

        cls,

        dataframe,

        target,

        threshold=None,

    ):

        dataframe = dataframe.dropna()

        X = dataframe.drop(

            columns=[target]

        )

        y = dataframe[target]

        X = add_constant(

            X

        )

        model = OLS(

            y,

            X

        ).fit()

        influence = model.get_influence()

        leverage = influence.hat_matrix_diag

        p = X.shape[1]

        n = len(X)

        if threshold is None:

            threshold = (2*p)/n

        indices = dataframe.index[

            leverage > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=leverage,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class DistanceOutlierDetector:

    """
    Lance tous les détecteurs
    basés sur la distance.
    """

    @staticmethod
    def compute(

        dataframe,

        target=None,

    ):

        results = {

            "mahalanobis":

                Mahalanobis.detect(

                    dataframe

                ),

            "robust_mahalanobis":

                RobustMahalanobis.detect(

                    dataframe

                )

        }

        if target is not None:

            results["cook_distance"] = (

                CookDistance.detect(

                    dataframe,

                    target

                )

            )

            results["leverage"] = (

                Leverage.detect(

                    dataframe,

                    target

                )

            )

        return results