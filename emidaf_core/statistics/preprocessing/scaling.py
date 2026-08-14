"""
=========================================================
EMIDAF Framework
Preprocessing - Scaling
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class StandardScalerPreprocessor:

    name = "Standard Scaler"

    def __init__(
        self,
        columns=None
    ):

        self.columns = columns
        self.columns_ = None
        self.mean_ = {}
        self.scale_ = {}
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        for column in self.columns_:

            self.mean_[column] = X[column].mean()

            std = X[column].std()

            self.scale_[column] = (
                std if std != 0 else 1
            )

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            data[column] = (
                data[column]
                - self.mean_[column]
            ) / self.scale_[column]

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class MinMaxScalerPreprocessor:

    name = "Min Max Scaler"

    def __init__(
        self,
        columns=None,
        feature_range=(0, 1)
    ):

        self.columns = columns
        self.feature_range = feature_range

        self.columns_ = None
        self.min_ = {}
        self.max_ = {}
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        for column in self.columns_:

            self.min_[column] = X[column].min()

            self.max_[column] = X[column].max()

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        low, high = self.feature_range

        for column in self.columns_:

            minimum = self.min_[column]
            maximum = self.max_[column]

            denominator = (
                maximum - minimum
            )

            if denominator == 0:

                data[column] = low

            else:

                data[column] = (
                    (
                        data[column]
                        - minimum
                    )
                    / denominator
                    * (high - low)
                    + low
                )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class RobustScalerPreprocessor:

    name = "Robust Scaler"

    def __init__(
        self,
        columns=None
    ):

        self.columns = columns
        self.columns_ = None
        self.median_ = {}
        self.iqr_ = {}
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        for column in self.columns_:

            q1 = X[column].quantile(0.25)

            q3 = X[column].quantile(0.75)

            iqr = q3 - q1

            self.median_[column] = (
                X[column].median()
            )

            self.iqr_[column] = (
                iqr if iqr != 0 else 1
            )

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            data[column] = (
                (
                    data[column]
                    - self.median_[column]
                )
                / self.iqr_[column]
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class MaxAbsScalerPreprocessor:

    name = "Max Abs Scaler"

    def __init__(
        self,
        columns=None
    ):

        self.columns = columns
        self.columns_ = None
        self.max_abs_ = {}
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        for column in self.columns_:

            value = (
                X[column]
                .abs()
                .max()
            )

            self.max_abs_[column] = (
                value if value != 0 else 1
            )

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            data[column] = (
                data[column]
                / self.max_abs_[column]
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class NormalizerPreprocessor:

    name = "Normalizer"

    def __init__(
        self,
        columns=None,
        norm="l2"
    ):

        self.columns = columns
        self.norm = norm
        self.columns_ = None
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:
            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(self.columns, str):
            return [self.columns]

        return list(self.columns)

    def fit(self, X, y=None):

        self.columns_ = self._get_columns(X)

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        values = data[
            self.columns_
        ].astype(float)

        if self.norm == "l1":

            denominator = (
                values.abs()
                .sum(axis=1)
            )

        elif self.norm == "max":

            denominator = (
                values.abs()
                .max(axis=1)
            )

        else:

            denominator = np.sqrt(
                (
                    values ** 2
                ).sum(axis=1)
            )

        denominator = denominator.replace(
            0,
            1
        )

        data[
            self.columns_
        ] = values.div(
            denominator,
            axis=0
        )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


def standardize(
    X,
    columns=None
):

    scaler = StandardScalerPreprocessor(
        columns=columns
    )

    return scaler.fit_transform(X)


def minmax_scale(
    X,
    columns=None,
    feature_range=(0, 1)
):

    scaler = MinMaxScalerPreprocessor(
        columns=columns,
        feature_range=feature_range
    )

    return scaler.fit_transform(X)


def robust_scale(
    X,
    columns=None
):

    scaler = RobustScalerPreprocessor(
        columns=columns
    )

    return scaler.fit_transform(X)


def maxabs_scale(
    X,
    columns=None
):

    scaler = MaxAbsScalerPreprocessor(
        columns=columns
    )

    return scaler.fit_transform(X)


def normalize(
    X,
    columns=None,
    norm="l2"
):

    scaler = NormalizerPreprocessor(
        columns=columns,
        norm=norm
    )

    return scaler.fit_transform(X)
