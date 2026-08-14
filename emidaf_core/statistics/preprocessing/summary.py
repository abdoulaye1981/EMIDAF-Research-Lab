"""
=========================================================
EMIDAF Framework
Preprocessing - Summary
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def missing_summary(X):

    result = pd.DataFrame({
        "missing_count": X.isna().sum(),
        "missing_percentage": (
            X.isna().mean() * 100
        )
    })

    result["non_missing_count"] = (
        len(X)
        - result["missing_count"]
    )

    return result.sort_values(
        "missing_count",
        ascending=False
    )


def duplicate_summary(X):

    duplicate_count = X.duplicated().sum()

    return {
        "duplicate_count": int(
            duplicate_count
        ),
        "duplicate_percentage": (
            duplicate_count
            / len(X)
            * 100
            if len(X) > 0
            else 0
        )
    }


def categorical_summary(X):

    columns = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    rows = []

    for column in columns:

        series = X[column]

        rows.append({
            "variable": column,
            "type": str(
                series.dtype
            ),
            "n_unique": (
                series.nunique(
                    dropna=True
                )
            ),
            "missing": int(
                series.isna().sum()
            ),
            "missing_percentage": (
                series.isna().mean()
                * 100
            )
        })

    return pd.DataFrame(rows)


def numeric_summary(X):

    data = X.select_dtypes(
        include=np.number
    )

    if data.empty:

        return pd.DataFrame()

    result = data.describe().T

    result["missing"] = (
        data.isna().sum()
    )

    result["missing_percentage"] = (
        data.isna().mean() * 100
    )

    result["skewness"] = (
        data.skew()
    )

    result["kurtosis"] = (
        data.kurtosis()
    )

    result["coefficient_variation"] = (
        data.std()
        / data.mean().replace(
            0,
            np.nan
        )
        * 100
    )

    return result


def unique_summary(X):

    return pd.DataFrame({
        "variable": X.columns,
        "n_unique": [
            X[column].nunique(
                dropna=True
            )
            for column in X.columns
        ],
        "n_missing": [
            X[column].isna().sum()
            for column in X.columns
        ]
    })


def constant_columns(X):

    return [
        column
        for column in X.columns
        if X[column].nunique(
            dropna=False
        ) <= 1
    ]


def high_cardinality_columns(
    X,
    threshold=50
):

    result = []

    for column in X.columns:

        n_unique = X[column].nunique(
            dropna=True
        )

        if n_unique > threshold:

            result.append({
                "variable": column,
                "n_unique": n_unique
            })

    return pd.DataFrame(
        result
    )


def data_types_summary(X):

    return pd.DataFrame({
        "variable": X.columns,
        "dtype": [
            str(dtype)
            for dtype in X.dtypes
        ]
    })


def memory_usage_summary(X):

    memory = X.memory_usage(
        deep=True
    )

    return pd.DataFrame({
        "variable": memory.index,
        "memory_bytes": memory.values
    })


def shape_summary(X):

    return {
        "n_rows": int(
            X.shape[0]
        ),
        "n_columns": int(
            X.shape[1]
        )
    }


def complete_cases_summary(X):

    complete_rows = (
        X.notna()
        .all(axis=1)
        .sum()
    )

    incomplete_rows = (
        len(X)
        - complete_rows
    )

    return {
        "complete_rows": int(
            complete_rows
        ),
        "incomplete_rows": int(
            incomplete_rows
        ),
        "complete_percentage": (
            complete_rows
            / len(X)
            * 100
            if len(X) > 0
            else 0
        ),
        "incomplete_percentage": (
            incomplete_rows
            / len(X)
            * 100
            if len(X) > 0
            else 0
        )
    }


def preprocessing_summary(X):

    return {
        "shape":
            shape_summary(X),

        "data_types":
            data_types_summary(X),

        "numeric":
            numeric_summary(X),

        "categorical":
            categorical_summary(X),

        "missing":
            missing_summary(X),

        "duplicates":
            duplicate_summary(X),

        "unique":
            unique_summary(X),

        "constant_columns":
            constant_columns(X),

        "complete_cases":
            complete_cases_summary(X)
    }


class PreprocessingSummary:

    name = "Preprocessing Summary"

    def __init__(self):

        self.summary_ = None
        self.fitted_ = False

    def fit(
        self,
        X,
        y=None
    ):

        self.summary_ = (
            preprocessing_summary(X)
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

        return X.copy()

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

    def get_summary(self):

        if not self.fitted_:

            raise RuntimeError(
                "Le résumé n'est pas disponible."
            )

        return self.summary_


def print_preprocessing_summary(
    X
):

    summary = (
        preprocessing_summary(X)
    )

    print("=" * 60)
    print("RÉSUMÉ DU PRÉTRAITEMENT")
    print("=" * 60)

    print("\nDimensions")
    print(summary["shape"])

    print("\nTypes")
    print(summary["data_types"])

    print("\nVariables numériques")
    print(summary["numeric"])

    print("\nVariables catégorielles")
    print(summary["categorical"])

    print("\nValeurs manquantes")
    print(summary["missing"])

    print("\nDoublons")
    print(summary["duplicates"])

    print("\nColonnes constantes")
    print(summary["constant_columns"])

    print("\nObservations complètes")
    print(summary["complete_cases"])

    return summary
