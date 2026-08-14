"""
=========================================================
EMIDAF Framework
Outlier Detection and Treatment
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import zscore

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from scipy.spatial.distance import mahalanobis

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# OUTLIERS
# ==========================================================

class OutlierDetection(
    BasePreprocessing
):

    """
    Complete outlier detection engine.
    """

    name = "Outlier Detection"

    def __init__(
        self,
        method="iqr"
    ):

        self.method = method
        self.result = None

    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.result = self.detect(
            X,
            method=self.method
        )

        return self

    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        if self.result is None:

            raise RuntimeError(
                "Le modèle doit être ajusté avec fit()."
            )

        return X.copy()

    # ==========================================================
# IQR
# ==========================================================

    @staticmethod
    def iqr(
        df,
        multiplier=1.5
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        results = []

        for column in numeric.columns:

            series = numeric[column].dropna()

            if len(series) == 0:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - multiplier * iqr
            upper = q3 + multiplier * iqr

            mask = (
                (numeric[column] < lower)
                |
                (numeric[column] > upper)
            )

            results.append({

                "variable": column,

                "q1": q1,

                "q3": q3,

                "iqr": iqr,

                "lower_bound": lower,

                "upper_bound": upper,

                "outlier_count": int(
                    mask.sum()
                ),

                "outlier_percent": (
                    mask.mean() * 100
                )

            })

        return pd.DataFrame(results)

    # ==========================================================
# Z SCORE
# ==========================================================

    @staticmethod
    def zscore(
        df,
        threshold=3
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        results = []

        for column in numeric.columns:

            series = numeric[column]

            z = pd.Series(
                zscore(
                    series,
                    nan_policy="omit"
                ),
                index=series.index
            )

            mask = z.abs() > threshold

            results.append({

                "variable": column,

                "threshold": threshold,

                "outlier_count": int(
                    mask.sum()
                ),

                "outlier_percent": (
                    mask.mean() * 100
                ),

                "maximum_abs_zscore": (
                    z.abs().max()
                )

            })

        return pd.DataFrame(results)

    # ==========================================================
# MAD
# ==========================================================

    @staticmethod
    def mad(
        df,
        threshold=3.5
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        results = []

        for column in numeric.columns:

            series = numeric[column]

            median = series.median()

            mad = np.median(
                np.abs(
                    series.dropna()
                    - median
                )
            )

            if mad == 0:

                modified_z = pd.Series(
                    0,
                    index=series.index,
                    dtype=float
                )

            else:

                modified_z = (
                    0.6745
                    * (series - median)
                    / mad
                )

            mask = (
                modified_z.abs()
                > threshold
            )

            results.append({

                "variable": column,

                "median": median,

                "mad": mad,

                "threshold": threshold,

                "outlier_count": int(
                    mask.sum()
                ),

                "outlier_percent": (
                    mask.mean() * 100
                )

            })

        return pd.DataFrame(results)

    # ==========================================================
# MAHALANOBIS
# ==========================================================

    @staticmethod
    def mahalanobis_distance(
        df,
        threshold=None
    ):

        numeric = df.select_dtypes(
            include=np.number
        ).dropna()

        if numeric.shape[1] < 2:

            raise ValueError(
                "Au moins deux variables "
                "numériques sont nécessaires."
            )

        values = numeric.values

        mean_vector = np.mean(
            values,
            axis=0
        )

        covariance = np.cov(
            values,
            rowvar=False
        )

        covariance += (
            np.eye(
                covariance.shape[0]
            ) * 1e-10
        )

        inverse_covariance = np.linalg.inv(
            covariance
        )

        distances = np.array([

            mahalanobis(
                row,
                mean_vector,
                inverse_covariance
            )

            for row in values

        ])

        result = pd.DataFrame({

            "index": numeric.index,

            "mahalanobis_distance":
                distances

        })

        if threshold is not None:

            result["outlier"] = (
                distances > threshold
            )

        return result

    # ==========================================================
# ISOLATION FOREST
# ==========================================================

    @staticmethod
    def isolation_forest(
        df,
        contamination="auto",
        random_state=42
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        clean = numeric.dropna()

        if clean.empty:

            return pd.DataFrame()

        model = IsolationForest(

            contamination=contamination,

            random_state=random_state

        )

        prediction = model.fit_predict(
            clean
        )

        score = model.decision_function(
            clean
        )

        result = pd.DataFrame({

            "index": clean.index,

            "anomaly_score": score,

            "outlier": prediction == -1

        })

        return result

    # ==========================================================
# LOF
# ==========================================================

    @staticmethod
    def lof(
        df,
        n_neighbors=20,
        contamination="auto"
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        clean = numeric.dropna()

        if len(clean) <= n_neighbors:

            raise ValueError(
                "n_neighbors doit être inférieur "
                "au nombre d'observations."
            )

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(
            clean
        )

        model = LocalOutlierFactor(

            n_neighbors=n_neighbors,

            contamination=contamination

        )

        prediction = model.fit_predict(
            X_scaled
        )

        score = model.negative_outlier_factor_

        result = pd.DataFrame({

            "index": clean.index,

            "lof_score": score,

            "outlier": prediction == -1

        })

        return result

    # ==========================================================
# DBSCAN
# ==========================================================

    @staticmethod
    def dbscan(
        df,
        eps=0.5,
        min_samples=5
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        clean = numeric.dropna()

        if clean.empty:

            return pd.DataFrame()

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(
            clean
        )

        model = DBSCAN(

            eps=eps,

            min_samples=min_samples

        )

        labels = model.fit_predict(
            X_scaled
        )

        result = pd.DataFrame({

            "index": clean.index,

            "cluster": labels,

            "outlier": labels == -1

        })

        return result

    # ==========================================================
# COMPARE
# ==========================================================

    @staticmethod
    def compare(
        df,
        z_threshold=3,
        iqr_multiplier=1.5,
        mad_threshold=3.5
    ):

        iqr_result = OutlierDetection.iqr(
            df,
            multiplier=iqr_multiplier
        )

        z_result = OutlierDetection.zscore(
            df,
            threshold=z_threshold
        )

        mad_result = OutlierDetection.mad(
            df,
            threshold=mad_threshold
        )

        comparison = pd.DataFrame({

            "variable":
                iqr_result["variable"],

            "IQR":
                iqr_result["outlier_count"],

            "Z_score":
                z_result["outlier_count"],

            "MAD":
                mad_result["outlier_count"]

        })

        return comparison

    # ==========================================================
# IQR MASK
# ==========================================================

    @staticmethod
    def iqr_mask(
        df,
        multiplier=1.5
    ):

        numeric = df.select_dtypes(
            include=np.number
        )

        mask = pd.DataFrame(
            False,
            index=df.index,
            columns=numeric.columns
        )

        for column in numeric.columns:

            q1 = numeric[column].quantile(
                0.25
            )

            q3 = numeric[column].quantile(
                0.75
            )

            iqr = q3 - q1

            lower = (
                q1 - multiplier * iqr
            )

            upper = (
                q3 + multiplier * iqr
            )

            mask[column] = (
                (numeric[column] < lower)
                |
                (numeric[column] > upper)
            )

        return mask

    # ==========================================================
# REMOVE
# ==========================================================

    @staticmethod
    def remove_iqr(
        df,
        multiplier=1.5
    ):

        mask = OutlierDetection.iqr_mask(
            df,
            multiplier
        )

        rows_to_remove = mask.any(
            axis=1
        )

        return df.loc[
            ~rows_to_remove
        ].copy()

    # ==========================================================
# WINSORIZATION
# ==========================================================

    @staticmethod
    def winsorize(
        df,
        lower=0.01,
        upper=0.99
    ):

        result = df.copy()

        numeric = result.select_dtypes(
            include=np.number
        ).columns

        for column in numeric:

            low = result[column].quantile(
                lower
            )

            high = result[column].quantile(
                upper
            )

            result[column] = (
                result[column]
                .clip(
                    lower=low,
                    upper=high
                )
            )

        return result


    # ==========================================================
# DETECT
# ==========================================================

    @staticmethod
    def detect(
        df,
        method="iqr",
        **kwargs
    ):

        methods = {

            "iqr":
                OutlierDetection.iqr,

            "zscore":
                OutlierDetection.zscore,

            "mad":
                OutlierDetection.mad,

            "mahalanobis":
                OutlierDetection.mahalanobis_distance,

            "isolation_forest":
                OutlierDetection.isolation_forest,

            "lof":
                OutlierDetection.lof,

            "dbscan":
                OutlierDetection.dbscan

        }

        if method not in methods:

            raise ValueError(
                f"Méthode inconnue : {method}. "
                f"Choisir parmi : "
                f"{list(methods.keys())}"
            )

        return methods[method](
            df,
            **kwargs
        )

# ==========================================================
# SERVICE
# ==========================================================

class Outliers:

    iqr = OutlierDetection.iqr

    zscore = OutlierDetection.zscore

    mad = OutlierDetection.mad

    mahalanobis = (
        OutlierDetection.mahalanobis_distance
    )

    isolation_forest = (
        OutlierDetection.isolation_forest
    )

    lof = OutlierDetection.lof

    dbscan = OutlierDetection.dbscan

    compare = OutlierDetection.compare

    iqr_mask = OutlierDetection.iqr_mask

    remove_iqr = OutlierDetection.remove_iqr

    winsorize = OutlierDetection.winsorize

    inspect = OutlierDetection.inspect

    detect = OutlierDetection.detect