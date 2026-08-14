"""
=========================================================
EMIDAF Framework
Preprocessing - Feature Engineering
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class FeatureEngineer:

    name = "Feature Engineer"

    def __init__(self):
        self.fitted_ = False

    def fit(self, X, y=None):

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:
            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        return X.copy()

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class InteractionFeatures:

    name = "Interaction Features"

    def __init__(
        self,
        columns,
        operation="multiply",
        suffix="_interaction"
    ):

        self.columns = columns
        self.operation = operation
        self.suffix = suffix

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        data = X.copy()

        columns = list(self.columns)

        if len(columns) < 2:
            raise ValueError(
                "Au moins deux variables sont nécessaires."
            )

        if self.operation == "multiply":

            for i in range(len(columns)):

                for j in range(i + 1, len(columns)):

                    c1 = columns[i]
                    c2 = columns[j]

                    name = (
                        f"{c1}_{c2}"
                        f"{self.suffix}"
                    )

                    data[name] = (
                        data[c1]
                        * data[c2]
                    )

        elif self.operation == "add":

            data[
                f"{self.suffix.strip('_')}_sum"
            ] = data[columns].sum(axis=1)

        elif self.operation == "subtract":

            result = data[columns[0]]

            for column in columns[1:]:

                result = result - data[column]

            data[
                f"{self.suffix.strip('_')}_difference"
            ] = result

        elif self.operation == "divide":

            for i in range(len(columns)):

                for j in range(i + 1, len(columns)):

                    c1 = columns[i]
                    c2 = columns[j]

                    name = (
                        f"{c1}_{c2}"
                        f"{self.suffix}"
                    )

                    denominator = (
                        data[c2]
                        .replace(0, np.nan)
                    )

                    data[name] = (
                        data[c1]
                        / denominator
                    )

        else:

            raise ValueError(
                "Opération inconnue."
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class PolynomialFeatures:

    name = "Polynomial Features"

    def __init__(
        self,
        columns,
        degree=2,
        include_original=True
    ):

        self.columns = columns
        self.degree = degree
        self.include_original = include_original

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        data = X.copy()

        for column in self.columns:

            if not self.include_original:

                data = data.drop(
                    columns=[column]
                )

            for power in range(
                2,
                self.degree + 1
            ):

                data[
                    f"{column}^{power}"
                ] = (
                    X[column] ** power
                )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class RatioFeature:

    name = "Ratio Feature"

    def __init__(
        self,
        numerator,
        denominator,
        name=None
    ):

        self.numerator = numerator
        self.denominator = denominator

        self.name = (
            name
            if name is not None
            else (
                f"{numerator}_"
                f"{denominator}_ratio"
            )
        )

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        data = X.copy()

        denominator = (
            data[self.denominator]
            .replace(0, np.nan)
        )

        data[self.name] = (
            data[self.numerator]
            / denominator
        )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class AggregationFeatures:

    name = "Aggregation Features"

    def __init__(
        self,
        columns,
        prefix="agg"
    ):

        self.columns = columns
        self.prefix = prefix

    def fit(self, X, y=None):

        return self

    def transform(self, X):

        data = X.copy()

        values = data[
            self.columns
        ]

        data[
            f"{self.prefix}_mean"
        ] = values.mean(axis=1)

        data[
            f"{self.prefix}_sum"
        ] = values.sum(axis=1)

        data[
            f"{self.prefix}_min"
        ] = values.min(axis=1)

        data[
            f"{self.prefix}_max"
        ] = values.max(axis=1)

        data[
            f"{self.prefix}_std"
        ] = values.std(axis=1)

        data[
            f"{self.prefix}_median"
        ] = values.median(axis=1)

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


def create_interaction(
    X,
    column1,
    column2,
    operation="multiply",
    name=None
):

    data = X.copy()

    if name is None:

        name = (
            f"{column1}_"
            f"{column2}_"
            f"{operation}"
        )

    if operation == "multiply":

        data[name] = (
            data[column1]
            * data[column2]
        )

    elif operation == "add":

        data[name] = (
            data[column1]
            + data[column2]
        )

    elif operation == "subtract":

        data[name] = (
            data[column1]
            - data[column2]
        )

    elif operation == "divide":

        denominator = (
            data[column2]
            .replace(0, np.nan)
        )

        data[name] = (
            data[column1]
            / denominator
        )

    else:

        raise ValueError(
            "Opération inconnue."
        )

    return data


def create_ratio(
    X,
    numerator,
    denominator,
    name=None
):

    data = X.copy()

    if name is None:

        name = (
            f"{numerator}_"
            f"{denominator}_ratio"
        )

    denominator_values = (
        data[denominator]
        .replace(0, np.nan)
    )

    data[name] = (
        data[numerator]
        / denominator_values
    )

    return data


def create_polynomial_features(
    X,
    columns,
    degree=2
):

    engineer = PolynomialFeatures(
        columns=columns,
        degree=degree
    )

    return engineer.fit_transform(X)


def create_aggregations(
    X,
    columns,
    prefix="agg"
):

    engineer = AggregationFeatures(
        columns=columns,
        prefix=prefix
    )

    return engineer.fit_transform(X)


def create_bmi(
    X,
    weight_column,
    height_column,
    name="BMI"
):

    data = X.copy()

    height = (
        data[height_column]
        .replace(0, np.nan)
    )

    data[name] = (
        data[weight_column]
        / height.pow(2)
    )

    return data


def create_age_group(
    X,
    age_column,
    bins=None,
    labels=None,
    name="Age_Group"
):

    data = X.copy()

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
            "Jeune",
            "Adulte",
            "Senior",
            "Très senior"
        ]

    data[name] = pd.cut(
        data[age_column],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return data


def create_date_features(
    X,
    date_column,
    prefix=None
):

    data = X.copy()

    dates = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    if prefix is None:
        prefix = date_column

    data[
        f"{prefix}_annee"
    ] = dates.dt.year

    data[
        f"{prefix}_mois"
    ] = dates.dt.month

    data[
        f"{prefix}_jour"
    ] = dates.dt.day

    data[
        f"{prefix}_jour_semaine"
    ] = dates.dt.dayofweek

    data[
        f"{prefix}_semaine"
    ] = dates.dt.isocalendar().week.astype(
        "Int64"
    )

    data[
        f"{prefix}_trimestre"
    ] = dates.dt.quarter

    data[
        f"{prefix}_heure"
    ] = dates.dt.hour

    data[
        f"{prefix}_minute"
    ] = dates.dt.minute

    data[
        f"{prefix}_weekend"
    ] = (
        dates.dt.dayofweek >= 5
    ).astype(int)

    return data


def create_log_features(
    X,
    columns,
    suffix="_log"
):

    data = X.copy()

    for column in columns:

        data[
            f"{column}{suffix}"
        ] = np.log1p(
            data[column]
        )

    return data


def create_sqrt_features(
    X,
    columns,
    suffix="_sqrt"
):

    data = X.copy()

    for column in columns:

        data[
            f"{column}{suffix}"
        ] = np.sqrt(
            data[column].clip(
                lower=0
            )
        )

    return data


def create_polynomial_column(
    X,
    column,
    degree=2,
    prefix=None
):

    data = X.copy()

    if prefix is None:
        prefix = column

    for power in range(
        2,
        degree + 1
    ):

        data[
            f"{prefix}_{power}"
        ] = (
            data[column] ** power
        )

    return data


def create_missing_indicators(
    X,
    columns=None,
    suffix="_missing"
):

    data = X.copy()

    if columns is None:

        columns = list(
            data.columns[
                data.isna().any()
            ]
        )

    elif isinstance(
        columns,
        str
    ):

        columns = [columns]

    for column in columns:

        data[
            f"{column}{suffix}"
        ] = (
            data[column]
            .isna()
            .astype(int)
        )

    return data
