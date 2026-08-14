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

    @classmethod
    def detect(

        cls,

        dataframe,

        n_components=2,

        percentile=95,

    ):

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

    @classmethod
    def detect(

        cls,

        dataframe,

        percentile=97.5,

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

    @classmethod
    def detect(

        cls,

        dataframe,

        contamination=0.05,

    ):

        from pyod.models.feature_bagging import (

            FeatureBagging

        )

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

    @classmethod
    def detect(

        cls,

        dataframe,

        percentile=97.5,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

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

        return {

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

            "feature_bagging":

                FeatureBaggingOutlier.detect(

                    dataframe

                )

        }