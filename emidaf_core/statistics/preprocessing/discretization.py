"""
=========================================================
EMIDAF Framework
Preprocessing - Discretization
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class Discretizer:

    name = "Discretizer"

    def __init__(
        self,
        method="uniform",
        columns=None,
        n_bins=5,
        labels=None,
        suffix="_bin"
    ):

        self.method = method
        self.columns = columns
        self.n_bins = n_bins
        self.labels = labels
        self.suffix = suffix

        self.columns_ = None
        self.bin_edges_ = {}
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

        self.bin_edges_ = {}

        for column in self.columns_:

            series = pd.to_numeric(
                X[column],
                errors="coerce"
            )

            if self.method == "uniform":

                edges = np.linspace(
                    series.min(),
                    series.max(),
                    self.n_bins + 1
                )

            elif self.method == "quantile":

                edges = np.quantile(
                    series.dropna(),
                    np.linspace(
                        0,
                        1,
                        self.n_bins + 1
                    )
                )

                edges = np.unique(edges)

            elif self.method == "custom":

                raise ValueError(
                    "Pour la méthode 'custom', "
                    "utilisez CustomBinner."
                )

            else:

                raise ValueError(
                    "Méthode inconnue. "
                    "Utilisez 'uniform', "
                    "'quantile' ou 'custom'."
                )

            self.bin_edges_[column] = edges

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:

            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            edges = self.bin_edges_[column]

            labels = self.labels

            if labels is not None:

                if len(edges) - 1 != len(labels):

                    raise ValueError(
                        "Le nombre de labels doit "
                        "correspondre au nombre "
                        "de classes."
                    )

            data[
                f"{column}{self.suffix}"
            ] = pd.cut(
                data[column],
                bins=edges,
                labels=labels,
                include_lowest=True,
                duplicates="drop"
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class EqualWidthBinner:

    name = "Equal Width Binner"

    def __init__(
        self,
        columns=None,
        n_bins=5,
        labels=None,
        suffix="_bin"
    ):

        self.columns = columns
        self.n_bins = n_bins
        self.labels = labels
        self.suffix = suffix

        self.columns_ = None
        self.edges_ = {}
        self.fitted_ = False

    def fit(self, X, y=None):

        if self.columns is None:

            self.columns_ = list(
                X.select_dtypes(
                    include=np.number
                ).columns
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

        for column in self.columns_:

            series = X[column]

            self.edges_[column] = (
                np.linspace(
                    series.min(),
                    series.max(),
                    self.n_bins + 1
                )
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

            data[
                f"{column}{self.suffix}"
            ] = pd.cut(
                data[column],
                bins=self.edges_[column],
                labels=self.labels,
                include_lowest=True,
                duplicates="drop"
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class QuantileBinner:

    name = "Quantile Binner"

    def __init__(
        self,
        columns=None,
        n_bins=5,
        labels=None,
        suffix="_bin"
    ):

        self.columns = columns
        self.n_bins = n_bins
        self.labels = labels
        self.suffix = suffix

        self.columns_ = None
        self.edges_ = {}
        self.fitted_ = False

    def fit(self, X, y=None):

        if self.columns is None:

            self.columns_ = list(
                X.select_dtypes(
                    include=np.number
                ).columns
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

        for column in self.columns_:

            values = (
                X[column]
                .dropna()
            )

            edges = np.quantile(
                values,
                np.linspace(
                    0,
                    1,
                    self.n_bins + 1
                )
            )

            self.edges_[column] = np.unique(
                edges
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

            data[
                f"{column}{self.suffix}"
            ] = pd.cut(
                data[column],
                bins=self.edges_[column],
                labels=self.labels,
                include_lowest=True,
                duplicates="drop"
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


class CustomBinner:

    name = "Custom Binner"

    def __init__(
        self,
        bins,
        columns=None,
        labels=None,
        suffix="_bin"
    ):

        self.bins = bins
        self.columns = columns
        self.labels = labels
        self.suffix = suffix

        self.columns_ = None
        self.fitted_ = False

    def fit(self, X, y=None):

        if self.columns is None:

            raise ValueError(
                "Spécifiez les colonnes."
            )

        if isinstance(
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

        self.fitted_ = True

        return self

    def transform(self, X):

        if not self.fitted_:

            raise RuntimeError(
                "Appelez fit() avant transform()."
            )

        data = X.copy()

        for column in self.columns_:

            bins = (
                self.bins[column]
                if isinstance(
                    self.bins,
                    dict
                )
                else self.bins
            )

            data[
                f"{column}{self.suffix}"
            ] = pd.cut(
                data[column],
                bins=bins,
                labels=self.labels,
                include_lowest=True,
                duplicates="drop"
            )

        return data

    def fit_transform(self, X, y=None):

        self.fit(X, y)

        return self.transform(X)


def equal_width_bins(
    series,
    n_bins=5,
    labels=None
):

    return pd.cut(
        series,
        bins=n_bins,
        labels=labels,
        include_lowest=True
    )


def quantile_bins(
    series,
    n_bins=5,
    labels=None
):

    return pd.qcut(
        series,
        q=n_bins,
        labels=labels,
        duplicates="drop"
    )


def custom_bins(
    series,
    bins,
    labels=None
):

    return pd.cut(
        series,
        bins=bins,
        labels=labels,
        include_lowest=True
    )


def bin_numeric_columns(
    X,
    columns=None,
    n_bins=5,
    method="uniform",
    labels=None,
    suffix="_bin"
):

    discretizer = Discretizer(
        method=method,
        columns=columns,
        n_bins=n_bins,
        labels=labels,
        suffix=suffix
    )

    return discretizer.fit_transform(
        X
    )
