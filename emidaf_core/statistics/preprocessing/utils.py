"""
=========================================================
EMIDAF Framework
Preprocessing - Utilities
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def get_numeric_columns(X):

    return list(
        X.select_dtypes(
            include=np.number
        ).columns
    )


def get_categorical_columns(X):

    return list(
        X.select_dtypes(
            include=["object", "category", "bool"]
        ).columns
    )


def copy_data(X):

    return X.copy()


def ensure_dataframe(X):

    if isinstance(X, pd.DataFrame):

        return X.copy()

    if isinstance(X, pd.Series):

        return X.to_frame()

    return pd.DataFrame(X)


def replace_inf_with_nan(X):

    data = X.copy()

    numeric_columns = get_numeric_columns(
        data
    )

    data[numeric_columns] = (
        data[numeric_columns]
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
    )

    return data


def remove_empty_columns(X):

    data = X.copy()

    return data.dropna(
        axis=1,
        how="all"
    )


def remove_empty_rows(X):

    data = X.copy()

    return data.dropna(
        axis=0,
        how="all"
    )


def normalize_column_names(X):

    data = X.copy()

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False
        )
    )

    return data


def strip_string_columns(X):

    data = X.copy()

    columns = get_categorical_columns(
        data
    )

    for column in columns:

        if data[column].dtype == "object":

            data[column] = (
                data[column]
                .str.strip()
            )

    return data


def preprocessing_copy(X):

    data = ensure_dataframe(
        X
    )

    data = replace_inf_with_nan(
        data
    )

    data = strip_string_columns(
        data
    )

    return data
