"""
=========================================================
EMIDAF Framework
Multivariate Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détection multivariée des valeurs aberrantes.

Contient

- PCA Outlier
- Robust PCA
- AutoEncoder (placeholder)
- Feature Bagging
- Minimum Covariance Determinant

=========================================================
"""

from __future__ import annotations

import numpy as np

from sklearn.covariance import MinCovDet
from sklearn.decomposition import PCA

from .base import BaseOutlierDetector


# ==========================================================
# PCA OUTLIER
# ==========================================================

class PCAOutlier(BaseOutlierDetector):

    name = "PCA"

    method_family = "dimensionality_reduction"

    score_type = "reconstruction_error"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        n_components=2,

        percentile=95,

    ):

        if not isinstance(
            n_components,
            int,
        ) or n_components < 1:
            raise ValueError(
                "n_components must be an integer >= 1."
            )

        if not 0 <= percentile <= 100:
            raise ValueError(
                "percentile must satisfy 0 <= percentile <= 100."
            )

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = PCA(

            n_components=n_components

        )

        transformed = model.fit_transform(

            dataframe

        )

        reconstruction = model.inverse_transform(

            transformed

        )

        error = np.linalg.norm(

            dataframe.values - reconstruction,

            axis=1

        )

        threshold = np.percentile(

            error,

            percentile

        )

        indices = dataframe.index[

            error > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=error,

            threshold=threshold,

            parameters={

                "components": n_components,

                "percentile": percentile

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# ROBUST PCA
# ==========================================================

class RobustPCAOutlier(BaseOutlierDetector):

    """
    Approximation utilisant
    Minimum Covariance Determinant.
    """

    name = "Robust PCA"

    method_family = "covariance"

    score_type = "squared_robust_mahalanobis_distance"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        percentile=97.5,

    ):

        if not 0 <= percentile <= 100:
            raise ValueError(
                "percentile must satisfy 0 <= percentile <= 100."
            )

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        n_observations = dataframe.shape[0]
        n_variables = dataframe.shape[1]

        if n_observations <= n_variables:
            raise ValueError(
                "Robust covariance estimation requires "
                "more complete observations than numeric variables."
            )

        estimator = MinCovDet()

        estimator.fit(

            dataframe

        )

        distance = estimator.mahalanobis(

            dataframe

        )

        threshold = np.percentile(

            distance,

            percentile

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
# FEATURE BAGGING
# ==========================================================

class FeatureBaggingOutlier(BaseOutlierDetector):

    """
    Wrapper PyOD.
    """

    name = "Feature Bagging"

    method_family = "ensemble"

    score_type = "pyod_decision_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        try:
            from pyod.models.feature_bagging import (
                FeatureBagging
            )
        except ModuleNotFoundError as exc:
            raise ImportError(
                "PyOD is required for FeatureBaggingOutlier. "
                "Install it with: pip install pyod"
            ) from exc

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = FeatureBagging(

            contamination=contamination

        )

        model.fit(

            dataframe

        )

        labels = model.labels_

        scores = model.decision_scores_

        indices = dataframe.index[

            labels == 1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            labels=labels,

            scores=scores

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# AUTOENCODER
# ==========================================================

class AutoEncoderOutlier(BaseOutlierDetector):

    """
    Placeholder.

    Une implémentation TensorFlow/PyTorch
    sera ajoutée dans EMIDAF ML.
    """

    name = "AutoEncoder"

    method_family = "neural_network"

    score_type = "reconstruction_error"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        **kwargs,

    ):

        raise NotImplementedError(

            "AutoEncoder "

            "sera disponible "

            "dans EMIDAF Machine Learning."

        )


# ==========================================================
# MINIMUM COVARIANCE
# ==========================================================

class MinimumCovarianceDeterminant(BaseOutlierDetector):

    name = "Minimum Covariance Determinant"

    method_family = "covariance"

    score_type = "squared_robust_mahalanobis_distance"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        dataframe,

        percentile=97.5,

    ):

        if not 0 <= percentile <= 100:
            raise ValueError(
                "percentile must satisfy 0 <= percentile <= 100."
            )

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        n_observations = dataframe.shape[0]
        n_variables = dataframe.shape[1]

        if n_observations <= n_variables:
            raise ValueError(
                "Minimum Covariance Determinant requires "
                "more complete observations than numeric variables."
            )

        estimator = MinCovDet()

        estimator.fit(

            dataframe

        )

        score = estimator.mahalanobis(

            dataframe

        )

        threshold = np.percentile(

            score,

            percentile

        )

        indices = dataframe.index[

            score > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=score,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class MultivariateOutlierDetector:

    """
    Lance tous les détecteurs
    multivariés.
    """

    @staticmethod
    def compute(
        dataframe,
    ):

        results = {
            "pca":
                PCAOutlier.detect(
                    dataframe
                ),

            "robust_pca":
                RobustPCAOutlier.detect(
                    dataframe
                ),

            "minimum_covariance":
                MinimumCovarianceDeterminant.detect(
                    dataframe
                ),
        }

        try:
            results["feature_bagging"] = (
                FeatureBaggingOutlier.detect(
                    dataframe
                )
            )

        except ImportError:
            pass

        return results
