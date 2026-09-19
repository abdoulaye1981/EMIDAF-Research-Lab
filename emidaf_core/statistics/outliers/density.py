"""
=========================================================
EMIDAF Framework
Density Based Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détecteurs d'anomalies basés sur la densité.

Contient

- Local Outlier Factor
- DBSCAN
- OPTICS

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS

from sklearn.neighbors import LocalOutlierFactor

from .base import BaseOutlierDetector


# ==========================================================
# LOCAL OUTLIER FACTOR
# ==========================================================

class LOF(BaseOutlierDetector):

    name = "Local Outlier Factor"

    method_family = "density"

    score_type = "local_outlier_factor"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        n_neighbors=20,

        contamination="auto",

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = LocalOutlierFactor(

            n_neighbors=n_neighbors,

            contamination=contamination

        )

        labels = model.fit_predict(

            dataframe

        )

        scores = -model.negative_outlier_factor_

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            scores=scores,

            labels=labels,

            parameters={

                "n_neighbors": n_neighbors,

                "contamination": contamination

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# DBSCAN
# ==========================================================

class DBSCANOutlier(BaseOutlierDetector):

    name = "DBSCAN"

    method_family = "density"

    score_type = ""

    score_direction = "none"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        eps=0.5,

        min_samples=5,

    ):

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = DBSCAN(

            eps=eps,

            min_samples=min_samples

        )

        labels = model.fit_predict(

            dataframe

        )

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            labels=labels,

            parameters={

                "eps": eps,

                "min_samples": min_samples

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# OPTICS
# ==========================================================

class OPTICSOutlier(BaseOutlierDetector):

    name = "OPTICS"

    method_family = "density"

    score_type = ""

    score_direction = "none"

    scaling_sensitive = True

    @classmethod
    def detect(

        cls,

        dataframe,

        min_samples=5,

        xi=0.05,

    ):

        if not 0 < xi < 1:
            raise ValueError(
                "xi must satisfy 0 < xi < 1."
            )

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        model = OPTICS(

            min_samples=min_samples,

            xi=xi

        )

        labels = model.fit_predict(

            dataframe

        )

        indices = dataframe.index[

            labels == -1

        ]

        return cls.build_result(

            dataframe.index,

            indices,

            labels=labels,

            parameters={

                "min_samples": min_samples,

                "xi": xi

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class DensityOutlierDetector:

    """
    Lance tous les détecteurs
    basés sur la densité.
    """

    @staticmethod
    def compute(

        dataframe,

    ):

        return {

            "lof":

                LOF.detect(

                    dataframe

                ),

            "dbscan":

                DBSCANOutlier.detect(

                    dataframe

                ),

            "optics":

                OPTICSOutlier.detect(

                    dataframe

                )

        }
