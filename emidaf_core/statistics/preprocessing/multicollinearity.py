"""
=========================================================
EMIDAF Framework
Preprocessing - Multicollinearity
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def correlation_matrix(
    X,
    method="pearson"
):

    data = X.select_dtypes(
        include=np.number
    )

    return data.corr(
        method=method
    )


def highly_correlated_pairs(
    X,
    threshold=0.8,
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
                and abs(value) >= threshold
            ):

                pairs.append({
                    "variable_1": columns[i],
                    "variable_2": columns[j],
                    "correlation": value
                })

    return pd.DataFrame(pairs)


def calculate_vif(
    X
):

    data = X.select_dtypes(
        include=np.number
    ).copy()

    data = data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    data = data.dropna()

    results = []

    columns = list(
        data.columns
    )

    for column in columns:

        y = data[column]

        other_columns = [
            c for c in columns
            if c != column
        ]

        if len(other_columns) == 0:

            vif = 1.0

        else:

            X_other = data[
                other_columns
            ]

            X_matrix = np.column_stack(
                [
                    np.ones(
                        len(X_other)
                    ),
                    X_other.values
                ]
            )

            try:

                coefficients = np.linalg.lstsq(
                    X_matrix,
                    y.values,
                    rcond=None
                )[0]

                predictions = (
                    X_matrix
                    @ coefficients
                )

                ss_res = np.sum(
                    (
                        y.values
                        - predictions
                    ) ** 2
                )

                ss_tot = np.sum(
                    (
                        y.values
                        - y.mean()
                    ) ** 2
                )

                if ss_tot == 0:

                    r_squared = 1.0

                else:

                    r_squared = (
                        1
                        - ss_res / ss_tot
                    )

                if r_squared >= 1:

                    vif = np.inf

                else:

                    vif = (
                        1
                        / (1 - r_squared)
                    )

            except np.linalg.LinAlgError:

                vif = np.inf

        results.append({
            "variable": column,
            "VIF": vif
        })

    return pd.DataFrame(
        results
    ).sort_values(
        "VIF",
        ascending=False
    ).reset_index(
        drop=True
    )


class VIFSelector:

    name = "VIF Selector"

    def __init__(
        self,
        threshold=5.0
    ):

        self.threshold = threshold
        self.vif_ = None
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
        ).copy()

        columns = list(
            data.columns
        )

        removed = []

        while len(columns) > 1:

            current = data[
                columns
            ]

            vif_table = calculate_vif(
                current
            )

            maximum = vif_table.iloc[
                0
            ]

            if (
                maximum["VIF"]
                <= self.threshold
            ):

                break

            variable = (
                maximum["variable"]
            )

            columns.remove(
                variable
            )

            removed.append(
                variable
            )

        self.selected_columns_ = columns

        self.removed_columns_ = removed

        self.vif_ = calculate_vif(
            data[self.selected_columns_]
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

        return self.selected_columns_

    def get_removed(self):

        return self.removed_columns_

    def get_vif(self):

        return self.vif_


def remove_multicollinearity(
    X,
    threshold=5.0
):

    selector = VIFSelector(
        threshold=threshold
    )

    result = selector.fit_transform(
        X
    )

    return result


def condition_number(
    X
):

    data = X.select_dtypes(
        include=np.number
    ).copy()

    data = data.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    if data.empty:

        return np.nan

    matrix = data.values

    matrix = (
        matrix
        - matrix.mean(axis=0)
    )

    std = matrix.std(
        axis=0
    )

    std[std == 0] = 1

    matrix = (
        matrix / std
    )

    singular_values = np.linalg.svd(
        matrix,
        compute_uv=False
    )

    if singular_values[-1] == 0:

        return np.inf

    return (
        singular_values[0]
        / singular_values[-1]
    )


def multicollinearity_report(
    X,
    correlation_threshold=0.8,
    vif_threshold=5.0,
    method="pearson"
):

    pairs = highly_correlated_pairs(
        X,
        threshold=correlation_threshold,
        method=method
    )

    vif = calculate_vif(
        X
    )

    condition = condition_number(
        X
    )

    return {
        "correlation_pairs": pairs,
        "vif": vif,
        "condition_number": condition
    }
