"""
=========================================================
EMIDAF Framework
Data Scaling
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    MaxAbsScaler,
    Normalizer
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# SCALING
# ==========================================================

class Scaling(
    BasePreprocessing
):

    """
    Complete numerical scaling engine.
    """

    name = "Scaling"

    def __init__(
        self,
        method="standard"
    ):

        self.method = method
        self.scaler = None
        self.columns = None
        self.result = None

    # ==========================================================
# NUMERIC COLUMNS
# ==========================================================

    @staticmethod
    def numeric_columns(
        df
    ):

        return list(
            df.select_dtypes(
                include=np.number
            ).columns
        )

    # ==========================================================
# CREATE SCALER
# ==========================================================

    @staticmethod
    def create_scaler(
        method="standard",
        **kwargs
    ):

        scalers = {

            "standard":
                StandardScaler,

            "minmax":
                MinMaxScaler,

            "robust":
                RobustScaler,

            "maxabs":
                MaxAbsScaler,

            "normalize":
                Normalizer

        }

        if method not in scalers:

            raise ValueError(
                f"Méthode inconnue : {method}. "
                f"Choisir parmi : "
                f"{list(scalers.keys())}"
            )

        return scalers[method](
            **kwargs
        )
    # ==========================================================
# STANDARD SCALING
# ==========================================================

    @staticmethod
    def standard(
        df,
        columns=None
    ):

        return Scaling.apply(
            df,
            method="standard",
            columns=columns
        )

    # ==========================================================
# MIN MAX
# ==========================================================

    @staticmethod
    def minmax(
        df,
        columns=None,
        feature_range=(0, 1)
    ):

        return Scaling.apply(
            df,
            method="minmax",
            columns=columns,
            feature_range=feature_range
        )
    
    # ==========================================================
# ROBUST
# ==========================================================

    @staticmethod
    def robust(
        df,
        columns=None,
        **kwargs
    ):

        return Scaling.apply(
            df,
            method="robust",
            columns=columns,
            **kwargs
        )

    # ==========================================================
# MAX ABS
# ==========================================================

    @staticmethod
    def maxabs(
        df,
        columns=None
    ):

        return Scaling.apply(
            df,
            method="maxabs",
            columns=columns
        )
    # ==========================================================
# NORMALIZATION
# ==========================================================

    @staticmethod
    def normalize(
        df,
        columns=None,
        norm="l2"
    ):

        return Scaling.apply(
            df,
            method="normalize",
            columns=columns,
            norm=norm
        )
    # ==========================================================
# APPLY
# ==========================================================

    @staticmethod
    def apply(
        df,
        method="standard",
        columns=None,
        **kwargs
    ):

        result = df.copy()

        if columns is None:

            columns = Scaling.numeric_columns(
                result
            )

        columns = list(columns)

        if not columns:

            return result, None

        missing_columns = [
            column
            for column in columns
            if column not in result.columns
        ]

        if missing_columns:

            raise KeyError(
                f"Colonnes inexistantes : "
                f"{missing_columns}"
            )

        scaler = Scaling.create_scaler(
            method,
            **kwargs
        )

        values = result[columns]

        if values.isna().any().any():

            raise ValueError(
                "Les variables à standardiser "
                "contiennent des valeurs manquantes. "
                "Traitez-les avant le scaling."
            )

        result[columns] = scaler.fit_transform(
            values
        )

        return result, scaler

    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.columns = (
            Scaling.numeric_columns(X)
        )

        if not self.columns:

            self.scaler = None

            return self

        self.scaler = Scaling.create_scaler(
            self.method
        )

        values = X[self.columns]

        if values.isna().any().any():

            raise ValueError(
                "Les données contiennent "
                "des valeurs manquantes."
            )

        self.scaler.fit(
            values
        )

        return self

    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        result = X.copy()

        if self.scaler is None:

            return result

        values = X[self.columns]

        result[self.columns] = (
            self.scaler.transform(
                values
            )
        )

        return result

    # ==========================================================
# FIT TRANSFORM
# ==========================================================

    def fit_transform(
        self,
        X,
        y=None
    ):

        self.fit(
            X,
            y
        )

        return self.transform(
            X
        )
    # ==========================================================
# STATISTICS
# ==========================================================

    @staticmethod
    def statistics(
        df,
        columns=None
    ):

        if columns is None:

            columns = Scaling.numeric_columns(
                df
            )

        statistics = []

        for column in columns:

            series = df[column]

            statistics.append({

                "variable":
                    column,

                "mean":
                    series.mean(),

                "std":
                    series.std(),

                "min":
                    series.min(),

                "median":
                    series.median(),

                "max":
                    series.max(),

                "q1":
                    series.quantile(0.25),

                "q3":
                    series.quantile(0.75)

            })

        return pd.DataFrame(
            statistics
        )
    # ==========================================================
# COMPARE
# ==========================================================

    @staticmethod
    def compare(
        df,
        columns=None
    ):

        if columns is None:

            columns = Scaling.numeric_columns(
                df
            )

        methods = [
            "standard",
            "minmax",
            "robust",
            "maxabs"
        ]

        results = {}

        for method in methods:

            scaled, _ = Scaling.apply(
                df,
                method=method,
                columns=columns
            )

            results[method] = (
                scaled[columns]
            )

        return results
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        columns = Scaling.numeric_columns(
            df
        )

        result = PreprocessingResult(

            step="Scaling",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=columns

        )

        result.statistics = {

            "numeric_columns":
                columns,

            "before":
                Scaling.statistics(
                    df,
                    columns
                )

        }

        return result


# ==========================================================
# PUBLIC API
# ==========================================================

class Scaler:

    numeric_columns = (
        Scaling.numeric_columns
    )

    standard = Scaling.standard

    minmax = Scaling.minmax

    robust = Scaling.robust

    maxabs = Scaling.maxabs

    normalize = Scaling.normalize

    apply = Scaling.apply

    compare = Scaling.compare

    statistics = Scaling.statistics

    inspect = Scaling.inspect