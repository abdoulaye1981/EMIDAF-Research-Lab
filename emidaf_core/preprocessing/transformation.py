"""
=========================================================
EMIDAF Framework
Numerical Data Transformation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import (
    boxcox,
    yeojohnson,
    skew
)

from sklearn.preprocessing import (
    PowerTransformer,
    QuantileTransformer,
    FunctionTransformer
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# TRANSFORMATION
# ==========================================================

class Transformation(
    BasePreprocessing
):

    """
    Complete numerical transformation engine.
    """

    name = "Transformation"

    def __init__(
        self,
        method="yeo_johnson"
    ):

        self.method = method
        self.transformer = None
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
# LOG
# ==========================================================

    @staticmethod
    def log(
        df,
        columns=None,
        offset=1.0
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        for column in columns:

            minimum = result[column].min()

            shift = offset

            if minimum <= 0:

                shift += abs(minimum)

            result[column] = np.log(
                result[column] + shift
            )

        return result
    # ==========================================================
# LOG1P
# ==========================================================

    @staticmethod
    def log1p(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        for column in columns:

            minimum = result[column].min()

            if minimum < 0:

                shift = abs(minimum) + 1

            else:

                shift = 0

            result[column] = np.log1p(
                result[column] + shift
            )

        return result
    # ==========================================================
# SQUARE ROOT
# ==========================================================

    @staticmethod
    def sqrt(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        for column in columns:

            minimum = result[column].min()

            shift = (
                abs(minimum)
                if minimum < 0
                else 0
            )

            result[column] = np.sqrt(
                result[column] + shift
            )

        return result
    # ==========================================================
# CUBE ROOT
# ==========================================================

    @staticmethod
    def cube_root(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        for column in columns:

            result[column] = np.cbrt(
                result[column]
            )

        return result
    # ==========================================================
# BOX COX
# ==========================================================

    @staticmethod
    def boxcox(
        df,
        columns=None
    ):

        result = df.copy()
        lambdas = {}

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        for column in columns:

            series = result[column]

            minimum = series.min()

            shift = (
                abs(minimum) + 1
                if minimum <= 0
                else 0
            )

            transformed, lmbda = boxcox(
                series + shift
            )

            result[column] = transformed

            lambdas[column] = {
                "lambda": lmbda,
                "shift": shift
            }

        return result, lambdas
    # ==========================================================
# YEO JOHNSON
# ==========================================================

    @staticmethod
    def yeo_johnson(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        transformer = PowerTransformer(
            method="yeo-johnson",
            standardize=False
        )

        values = result[columns]

        if values.isna().any().any():

            raise ValueError(
                "Les données contiennent "
                "des valeurs manquantes."
            )

        result[columns] = (
            transformer.fit_transform(
                values
            )
        )

        return result, transformer
    # ==========================================================
# QUANTILE
# ==========================================================

    @staticmethod
    def quantile(
        df,
        columns=None,
        output_distribution="normal",
        n_quantiles=1000
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        n_quantiles = min(
            n_quantiles,
            len(result)
        )

        transformer = QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution=output_distribution,
            random_state=42
        )

        values = result[columns]

        if values.isna().any().any():

            raise ValueError(
                "Les données contiennent "
                "des valeurs manquantes."
            )

        result[columns] = (
            transformer.fit_transform(
                values
            )
        )

        return result, transformer
    # ==========================================================
# POWER TRANSFORM
# ==========================================================

    @staticmethod
    def power(
        df,
        columns=None,
        method="yeo-johnson",
        standardize=False
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        transformer = PowerTransformer(
            method=method,
            standardize=standardize
        )

        values = result[columns]

        if values.isna().any().any():

            raise ValueError(
                "Les données contiennent "
                "des valeurs manquantes."
            )

        result[columns] = (
            transformer.fit_transform(
                values
            )
        )

        return result, transformer
    # ==========================================================
# INVERSE
# ==========================================================

    @staticmethod
    def inverse(
        values,
        transformer
    ):

        return transformer.inverse_transform(
            values
        )
    # ==========================================================
# SKEWNESS
# ==========================================================

    @staticmethod
    def skewness(
        df,
        columns=None
    ):

        if columns is None:

            columns = Transformation.numeric_columns(
                df
            )

        results = []

        for column in columns:

            value = skew(
                df[column].dropna()
            )

            results.append({

                "variable":
                    column,

                "skewness":
                    value,

                "absolute_skewness":
                    abs(value)

            })

        return pd.DataFrame(
            results
        )
    # ==========================================================
# COMPARE
# ==========================================================

    @staticmethod
    def compare(
        df,
        transformed_df,
        columns=None
    ):

        if columns is None:

            columns = Transformation.numeric_columns(
                df
            )

        results = []

        for column in columns:

            before = skew(
                df[column].dropna()
            )

            after = skew(
                transformed_df[column].dropna()
            )

            results.append({

                "variable":
                    column,

                "skewness_before":
                    before,

                "skewness_after":
                    after,

                "improvement":
                    abs(before) - abs(after)

            })

        return pd.DataFrame(
            results
        )
    # ==========================================================
# AUTO TRANSFORM
# ==========================================================

    @staticmethod
    def auto(
        df,
        columns=None,
        threshold=1
    ):

        result = df.copy()

        if columns is None:

            columns = Transformation.numeric_columns(
                result
            )

        decisions = []

        for column in columns:

            series = result[column].dropna()

            original_skew = skew(
                series
            )

            if abs(original_skew) <= threshold:

                decisions.append({

                    "variable": column,

                    "method": "none",

                    "skewness_before":
                        original_skew,

                    "skewness_after":
                        original_skew

                })

                continue

            if (series > 0).all():

                transformed = np.log(
                    series
                )

                method = "log"

            else:

                transformed = yeojohnson(
                    series
                )[0]

                method = "yeo_johnson"

            new_skew = skew(
                transformed
            )

            if abs(new_skew) < abs(
                original_skew
            ):

                if method == "log":

                    minimum = result[
                        column
                    ].min()

                    shift = (
                        0
                        if minimum > 0
                        else abs(minimum) + 1
                    )

                    result[column] = np.log(
                        result[column] + shift
                    )

                else:

                    transformer = PowerTransformer(
                        method="yeo-johnson",
                        standardize=False
                    )

                    result[column] = (
                        transformer
                        .fit_transform(
                            result[
                                [column]
                            ]
                        )
                        .ravel()
                    )

            else:

                method = "none"

            decisions.append({

                "variable": column,

                "method": method,

                "skewness_before":
                    original_skew,

                "skewness_after":
                    new_skew

            })

        return (
            result,
            pd.DataFrame(decisions)
        )
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.columns = (
            Transformation.numeric_columns(X)
        )

        if not self.columns:

            return self

        if X[self.columns].isna().any().any():

            raise ValueError(
                "Les variables numériques "
                "contiennent des valeurs manquantes."
            )

        if self.method in [
            "yeo_johnson",
            "box_cox"
        ]:

            sklearn_method = (
                "yeo-johnson"
                if self.method == "yeo_johnson"
                else "box-cox"
            )

            self.transformer = PowerTransformer(
                method=sklearn_method,
                standardize=False
            )

            self.transformer.fit(
                X[self.columns]
            )

        else:

            raise ValueError(
                "Méthode non supportée pour fit(). "
                "Utiliser 'yeo_johnson' ou 'box_cox'."
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

        if self.transformer is None:

            raise RuntimeError(
                "Le transformateur doit être "
                "ajusté avec fit()."
            )

        result[self.columns] = (
            self.transformer
            .transform(
                X[self.columns]
            )
        )

        return result
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        columns = (
            Transformation.numeric_columns(
                df
            )
        )

        result = PreprocessingResult(

            step="Transformation",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=columns

        )

        result.statistics = {

            "skewness":
                Transformation.skewness(
                    df,
                    columns
                )

        }

        return result
    # ==========================================================
# PUBLIC API
# ==========================================================

class Transformer:

    numeric_columns = (
        Transformation.numeric_columns
    )

    log = Transformation.log

    log1p = Transformation.log1p

    sqrt = Transformation.sqrt

    cube_root = (
        Transformation.cube_root
    )

    boxcox = Transformation.boxcox

    yeo_johnson = (
        Transformation.yeo_johnson
    )

    quantile = Transformation.quantile

    power = Transformation.power

    inverse = Transformation.inverse

    skewness = Transformation.skewness

    compare = Transformation.compare

    auto = Transformation.auto

    inspect = Transformation.inspect