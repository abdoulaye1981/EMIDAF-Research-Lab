"""
=========================================================
EMIDAF Framework
Preprocessing - Transformations
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class Transformer:

    name = "Transformer"

    def __init__(
        self,
        method="standard",
        columns=None
    ):

        self.method = method
        self.columns = columns
        self.columns_ = None
        self.fitted_ = False

    def _get_columns(self, X):

        if self.columns is None:

            return list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        if isinstance(
            self.columns,
            str
        ):

            return [self.columns]

        return list(
            self.columns
        )

    def fit(
        self,
        X,
        y=None
    ):

        self.columns_ = self._get_columns(X)

        self.fitted_ = True

        return self

    def transform(
        self,
        X
    ):

        if not self.fitted_:

            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            data[column] = self._transform_series(
                data[column]
            )

        return data

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

    def _transform_series(
        self,
        series
    ):

        if self.method == "log":

            return np.log1p(
                series
            )

        if self.method == "log10":

            return np.log10(
                series
            )

        if self.method == "sqrt":

            return np.sqrt(
                series.clip(lower=0)
            )

        if self.method == "square":

            return series ** 2

        if self.method == "cube":

            return series ** 3

        if self.method == "cbrt":

            return np.cbrt(
                series
            )

        if self.method == "reciprocal":

            return 1 / series.replace(
                0,
                np.nan
            )

        if self.method == "exp":

            return np.exp(
                series
            )

        if self.method == "abs":

            return series.abs()

        if self.method == "rank":

            return series.rank(
                method="average"
            )

        if self.method == "standard":

            mean = series.mean()

            std = series.std()

            if std == 0:

                return series * 0

            return (
                series - mean
            ) / std

        raise ValueError(
            f"Transformation inconnue : "
            f"{self.method}"
        )


class LogTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="log",
            columns=columns
        )


class SqrtTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="sqrt",
            columns=columns
        )


class SquareTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="square",
            columns=columns
        )


class CubeTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="cube",
            columns=columns
        )


class ReciprocalTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="reciprocal",
            columns=columns
        )


class RankTransformer(
    Transformer
):

    def __init__(
        self,
        columns=None
    ):

        super().__init__(
            method="rank",
            columns=columns
        )


def log_transform(
    X,
    columns=None
):

    transformer = LogTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def log10_transform(
    X,
    columns=None
):

    transformer = Transformer(
        method="log10",
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def sqrt_transform(
    X,
    columns=None
):

    transformer = SqrtTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def square_transform(
    X,
    columns=None
):

    transformer = SquareTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def cube_transform(
    X,
    columns=None
):

    transformer = CubeTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def reciprocal_transform(
    X,
    columns=None
):

    transformer = ReciprocalTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def rank_transform(
    X,
    columns=None
):

    transformer = RankTransformer(
        columns=columns
    )

    return transformer.fit_transform(
        X
    )


def power_transform(
    X,
    power,
    columns=None
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.select_dtypes(
                include=np.number
            ).columns
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        data[column] = (
            data[column] ** power
        )

    return data


def clip_values(
    X,
    lower=None,
    upper=None,
    columns=None
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.select_dtypes(
                include=np.number
            ).columns
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        data[column] = (
            data[column]
            .clip(
                lower=lower,
                upper=upper
            )
        )

    return data


def winsorize(
    X,
    columns=None,
    lower_quantile=0.01,
    upper_quantile=0.99
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.select_dtypes(
                include=np.number
            ).columns
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        lower = data[column].quantile(
            lower_quantile
        )

        upper = data[column].quantile(
            upper_quantile
        )

        data[column] = (
            data[column]
            .clip(
                lower=lower,
                upper=upper
            )
        )

    return data
