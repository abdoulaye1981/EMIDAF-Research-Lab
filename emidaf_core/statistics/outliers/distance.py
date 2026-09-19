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

    method_family = "distance"

    score_type = "mahalanobis_distance"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @staticmethod
    def _prepare_dataframe(
        dataframe,
        alpha,
    ):
        """
        Prépare et valide les données utilisées
        pour les distances de Mahalanobis.
        """

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha must satisfy 0 < alpha < 1."
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        numeric = dataframe.select_dtypes(
            include="number"
        ).copy()

        if numeric.shape[1] == 0:
            raise ValueError(
                "At least one numeric column is required."
            )

        # Les valeurs infinies ne sont pas assimilées
        # à des valeurs manquantes.
        if not np.isfinite(
            numeric.to_numpy(
                dtype=float
            )
        ).all():
            finite_or_nan = (
                np.isfinite(
                    numeric.to_numpy(
                        dtype=float
                    )
                )
                |
                np.isnan(
                    numeric.to_numpy(
                        dtype=float
                    )
                )
            )

            if not finite_or_nan.all():
                raise ValueError(
                    "Infinite values are not supported."
                )

        numeric = numeric.dropna()

        if numeric.empty:
            raise ValueError(
                "No complete numeric observations remain "
                "after removing missing values."
            )

        n_observations = numeric.shape[0]
        n_variables = numeric.shape[1]

        if n_observations <= n_variables:
            raise ValueError(
                "Mahalanobis distance requires more "
                "complete observations than numeric variables."
            )

        return numeric

    @classmethod
    def detect(
        cls,
        dataframe,
        alpha=0.001,
    ):

        dataframe = cls._prepare_dataframe(
            dataframe,
            alpha,
        )

        x = dataframe.to_numpy(
            dtype=float
        )

        mean = np.mean(
            x,
            axis=0,
        )

        # Cas univarié :
        # np.cov retourne un scalaire.
        covariance = np.cov(
            x,
            rowvar=False,
        )

        covariance = np.atleast_2d(
            covariance
        )

        # La pseudo-inverse permet de gérer proprement :
        # - colinéarité parfaite
        # - colonnes constantes
        # - covariance de rang déficient
        inverse = np.linalg.pinv(
            covariance
        )

        centered = x - mean

        squared_distance = np.einsum(
            "ij,jk,ik->i",
            centered,
            inverse,
            centered,
        )

        # Protection contre de très petites valeurs
        # négatives dues aux erreurs numériques.
        squared_distance = np.maximum(
            squared_distance,
            0.0,
        )

        distance = np.sqrt(
            squared_distance
        )

        threshold = np.sqrt(
            chi2.ppf(
                1 - alpha,
                dataframe.shape[1],
            )
        )

        indices = dataframe.index[
            distance > threshold
        ]

        return cls.build_result(
            dataframe.index,
            indices,
            scores=distance,
            threshold=threshold,
            parameters={
                "alpha": alpha,
                "degrees_of_freedom":
                    dataframe.shape[1],
                "covariance_inverse":
                    "moore_penrose_pseudoinverse",
            },
        )

    fit = detect
    fit_predict = detect


# ==========================================================
# ROBUST MAHALANOBIS
# ==========================================================

class RobustMahalanobis(BaseOutlierDetector):

    name = "Robust Mahalanobis"

    method_family = "distance"

    score_type = "robust_mahalanobis_distance"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(
        cls,
        dataframe,
        alpha=0.001,
    ):

        dataframe = Mahalanobis._prepare_dataframe(
            dataframe,
            alpha,
        )

        estimator = MinCovDet(
            random_state=42
        )

        estimator.fit(
            dataframe
        )

        # sklearn renvoie les distances
        # de Mahalanobis AU CARRE.
        squared_distance = (
            estimator.mahalanobis(
                dataframe
            )
        )

        squared_distance = np.maximum(
            squared_distance,
            0.0,
        )

        # Harmonisation avec Mahalanobis :
        # le score public représente une distance.
        distance = np.sqrt(
            squared_distance
        )

        threshold = np.sqrt(
            chi2.ppf(
                1 - alpha,
                dataframe.shape[1],
            )
        )

        indices = dataframe.index[
            distance > threshold
        ]

        return cls.build_result(
            dataframe.index,
            indices,
            scores=distance,
            threshold=threshold,
            parameters={
                "alpha": alpha,
                "degrees_of_freedom":
                    dataframe.shape[1],
                "covariance_estimator":
                    "minimum_covariance_determinant",
                "random_state": 42,
            },
        )

    fit = detect
    fit_predict = detect


# ==========================================================
# COOK DISTANCE
# ==========================================================

class CookDistance(BaseOutlierDetector):

    name = "Cook Distance"

    method_family = "influence"

    score_type = "cooks_distance"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

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

    method_family = "influence"

    score_type = "leverage"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

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
