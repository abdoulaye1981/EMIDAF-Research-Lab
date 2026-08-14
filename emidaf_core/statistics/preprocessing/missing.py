"""
=========================================================
EMIDAF Framework
Preprocessing - Missing Values
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class MissingValues:

    name = "Missing Values"

    def __init__(
        self,
        strategy="auto",
        value=None,
        columns=None
    ):

        self.strategy = strategy
        self.value = value
        self.columns = columns

        self.statistics_ = {}
        self.fitted_ = False

    def _get_columns(
        self,
        X
    ):

        if self.columns is None:
            return list(X.columns)

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

        data = X.copy()

        columns = self._get_columns(
            data
        )

        self.statistics_ = {}

        for column in columns:

            series = data[column]

            if pd.api.types.is_numeric_dtype(
                series
            ):

                if self.strategy in [
                    "mean",
                    "auto"
                ]:

                    self.statistics_[column] = (
                        series.mean()
                    )

                elif self.strategy == "median":

                    self.statistics_[column] = (
                        series.median()
                    )

                elif self.strategy == "zero":

                    self.statistics_[column] = 0

                elif self.strategy == "value":

                    self.statistics_[column] = (
                        self.value
                    )

            else:

                if self.strategy in [
                    "mode",
                    "auto"
                ]:

                    mode = (
                        series
                        .mode(
                            dropna=True
                        )
                    )

                    self.statistics_[column] = (
                        mode.iloc[0]
                        if not mode.empty
                        else self.value
                    )

                elif self.strategy == "value":

                    self.statistics_[column] = (
                        self.value
                    )

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

        for column, value in (
            self.statistics_.items()
        ):

            data[column] = (
                data[column]
                .fillna(value)
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

    def missing_count(
        self,
        X
    ):

        return (
            X.isna()
            .sum()
        )

    def missing_percentage(
        self,
        X
    ):

        return (
            X.isna()
            .mean()
            * 100
        )

    def report(
        self,
        X
    ):

        result = pd.DataFrame({

            "variable":
                X.columns,

            "missing_count":
                X.isna()
                .sum()
                .values,

            "missing_percentage":
                (
                    X.isna()
                    .mean()
                    .values
                    * 100
                )

        })

        return result.sort_values(
            "missing_percentage",
            ascending=False
        ).reset_index(
            drop=True
        )


class SimpleImputerPreprocessor(
    MissingValues
):

    pass


class MissingIndicator:

    name = "Missing Indicator"

    def __init__(
        self,
        columns=None,
        suffix="_missing"
    ):

        self.columns = columns
        self.suffix = suffix
        self.columns_ = None

    def fit(
        self,
        X,
        y=None
    ):

        if self.columns is None:

            self.columns_ = list(
                X.columns[
                    X.isna().any()
                ]
            )

        elif isinstance(
            self.columns,
            str
        ):

            self.columns_ = [
                self.columns
            ]

        else:

            self.columns_ = list(
                self.columns
            )

        return self

    def transform(
        self,
        X
    ):

        data = X.copy()

        for column in self.columns_:

            data[
                f"{column}{self.suffix}"
            ] = (
                data[column]
                .isna()
                .astype(int)
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


class MissingHandler(
    MissingValues
):

    pass


def missing_summary(
    X
):

    return pd.DataFrame({

        "variable":
            X.columns,

        "missing":
            X.isna()
            .sum()
            .values,

        "percentage":
            (
                X.isna()
                .mean()
                .values
                * 100
            )

    })


def missing_columns(
    X
):

    return list(
        X.columns[
            X.isna().any()
        ]
    )


def complete_columns(
    X
):

    return list(
        X.columns[
            ~X.isna().any()
        ]
    )


def complete_cases(
    X
):

    return X.dropna()


def remove_missing_rows(
    X
):

    return X.dropna(
        axis=0
    )


def remove_missing_columns(
    X
):

    return X.dropna(
        axis=1
    )


def fill_constant(
    X,
    value=0,
    columns=None
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.columns
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        data[column] = (
            data[column]
            .fillna(value)
        )

    return data


def fill_mean(
    X,
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
            .fillna(
                data[column].mean()
            )
        )

    return data


def fill_median(
    X,
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
            .fillna(
                data[column].median()
            )
        )

    return data


def fill_mode(
    X,
    columns=None
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.columns
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        mode = (
            data[column]
            .mode(
                dropna=True
            )
        )

        if not mode.empty:

            data[column] = (
                data[column]
                .fillna(
                    mode.iloc[0]
                )
            )

    return data
