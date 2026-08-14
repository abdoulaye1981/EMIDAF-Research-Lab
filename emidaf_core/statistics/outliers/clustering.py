"""
=========================================================
EMIDAF Framework
Clustering Based Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détecteurs d'anomalies basés sur le clustering.

Contient

- KMeans
- MiniBatchKMeans
- Birch
- Gaussian Mixture Model

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import Birch

from sklearn.mixture import GaussianMixture

from .base import BaseOutlierDetector


# ==========================================================
# KMEANS
# ==========================================================

class KMeansOutlier(BaseOutlierDetector):

    name = "KMeans"

    @classmethod
    def detect(

        cls,

        dataframe,

        n_clusters=3,

        percentile=95,

        random_state=42,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = KMeans(

            n_clusters=n_clusters,

            random_state=random_state,

            n_init="auto"

        )

        labels = model.fit_predict(dataframe)

        centers = model.cluster_centers_

        distances = np.linalg.norm(

            dataframe.values -

            centers[labels],

            axis=1

        )

        threshold = np.percentile(

            distances,

            percentile

        )

        indices = dataframe.index[

            distances > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=distances,

            labels=labels,

            threshold=threshold,

            parameters={

                "clusters": n_clusters,

                "percentile": percentile

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# MINI BATCH KMEANS
# ==========================================================

class MiniBatchKMeansOutlier(BaseOutlierDetector):

    name = "MiniBatchKMeans"

    @classmethod
    def detect(

        cls,

        dataframe,

        n_clusters=3,

        percentile=95,

        random_state=42,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = MiniBatchKMeans(

            n_clusters=n_clusters,

            random_state=random_state

        )

        labels = model.fit_predict(dataframe)

        centers = model.cluster_centers_

        distances = np.linalg.norm(

            dataframe.values -

            centers[labels],

            axis=1

        )

        threshold = np.percentile(

            distances,

            percentile

        )

        indices = dataframe.index[

            distances > threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=distances,

            labels=labels,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# BIRCH
# ==========================================================

class BirchOutlier(BaseOutlierDetector):

    name = "Birch"

    @classmethod
    def detect(

        cls,

        dataframe,

        threshold=0.5,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = Birch(

            threshold=threshold

        )

        labels = model.fit_predict(

            dataframe

        )

        unique, counts = np.unique(

            labels,

            return_counts=True

        )

        small_clusters = unique[

            counts < 5

        ]

        indices = dataframe.index[

            np.isin(

                labels,

                small_clusters

            )

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            labels=labels,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# GAUSSIAN MIXTURE MODEL
# ==========================================================

class GaussianMixtureOutlier(BaseOutlierDetector):

    name = "Gaussian Mixture"

    @classmethod
    def detect(

        cls,

        dataframe,

        n_components=3,

        percentile=5,

        random_state=42,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = GaussianMixture(

            n_components=n_components,

            random_state=random_state

        )

        model.fit(dataframe)

        probability = model.score_samples(

            dataframe

        )

        threshold = np.percentile(

            probability,

            percentile

        )

        indices = dataframe.index[

            probability < threshold

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=probability,

            threshold=threshold,

            parameters={

                "components": n_components

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class ClusteringOutlierDetector:

    """
    Lance tous les détecteurs
    basés sur le clustering.
    """

    @staticmethod
    def compute(

        dataframe,

    ):

        return {

            "kmeans":

                KMeansOutlier.detect(

                    dataframe

                ),

            "mini_batch":

                MiniBatchKMeansOutlier.detect(

                    dataframe

                ),

            "birch":

                BirchOutlier.detect(

                    dataframe

                ),

            "gaussian_mixture":

                GaussianMixtureOutlier.detect(

                    dataframe

                )

        }