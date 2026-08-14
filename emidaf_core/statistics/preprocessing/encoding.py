"""
=========================================================
EMIDAF Framework
Preprocessing - Encoding
=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np


class OneHotEncoderPreprocessor:

    name = "One Hot Encoder"

    def __init__(
        self,
        columns=None,
        drop_first=False,
        dtype=int,
        handle_unknown="ignore"
    ):

        self.columns = columns
        self.drop_first = drop_first
        self.dtype = dtype
        self.handle_unknown = handle_unknown

        self.columns_ = None
        self.categories_ = {}
        self.feature_names_out_ = None
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=[
                        "object",
                        "category",
                        "bool"
                    ]
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        self.categories_ = {}

        for column in self.columns_:

            self.categories_[column] = list(
                X[column]
                .dropna()
                .unique()
            )

        self.feature_names_out_ = list(
            pd.get_dummies(
                X,
                columns=self.columns_,
                drop_first=self.drop_first,
                dtype=self.dtype
            ).columns
        )

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        data = pd.get_dummies(
            data,
            columns=self.columns_,
            drop_first=self.drop_first,
            dtype=self.dtype
        )

        for column in self.feature_names_out_:

            if column not in data.columns:
                data[column] = 0

        data = data[
            self.feature_names_out_
        ]

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)

    def get_feature_names_out(self):

        return self.feature_names_out_


class OrdinalEncoderPreprocessor:

    name = "Ordinal Encoder"

    def __init__(
        self,
        columns=None,
        unknown_value=-1
    ):

        self.columns = columns
        self.unknown_value = unknown_value

        self.columns_ = None
        self.mapping_ = {}
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:

            return list(
                X.select_dtypes(
                    include=[
                        "object",
                        "category",
                        "bool"
                    ]
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        self.mapping_ = {}

        for column in self.columns_:

            categories = (
                X[column]
                .dropna()
                .unique()
            )

            self.mapping_[column] = {
                value: index
                for index, value
                in enumerate(categories)
            }

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            mapping = self.mapping_[column]

            data[column] = (
                data[column]
                .map(mapping)
                .fillna(self.unknown_value)
                .astype(int)
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class LabelEncoderPreprocessor:

    name = "Label Encoder"

    def __init__(
        self,
        column=None
    ):

        self.column = column
        self.classes_ = None
        self.mapping_ = {}
        self.fitted_ = False

    def fit(self, X, y=None):

        if y is None:

            if self.column is None:
                raise ValueError(
                    "Spécifiez column ou fournissez y."
                )

            series = X[self.column]

        else:

            series = pd.Series(y)

        self.classes_ = list(
            pd.Series(series)
            .dropna()
            .unique()
        )

        self.mapping_ = {
            value: index
            for index, value
            in enumerate(self.classes_)
        }

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        if self.column is None:
            raise ValueError(
                "column doit être spécifié."
            )

        data[self.column] = (
            data[self.column]
            .map(self.mapping_)
        )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class BinaryEncoder:

    name = "Binary Encoder"

    def __init__(
        self,
        column
    ):

        self.column = column
        self.mapping_ = {}
        self.fitted_ = False

    def fit(self, X, y=None):

        values = list(
            X[self.column]
            .dropna()
            .unique()
        )

        self.mapping_ = {
            value: index
            for index, value
            in enumerate(values)
        }

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        data[self.column] = (
            data[self.column]
            .map(self.mapping_)
        )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


def one_hot_encode(
    X,
    columns=None,
    drop_first=False,
    dtype=int
):

    return pd.get_dummies(
        X,
        columns=columns,
        drop_first=drop_first,
        dtype=dtype
    )


def ordinal_encode(
    X,
    columns
):

    data = X.copy()

    if isinstance(columns, str):
        columns = [columns]

    for column in columns:

        categories = (
            data[column]
            .dropna()
            .unique()
        )

        mapping = {
            value: index
            for index, value
            in enumerate(categories)
        }

        data[column] = (
            data[column]
            .map(mapping)
        )

    return data


def frequency_encode(
    X,
    columns
):

    data = X.copy()

    if isinstance(columns, str):
        columns = [columns]

    for column in columns:

        frequencies = (
            data[column]
            .value_counts(
                normalize=True
            )
        )

        data[column] = (
            data[column]
            .map(frequencies)
        )

    return data


def target_encode(
    X,
    y,
    columns
):

    data = X.copy()

    if isinstance(columns, str):
        columns = [columns]

    target = pd.Series(
        y,
        index=data.index
    )

    global_mean = target.mean()

    for column in columns:

        means = (
            pd.DataFrame({
                "category": data[column],
                "target": target
            })
            .groupby("category")["target"]
            .mean()
        )

        data[column] = (
            data[column]
            .map(means)
            .fillna(global_mean)
        )

    return data


def binary_encode(
    X,
    column
):

    data = X.copy()

    values = list(
        data[column]
        .dropna()
        .unique()
    )

    mapping = {
        value: index
        for index, value
        in enumerate(values)
    }

    data[column] = (
        data[column]
        .map(mapping)
    )

    return data
