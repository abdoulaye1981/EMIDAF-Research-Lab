"""
=========================================================
EMIDAF Framework
Categorical Encoding
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    OrdinalEncoder,
    OneHotEncoder
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# ENCODING
# ==========================================================

class Encoding(
    BasePreprocessing
):

    """
    Complete categorical encoding engine.
    """

    name = "Encoding"

    def __init__(
        self,
        method="onehot"
    ):

        self.method = method
        self.encoder = None
        self.columns = None
        self.feature_names = None
        self.result = None


    @staticmethod

    def categorical_columns(
        df
    ):

        return list(
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )
    @staticmethod
    def label_encode(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Encoding.categorical_columns(
                result
            )

        encoders = {}

        for column in columns:

            encoder = LabelEncoder()

            values = (
                result[column]
                .fillna("__MISSING__")
                .astype(str)
            )

            result[column] = encoder.fit_transform(
                values
            )

            encoders[column] = encoder

        return result, encoders

    @staticmethod
    @staticmethod
    def onehot_encode(
        df,
        columns=None
    ):
        """
        Encode les variables catégorielles
        par one-hot encoding.

        Retourne
        --------
        result : pandas.DataFrame
            Jeu de données transformé.

        encoder : OneHotEncoder | None
            Encodeur ajusté. None lorsqu'aucune
            variable catégorielle n'est disponible.
        """

        if not isinstance(
            df,
            pd.DataFrame
        ):
            raise TypeError(
                "df must be a pandas DataFrame."
            )

        result = df.copy()

        if columns is None:
            columns = (
                Encoding.categorical_columns(
                    result
                )
            )
        else:
            columns = list(columns)

        if not columns:
            return result, None

        missing = [
            column
            for column in columns
            if column not in result.columns
        ]

        if missing:
            raise KeyError(
                "Unknown columns: "
                + ", ".join(missing)
            )

        encoder = OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False
        )

        values = (
            result[columns]
            .fillna("__MISSING__")
            .astype(str)
        )

        encoded = encoder.fit_transform(
            values
        )

        feature_names = list(
            encoder.get_feature_names_out(
                columns
            )
        )

        encoded_df = pd.DataFrame(
            encoded,
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

        return result, encoder

    def ordinal_encode(
        df,
        columns=None,
        categories=None
    ):

        result = df.copy()

        if columns is None:

            columns = Encoding.categorical_columns(
                result
            )

        if not columns:

            return result, None

        encoder = OrdinalEncoder(
            categories=categories,
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        result[columns] = encoder.fit_transform(
            result[columns].fillna(
                "__MISSING__"
            )
        )

        return result, encoder

    @staticmethod
    def frequency_encode(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Encoding.categorical_columns(
                result
            )

        mappings = {}

        for column in columns:

            frequencies = (
                result[column]
                .fillna("__MISSING__")
                .value_counts(
                    normalize=True
                )
            )

            result[column] = (
                result[column]
                .fillna("__MISSING__")
                .map(frequencies)
            )

            mappings[column] = frequencies.to_dict()

        return result, mappings

    @staticmethod
    def target_encode(
        df,
        target,
        columns=None,
        smoothing=10
    ):

        result = df.copy()

        if target not in result.columns:

            raise KeyError(
                f"La variable cible '{target}' "
                "n'existe pas."
            )

        if columns is None:

            columns = Encoding.categorical_columns(
                result
            )

        global_mean = result[target].mean()

        mappings = {}

        for column in columns:

            statistics = (
                result
                .groupby(
                    column,
                    dropna=False
                )[target]
                .agg(
                    ["mean", "count"]
                )
            )

            smoothing_factor = (
                statistics["count"]
                /
                (
                    statistics["count"]
                    + smoothing
                )
            )

            encoded_values = (
                global_mean
                * (1 - smoothing_factor)
                +
                statistics["mean"]
                * smoothing_factor
            )

            mapping = encoded_values.to_dict()

            result[column] = (
                result[column]
                .map(mapping)
                .fillna(global_mean)
            )

            mappings[column] = mapping

        return result, mappings

    @staticmethod
    def binary_encode(
        df,
        columns=None
    ):

        result = df.copy()

        if columns is None:

            columns = Encoding.categorical_columns(
                result
            )

        for column in columns:

            categories = (
                result[column]
                .fillna("__MISSING__")
                .astype("category")
            )

            codes = categories.cat.codes

            max_value = max(
                int(codes.max()),
                1
            )

            n_bits = max(
                1,
                int(
                    np.ceil(
                        np.log2(
                            max_value + 1
                        )
                    )
                )
            )

            for bit in range(n_bits):

                result[
                    f"{column}_bit_{bit}"
                ] = (
                    codes
                    .astype(int)
                    .apply(
                        lambda x:
                        (x >> bit) & 1
                    )
                )

            result = result.drop(
                columns=[column]
            )

        return result

    @staticmethod
    def auto_encode(
        df,
        max_onehot_cardinality=10
    ):

        result = df.copy()

        categorical = (
            Encoding.categorical_columns(
                result
            )
        )

        low_cardinality = [
            column
            for column in categorical
            if result[column].nunique(
                dropna=False
            ) <= max_onehot_cardinality
        ]

        high_cardinality = [
            column
            for column in categorical
            if column not in low_cardinality
        ]

        if low_cardinality:

            result, _ = Encoding.onehot_encode(
                result,
                columns=low_cardinality
            )

        if high_cardinality:

            result, _ = Encoding.frequency_encode(
                result,
                columns=high_cardinality
            )

        return result

    def fit(
        self,
        X,
        y=None
    ):

        self.columns = (
            Encoding.categorical_columns(X)
        )

        if self.method == "onehot":

            self.encoder = OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )

            if self.columns:

                self.encoder.fit(
                    X[self.columns].fillna(
                        "__MISSING__"
                    )
                )

                self.feature_names = (
                    self.encoder
                    .get_feature_names_out(
                        self.columns
                    )
                )

        elif self.method == "ordinal":

            self.encoder = OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1
            )

            if self.columns:

                self.encoder.fit(
                    X[self.columns].fillna(
                        "__MISSING__"
                    )
                )

        else:

            raise ValueError(
                "Méthode inconnue. "
                "Utiliser 'onehot' ou 'ordinal'."
            )

        return self

    def transform(
        self,
        X
    ):

        result = X.copy()

        if not self.columns:

            return result

        values = (
            result[self.columns]
            .fillna("__MISSING__")
        )

        if self.method == "onehot":

            encoded = self.encoder.transform(
                values
            )

            encoded_df = pd.DataFrame(
                encoded,
                columns=self.feature_names,
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

        elif self.method == "ordinal":

            result[self.columns] = (
                self.encoder.transform(
                    values
                )
            )

        return result

    @staticmethod
    def inspect(
        df
    ):

        columns = Encoding.categorical_columns(
            df
        )

        cardinality = {
            column:
            int(
                df[column]
                .nunique(
                    dropna=False
                )
            )
            for column in columns
        }

        result = PreprocessingResult(

            step="Encoding",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=columns

        )

        result.statistics = {

            "categorical_columns":
                columns,

            "cardinality":
                cardinality,

            "low_cardinality":
                [
                    c
                    for c in columns
                    if cardinality[c] <= 10
                ],

            "high_cardinality":
                [
                    c
                    for c in columns
                    if cardinality[c] > 10
                ]

        }

        return result

    # ==========================================================
# PUBLIC API
# ==========================================================

class Encoder:

    categorical_columns = (
        Encoding.categorical_columns
    )

    label = Encoding.label_encode

    ordinal = Encoding.ordinal_encode

    onehot = Encoding.onehot_encode

    frequency = Encoding.frequency_encode

    target = Encoding.target_encode

    binary = Encoding.binary_encode

    auto = Encoding.auto_encode

    inspect = Encoding.inspect
