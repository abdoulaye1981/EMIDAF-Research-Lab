"""
=========================================================
EMIDAF Framework
Preprocessing - Feature Selection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class FeatureSelector:

    name = "Feature Selector"

    def __init__(
        self,
        columns=None
    ):

        self.columns = columns
        self.selected_columns_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        if self.columns is None:

            self.selected_columns_ = list(
                X.columns
            )

        elif isinstance(
            self.columns,
            str
        ):

            self.selected_columns_ = [
                self.columns
            ]

        else:

            self.selected_columns_ = list(
                self.columns
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

        return X[
            self.selected_columns_
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

    def get_support(self):

        if self.selected_columns_ is None:

            raise RuntimeError(
                "Le sélecteur n'est pas ajusté."
            )

        return self.selected_columns_


class VarianceThresholdSelector:

    name = "Variance Threshold"

    def __init__(
        self,
        threshold=0.0,
        columns=None
    ):

        self.threshold = threshold
        self.columns = columns

        self.variances_ = {}
        self.selected_columns_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        if self.columns is None:

            columns = list(
                X.select_dtypes(
                    include=np.number
                ).columns
            )

        elif isinstance(
            self.columns,
            str
        ):

            columns = [
                self.columns
            ]

        else:

            columns = list(
                self.columns
            )

        self.variances_ = {
            column: X[column].var()
            for column in columns
        }

        self.selected_columns_ = [
            column
            for column in columns
            if self.variances_[column]
            > self.threshold
        ]

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

        return X[
            self.selected_columns_
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

    def get_support(self):

        return self.selected_columns_


class CorrelationSelector:

    name = "Correlation Selector"

    def __init__(
        self,
        threshold=0.9,
        method="pearson"
    ):

        self.threshold = threshold
        self.method = method

        self.correlation_matrix_ = None
        self.selected_columns_ = None
        self.removed_columns_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        data = X.select_dtypes(
            include=np.number
        )

        self.correlation_matrix_ = (
            data.corr(
                method=self.method
            )
        )

        columns = list(
            self.correlation_matrix_.columns
        )

        remove = set()

        for i in range(
            len(columns)
        ):

            for j in range(
                i + 1,
                len(columns)
            ):

                correlation = abs(
                    self.correlation_matrix_.iloc[
                        i,
                        j
                    ]
                )

                if correlation >= self.threshold:

                    remove.add(
                        columns[j]
                    )

        self.removed_columns_ = list(
            remove
        )

        self.selected_columns_ = [
            column
            for column in columns
            if column not in remove
        ]

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

        return X[
            self.selected_columns_
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

    def get_support(self):

        return self.selected_columns_

    def get_removed(self):

        return self.removed_columns_


class UnivariateCorrelationSelector:

    name = "Univariate Correlation Selector"

    def __init__(
        self,
        threshold=0.1,
        method="pearson"
    ):

        self.threshold = threshold
        self.method = method

        self.scores_ = {}
        self.selected_columns_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y
    ):

        target = pd.Series(
            y,
            index=X.index
        )

        numeric = X.select_dtypes(
            include=np.number
        )

        self.scores_ = {}

        for column in numeric.columns:

            score = (
                numeric[column]
                .corr(
                    target,
                    method=self.method
                )
            )

            self.scores_[column] = score

        self.selected_columns_ = [
            column
            for column, score
            in self.scores_.items()
            if pd.notna(score)
            and abs(score)
            >= self.threshold
        ]

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

        return X[
            self.selected_columns_
        ].copy()

    def fit_transform(
        self,
        X,
        y
    ):

        self.fit(
            X,
            y
        )

        return self.transform(
            X
        )

    def scores(self):

        return pd.Series(
            self.scores_
        ).sort_values(
            ascending=False
        )


def variance_threshold(
    X,
    threshold=0.0
):

    selector = VarianceThresholdSelector(
        threshold=threshold
    )

    return selector.fit_transform(
        X
    )


def remove_correlated_features(
    X,
    threshold=0.9,
    method="pearson"
):

    selector = CorrelationSelector(
        threshold=threshold,
        method=method
    )

    return selector.fit_transform(
        X
    )


def correlation_matrix(
    X,
    method="pearson"
):

    return (
        X.select_dtypes(
            include=np.number
        )
        .corr(
            method=method
        )
    )


def highly_correlated_features(
    X,
    threshold=0.9,
    method="pearson"
):

    matrix = correlation_matrix(
        X,
        method=method
    )

    pairs = []

    columns = list(
        matrix.columns
    )

    for i in range(
        len(columns)
    ):

        for j in range(
            i + 1,
            len(columns)
        ):

            value = matrix.iloc[
                i,
                j
            ]

            if (
                pd.notna(value)
                and abs(value)
                >= threshold
            ):

                pairs.append({

                    "variable_1":
                        columns[i],

                    "variable_2":
                        columns[j],

                    "correlation":
                        value

                })

    return pd.DataFrame(
        pairs
    )


def select_by_correlation(
    X,
    y,
    threshold=0.1,
    method="pearson"
):

    selector = UnivariateCorrelationSelector(
        threshold=threshold,
        method=method
    )

    return selector.fit_transform(
        X,
        y
    )
