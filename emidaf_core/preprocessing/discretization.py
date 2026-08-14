"""
=========================================================
EMIDAF Framework
Numerical Discretization
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.preprocessing import KBinsDiscretizer

from .base import (
    BasePreprocessing,
    PreprocessingResult
)
# ==========================================================
# DISCRETIZATION
# ==========================================================

class Discretization(
    BasePreprocessing
):

    """
    Complete numerical discretization engine.
    """

    name = "Discretization"

    def __init__(
        self,
        method="uniform",
        n_bins=5,
        encode="ordinal"
    ):

        self.method = method
        self.n_bins = n_bins
        self.encode = encode

        self.discretizer = None
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
# EQUAL WIDTH
# ==========================================================

    @staticmethod
    def equal_width(
        df,
        columns=None,
        n_bins=5,
        labels=None
    ):

        result = df.copy()

        if columns is None:

            columns = (
                Discretization
                .numeric_columns(df)
            )

        for column in columns:

            result[
                f"{column}_bin"
            ] = pd.cut(

                result[column],

                bins=n_bins,

                labels=labels,

                include_lowest=True

            )

        return result
    # ==========================================================
# EQUAL FREQUENCY
# ==========================================================

    @staticmethod
    def equal_frequency(
        df,
        columns=None,
        n_bins=5,
        labels=None
    ):

        result = df.copy()

        if columns is None:

            columns = (
                Discretization
                .numeric_columns(df)
            )

        for column in columns:

            result[
                f"{column}_bin"
            ] = pd.qcut(

                result[column],

                q=n_bins,

                labels=labels,

                duplicates="drop"

            )

        return result
    # ==========================================================
# CUSTOM BINS
# ==========================================================

    @staticmethod
    def custom_bins(
        df,
        column,
        bins,
        labels=None,
        right=True,
        include_lowest=True
    ):

        result = df.copy()

        if column not in result.columns:

            raise KeyError(
                f"La variable '{column}' "
                "n'existe pas."
            )

        result[
            f"{column}_bin"
        ] = pd.cut(

            result[column],

            bins=bins,

            labels=labels,

            right=right,

            include_lowest=include_lowest

        )

        return result
    # ==========================================================
# KBINS
# ==========================================================

    @staticmethod
    def kbins(
        df,
        columns=None,
        n_bins=5,
        strategy="uniform",
        encode="ordinal"
    ):

        result = df.copy()

        if columns is None:

            columns = (
                Discretization
                .numeric_columns(df)
            )

        if not columns:

            return result, None

        if strategy not in [
            "uniform",
            "quantile",
            "kmeans"
        ]:

            raise ValueError(
                "strategy doit être "
                "'uniform', 'quantile' ou 'kmeans'."
            )

        if encode not in [
            "ordinal",
            "onehot",
            "onehot-dense"
        ]:

            raise ValueError(
                "encode invalide."
            )

        discretizer = KBinsDiscretizer(

            n_bins=n_bins,

            encode=encode,

            strategy=strategy,

            subsample=None

        )

        values = result[columns]

        if values.isna().any().any():

            raise ValueError(
                "Les variables contiennent "
                "des valeurs manquantes."
            )

        transformed = (
            discretizer.fit_transform(
                values
            )
        )

        if encode == "ordinal":

            result[columns] = transformed

        else:

            feature_names = (
                discretizer
                .get_feature_names_out(
                    columns
                )
            )

            encoded_df = pd.DataFrame(

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
                    encoded_df
                ],
                axis=1
            )

        return result, discretizer
    # ==========================================================
# AGE GROUPS
# ==========================================================

    @staticmethod
    def age_groups(
        df,
        column="Age",
        bins=None,
        labels=None
    ):

        result = df.copy()

        if column not in result.columns:

            raise KeyError(
                f"La variable '{column}' "
                "n'existe pas."
            )

        if bins is None:

            bins = [
                0,
                18,
                25,
                35,
                50,
                np.inf
            ]

        if labels is None:

            labels = [
                "Mineur",
                "18-24",
                "25-34",
                "35-49",
                "50+"
            ]

        result[
            f"{column}_Groupe"
        ] = pd.cut(

            result[column],

            bins=bins,

            labels=labels,

            include_lowest=True

        )

        return result
    # ==========================================================
# GRADE GROUPS
# ==========================================================

    @staticmethod
    def grade_groups(
        df,
        column="Moyenne_Generale",
        labels=None
    ):

        result = df.copy()

        if labels is None:

            labels = [
                "Très faible",
                "Faible",
                "Passable",
                "Assez bien",
                "Bien",
                "Très bien"
            ]

        bins = [
            -np.inf,
            5,
            8,
            10,
            12,
            14,
            16,
            np.inf
        ]

        labels = labels[:len(bins) - 1]

        result[
            f"{column}_Categorie"
        ] = pd.cut(

            result[column],

            bins=bins,

            labels=labels,

            include_lowest=True

        )

        return result
    # ==========================================================
# CATEGORY CODES
# ==========================================================

    @staticmethod
    def category_codes(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = list(
                result.select_dtypes(
                    include=[
                        "category"
                    ]
                ).columns
            )

        for column in columns:

            result[column] = (
                result[column]
                .cat.codes
            )

        return result
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.columns = (
            Discretization
            .numeric_columns(X)
        )

        if not self.columns:

            return self

        self.discretizer = (
            KBinsDiscretizer(

                n_bins=self.n_bins,

                encode=self.encode,

                strategy=self.method,

                subsample=None

            )
        )

        values = X[self.columns]

        if values.isna().any().any():

            raise ValueError(
                "Les données contiennent "
                "des valeurs manquantes."
            )

        self.discretizer.fit(
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

        if self.discretizer is None:

            raise RuntimeError(
                "Le discrétiseur doit être "
                "ajusté avec fit()."
            )

        result = X.copy()

        transformed = (
            self.discretizer
            .transform(
                X[self.columns]
            )
        )

        if self.encode == "ordinal":

            result[self.columns] = transformed

        else:

            feature_names = (
                self.discretizer
                .get_feature_names_out(
                    self.columns
                )
            )

            encoded_df = pd.DataFrame(

                transformed,

                columns=feature_names,

                index=result.index

            )

            result = result.drop(
                columns=self.columns
            )

            result = pd.concat(
                [
                    result,
                    encoded_df
                ],
                axis=1
            )

        return result
    # ==========================================================
# BIN STATISTICS
# ==========================================================

    @staticmethod
    def bin_statistics(
        df,
        column
    ):

        if column not in df.columns:

            raise KeyError(
                f"La variable '{column}' "
                "n'existe pas."
            )

        series = df[column]

        if not pd.api.types.is_categorical_dtype(
            series
        ):

            raise TypeError(
                "La variable doit être "
                "catégorielle."
            )

        counts = (
            series
            .value_counts(
                dropna=False
            )
            .sort_index()
        )

        percentages = (
            counts
            / len(series)
            * 100
        )

        return pd.DataFrame({

            "effectif": counts,

            "pourcentage": percentages

        })
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        columns = (
            Discretization
            .numeric_columns(df)
        )

        result = PreprocessingResult(

            step="Discretization",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=columns

        )

        result.statistics = {

            "numeric_columns":
                columns,

            "number_of_numeric_variables":
                len(columns)

        }

        return result
# ==========================================================
# PUBLIC API
# ==========================================================

class Discretizer:

    numeric_columns = (
        Discretization.numeric_columns
    )

    equal_width = (
        Discretization.equal_width
    )

    equal_frequency = (
        Discretization.equal_frequency
    )

    custom_bins = (
        Discretization.custom_bins
    )

    kbins = (
        Discretization.kbins
    )

    age_groups = (
        Discretization.age_groups
    )

    grade_groups = (
        Discretization.grade_groups
    )

    category_codes = (
        Discretization.category_codes
    )

    bin_statistics = (
        Discretization.bin_statistics
    )

    inspect = Discretization.inspect