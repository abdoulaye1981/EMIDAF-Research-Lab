"""
=========================================================
EMIDAF Framework
Feature Engineering
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from itertools import combinations

from sklearn.preprocessing import PolynomialFeatures

from .base import (
    BasePreprocessing,
    PreprocessingResult
)
# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

class FeatureEngineering(
    BasePreprocessing
):

    """
    Complete feature engineering engine.
    """

    name = "Feature Engineering"

    def __init__(
        self,
        method=None
    ):

        self.method = method
        self.transformer = None
        self.features = None
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
# RATIO
# ==========================================================

    @staticmethod
    def ratio(
        df,
        numerator,
        denominator,
        new_name=None,
        zero_value=np.nan
    ):

        result = df.copy()

        if numerator not in result.columns:

            raise KeyError(
                f"Variable absente : {numerator}"
            )

        if denominator not in result.columns:

            raise KeyError(
                f"Variable absente : {denominator}"
            )

        if new_name is None:

            new_name = (
                f"{numerator}_sur_{denominator}"
            )

        denominator_values = (
            result[denominator]
        )

        result[new_name] = np.where(

            denominator_values == 0,

            zero_value,

            result[numerator]
            / denominator_values

        )

        return result
    # ==========================================================
# DIFFERENCE
# ==========================================================

    @staticmethod
    def difference(
        df,
        variable1,
        variable2,
        new_name=None
    ):

        result = df.copy()

        if variable1 not in result.columns:
            raise KeyError(
                f"Variable absente : {variable1}"
            )

        if variable2 not in result.columns:
            raise KeyError(
                f"Variable absente : {variable2}"
            )

        if new_name is None:

            new_name = (
                f"{variable1}_moins_{variable2}"
            )

        result[new_name] = (
            result[variable1]
            - result[variable2]
        )

        return result
    # ==========================================================
# SUM
# ==========================================================

    @staticmethod
    def sum_features(
        df,
        columns,
        new_name="somme"
    ):

        result = df.copy()

        missing = [
            column
            for column in columns
            if column not in result.columns
        ]

        if missing:

            raise KeyError(
                f"Variables absentes : {missing}"
            )

        result[new_name] = (
            result[columns]
            .sum(axis=1)
        )

        return result
    # ==========================================================
# MEAN
# ==========================================================

    @staticmethod
    def mean_features(
        df,
        columns,
        new_name="moyenne"
    ):

        result = df.copy()

        missing = [
            column
            for column in columns
            if column not in result.columns
        ]

        if missing:

            raise KeyError(
                f"Variables absentes : {missing}"
            )

        result[new_name] = (
            result[columns]
            .mean(axis=1)
        )

        return result
    # ==========================================================
# MINIMUM
# ==========================================================

    @staticmethod
    def min_feature(
        df,
        columns,
        new_name="minimum"
    ):

        result = df.copy()

        result[new_name] = (
            result[columns]
            .min(axis=1)
        )

        return result


# ==========================================================
# MAXIMUM
# ==========================================================

    @staticmethod
    def max_feature(
        df,
        columns,
        new_name="maximum"
    ):

        result = df.copy()

        result[new_name] = (
            result[columns]
            .max(axis=1)
        )

        return result
    # ==========================================================
# RANGE
# ==========================================================

    @staticmethod
    def range_feature(
        df,
        columns,
        new_name="etendue"
    ):

        result = df.copy()

        result[new_name] = (
            result[columns].max(axis=1)
            -
            result[columns].min(axis=1)
        )

        return result
    # ==========================================================
# PRODUCT
# ==========================================================

    @staticmethod
    def product(
        df,
        variable1,
        variable2,
        new_name=None
    ):

        result = df.copy()

        if new_name is None:

            new_name = (
                f"{variable1}_x_{variable2}"
            )

        result[new_name] = (
            result[variable1]
            * result[variable2]
        )

        return result
    # ==========================================================
# INTERACTIONS
# ==========================================================

    @staticmethod
    def interactions(
        df,
        columns,
        degree=2,
        include_original=True
    ):

        result = df.copy()

        missing = [
            column
            for column in columns
            if column not in result.columns
        ]

        if missing:

            raise KeyError(
                f"Variables absentes : {missing}"
            )

        polynomial = PolynomialFeatures(

            degree=degree,

            include_bias=False

        )

        transformed = polynomial.fit_transform(
            result[columns]
        )

        feature_names = (
            polynomial
            .get_feature_names_out(
                columns
            )
        )

        engineered = pd.DataFrame(

            transformed,

            columns=feature_names,

            index=result.index

        )

        if include_original:

            new_columns = [
                column
                for column in engineered.columns
                if column not in columns
            ]

            result = pd.concat(
                [
                    result,
                    engineered[new_columns]
                ],
                axis=1
            )

        else:

            result = pd.concat(
                [
                    result.drop(
                        columns=columns
                    ),
                    engineered
                ],
                axis=1
            )

        return result
    # ==========================================================
# POLYNOMIAL FEATURES
# ==========================================================

    @staticmethod
    def polynomial(
        df,
        columns,
        degree=2,
        include_bias=False
    ):

        result = df.copy()

        polynomial = PolynomialFeatures(

            degree=degree,

            include_bias=include_bias

        )

        transformed = (
            polynomial.fit_transform(
                result[columns]
            )
        )

        feature_names = (
            polynomial
            .get_feature_names_out(
                columns
            )
        )

        engineered = pd.DataFrame(

            transformed,

            columns=feature_names,

            index=result.index

        )

        result = result.drop(
            columns=columns
        )

        result = pd.concat(
            [
                result,
                engineered
            ],
            axis=1
        )

        return result, polynomial
    # ==========================================================
# POWER FEATURES
# ==========================================================

    @staticmethod
    def powers(
        df,
        columns,
        powers=(2, 3)
    ):

        result = df.copy()

        for column in columns:

            for power in powers:

                new_name = (
                    f"{column}_puissance_{power}"
                )

                result[new_name] = (
                    result[column] ** power
                )

        return result
    # ==========================================================
# LOG FEATURES
# ==========================================================

    @staticmethod
    def log_features(
        df,
        columns
    ):

        result = df.copy()

        for column in columns:

            minimum = (
                result[column].min()
            )

            shift = (
                abs(minimum) + 1
                if minimum <= 0
                else 0
            )

            new_name = (
                f"log_{column}"
            )

            result[new_name] = np.log(
                result[column] + shift
            )

        return result
    # ==========================================================
# SQRT FEATURES
# ==========================================================

    @staticmethod
    def sqrt_features(
        df,
        columns
    ):

        result = df.copy()

        for column in columns:

            minimum = (
                result[column].min()
            )

            shift = (
                abs(minimum)
                if minimum < 0
                else 0
            )

            new_name = (
                f"sqrt_{column}"
            )

            result[new_name] = np.sqrt(
                result[column] + shift
            )

        return result
    # ==========================================================
# THRESHOLD
# ==========================================================

    @staticmethod
    def threshold(
        df,
        column,
        threshold,
        new_name=None,
        above=1,
        below=0
    ):

        result = df.copy()

        if new_name is None:

            new_name = (
                f"{column}_au_dessus_{threshold}"
            )

        result[new_name] = np.where(

            result[column] >= threshold,

            above,

            below

        )

        return result
    # ==========================================================
# BINARY FEATURES
# ==========================================================

    @staticmethod
    def binary_features(
        df,
        columns,
        thresholds
    ):

        result = df.copy()

        for column in columns:

            if column not in thresholds:

                raise KeyError(
                    f"Seuil absent pour {column}"
                )

            threshold = (
                thresholds[column]
            )

            new_name = (
                f"{column}_binaire"
            )

            result[new_name] = np.where(

                result[column] >= threshold,

                1,

                0

            )

        return result
    # ==========================================================
# COUNT POSITIVE
# ==========================================================

    @staticmethod
    def count_positive(
        df,
        columns,
        new_name="nombre_variables_positives"
    ):

        result = df.copy()

        result[new_name] = (
            result[columns] > 0
        ).sum(axis=1)

        return result
    # ==========================================================
# COUNT MISSING
# ==========================================================

    @staticmethod
    def count_missing(
        df,
        columns=None,
        new_name="nombre_valeurs_manquantes"
    ):

        result = df.copy()

        if columns is None:

            columns = result.columns

        result[new_name] = (
            result[columns]
            .isna()
            .sum(axis=1)
        )

        return result
    # ==========================================================
# MISSING RATE
# ==========================================================

    @staticmethod
    def missing_rate(
        df,
        columns=None,
        new_name="taux_valeurs_manquantes"
    ):

        result = df.copy()

        if columns is None:

            columns = result.columns

        result[new_name] = (
            result[columns]
            .isna()
            .mean(axis=1)
            * 100
        )

        return result
    # ==========================================================
# AUTOMATIC INTERACTIONS
# ==========================================================

    @staticmethod
    def automatic_interactions(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = (
                FeatureEngineering
                .numeric_columns(df)
            )

        for variable1, variable2 in combinations(
            columns,
            2
        ):

            new_name = (
                f"{variable1}_x_{variable2}"
            )

            result[new_name] = (
                result[variable1]
                *
                result[variable2]
            )

        return result
    # ==========================================================
# DATE FEATURES
# ==========================================================

    @staticmethod
    def date_features(
        df,
        date_column,
        prefix=None
    ):

        result = df.copy()

        if date_column not in result.columns:

            raise KeyError(
                f"Variable absente : {date_column}"
            )

        dates = pd.to_datetime(
            result[date_column],
            errors="coerce"
        )

        if prefix is None:

            prefix = date_column

        result[
            f"{prefix}_Annee"
        ] = dates.dt.year

        result[
            f"{prefix}_Mois"
        ] = dates.dt.month

        result[
            f"{prefix}_Jour"
        ] = dates.dt.day

        result[
            f"{prefix}_Jour_Semaine"
        ] = dates.dt.dayofweek

        result[
            f"{prefix}_Semaine"
        ] = dates.dt.isocalendar().week

        result[
            f"{prefix}_Trimestre"
        ] = dates.dt.quarter

        result[
            f"{prefix}_Weekend"
        ] = (
            dates.dt.dayofweek >= 5
        ).astype(int)

        result[
            f"{prefix}_Heure"
        ] = dates.dt.hour

        return result
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.features = (
            FeatureEngineering
            .numeric_columns(X)
        )

        return self
    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        if self.features is None:

            raise RuntimeError(
                "Le moteur doit être ajusté "
                "avec fit()."
            )

        return X.copy()
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        numeric = (
            FeatureEngineering
            .numeric_columns(df)
        )

        result = PreprocessingResult(

            step="Feature Engineering",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=numeric

        )

        result.statistics = {

            "numeric_variables":
                numeric,

            "number_of_numeric_variables":
                len(numeric),

            "number_of_rows":
                len(df)

        }

        return result
# ==========================================================
# PUBLIC API
# ==========================================================

class Engineer:

    numeric_columns = (
        FeatureEngineering.numeric_columns
    )

    ratio = (
        FeatureEngineering.ratio
    )

    difference = (
        FeatureEngineering.difference
    )

    sum = (
        FeatureEngineering.sum_features
    )

    mean = (
        FeatureEngineering.mean_features
    )

    minimum = (
        FeatureEngineering.min_feature
    )

    maximum = (
        FeatureEngineering.max_feature
    )

    range = (
        FeatureEngineering.range_feature
    )

    product = (
        FeatureEngineering.product
    )

    interactions = (
        FeatureEngineering.interactions
    )

    polynomial = (
        FeatureEngineering.polynomial
    )

    powers = (
        FeatureEngineering.powers
    )

    log = (
        FeatureEngineering.log_features
    )

    sqrt = (
        FeatureEngineering.sqrt_features
    )

    threshold = (
        FeatureEngineering.threshold
    )

    binary = (
        FeatureEngineering.binary_features
    )

    count_positive = (
        FeatureEngineering.count_positive
    )

    count_missing = (
        FeatureEngineering.count_missing
    )

    missing_rate = (
        FeatureEngineering.missing_rate
    )

    automatic_interactions = (
        FeatureEngineering
        .automatic_interactions
    )

    date_features = (
        FeatureEngineering.date_features
    )

    inspect = (
        FeatureEngineering.inspect
    )