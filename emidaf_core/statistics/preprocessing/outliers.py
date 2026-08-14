"""
=========================================================
EMIDAF Framework
Preprocessing - Outliers
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class OutlierDetector:

    name = "Outlier Detector"

    def __init__(
        self,
        method="iqr",
        threshold=1.5,
        columns=None
    ):

        self.method = method
        self.threshold = threshold
        self.columns = columns

        self.bounds_ = {}
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

        data = X.copy()

        columns = self._get_columns(
            data
        )

        self.bounds_ = {}

        for column in columns:

            series = pd.to_numeric(
                data[column],
                errors="coerce"
            )

            if self.method == "iqr":

                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)

                iqr = q3 - q1

                lower = (
                    q1
                    - self.threshold * iqr
                )

                upper = (
                    q3
                    + self.threshold * iqr
                )

            elif self.method == "zscore":

                mean = series.mean()
                std = series.std()

                lower = (
                    mean
                    - self.threshold * std
                )

                upper = (
                    mean
                    + self.threshold * std
                )

            elif self.method == "mad":

                median = series.median()

                mad = (
                    series
                    .sub(median)
                    .abs()
                    .median()
                )

                lower = (
                    median
                    - self.threshold * mad
                )

                upper = (
                    median
                    + self.threshold * mad
                )

            else:

                raise ValueError(
                    "Méthode inconnue. "
                    "Utilisez 'iqr', "
                    "'zscore' ou 'mad'."
                )

            self.bounds_[column] = (
                lower,
                upper
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

        mask = self.mask(
            data
        )

        return data.loc[
            ~mask
        ].copy()

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

    def mask(
        self,
        X
    ):

        if not self.fitted_:

            self.fit(X)

        mask = pd.Series(
            False,
            index=X.index
        )

        for column, (
            lower,
            upper
        ) in self.bounds_.items():

            current = (
                X[column]
                < lower
            ) | (
                X[column]
                > upper
            )

            mask = mask | current

        return mask

    def count(
        self,
        X
    ):

        return int(
            self.mask(X).sum()
        )

    def percentage(
        self,
        X
    ):

        if len(X) == 0:

            return 0.0

        return (
            self.count(X)
            / len(X)
            * 100
        )

    def report(
        self,
        X
    ):

        mask = self.mask(X)

        return {

            "method":
                self.method,

            "threshold":
                self.threshold,

            "outlier_count":
                int(mask.sum()),

            "outlier_percentage":
                (
                    mask.mean() * 100
                )

        }


class IQRDetector(
    OutlierDetector
):

    def __init__(
        self,
        multiplier=1.5,
        columns=None
    ):

        super().__init__(
            method="iqr",
            threshold=multiplier,
            columns=columns
        )


class ZScoreDetector(
    OutlierDetector
):

    def __init__(
        self,
        threshold=3.0,
        columns=None
    ):

        super().__init__(
            method="zscore",
            threshold=threshold,
            columns=columns
        )


class MADDetector(
    OutlierDetector
):

    def __init__(
        self,
        threshold=3.0,
        columns=None
    ):

        super().__init__(
            method="mad",
            threshold=threshold,
            columns=columns
        )


def iqr_bounds(
    series,
    multiplier=1.5
):

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = (
        q1
        - multiplier * iqr
    )

    upper = (
        q3
        + multiplier * iqr
    )

    return lower, upper


def iqr_mask(
    series,
    multiplier=1.5
):

    lower, upper = iqr_bounds(
        series,
        multiplier
    )

    return (
        (series < lower)
        |
        (series > upper)
    )


def zscore(
    series
):

    mean = series.mean()

    std = series.std()

    if std == 0:

        return pd.Series(
            0,
            index=series.index
        )

    return (
        series - mean
    ) / std


def zscore_mask(
    series,
    threshold=3.0
):

    scores = zscore(
        series
    )

    return (
        scores.abs()
        > threshold
    )


def mad_score(
    series
):

    median = series.median()

    mad = (
        series
        .sub(median)
        .abs()
        .median()
    )

    if mad == 0:

        return pd.Series(
            0,
            index=series.index
        )

    return (
        series - median
    ).abs() / mad


def mad_mask(
    series,
    threshold=3.0
):

    return (
        mad_score(series)
        > threshold
    )


def outlier_mask(
    X,
    method="iqr",
    threshold=1.5,
    columns=None
):

    detector = OutlierDetector(
        method=method,
        threshold=threshold,
        columns=columns
    )

    detector.fit(X)

    return detector.mask(X)


def remove_outliers(
    X,
    method="iqr",
    threshold=1.5,
    columns=None
):

    detector = OutlierDetector(
        method=method,
        threshold=threshold,
        columns=columns
    )

    detector.fit(X)

    return detector.transform(X)


def outlier_summary(
    X,
    method="iqr",
    threshold=1.5,
    columns=None
):

    detector = OutlierDetector(
        method=method,
        threshold=threshold,
        columns=columns
    )

    detector.fit(X)

    rows = []

    for column, (
        lower,
        upper
    ) in detector.bounds_.items():

        series = X[column]

        mask = (
            (series < lower)
            |
            (series > upper)
        )

        rows.append({

            "variable":
                column,

            "lower_bound":
                lower,

            "upper_bound":
                upper,

            "outlier_count":
                int(mask.sum()),

            "outlier_percentage":
                mask.mean() * 100

        })

    return pd.DataFrame(
        rows
    )


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
