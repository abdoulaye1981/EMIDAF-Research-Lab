"""
=========================================================
EMIDAF Framework
Preprocessing Utilities
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd


# ==========================================================
# TYPE DETECTION
# ==========================================================

def get_numeric_columns(
    df
):

    return list(
        df.select_dtypes(
            include=np.number
        ).columns
    )


def get_categorical_columns(
    df
):

    return list(
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns
    )


def get_datetime_columns(
    df
):

    return list(
        df.select_dtypes(
            include=[
                "datetime",
                "datetimetz"
            ]
        ).columns
    )


# ==========================================================
# COLUMN VALIDATION
# ==========================================================

def validate_columns(
    df,
    columns
):

    if columns is None:

        return True

    if isinstance(
        columns,
        str
    ):

        columns = [columns]

    missing = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Variables absentes : {missing}"
        )

    return True


# ==========================================================
# COPY DATAFRAME
# ==========================================================

def safe_copy(
    df
):

    if isinstance(
        df,
        pd.DataFrame
    ):

        return df.copy()

    raise TypeError(
        "L'objet doit être un "
        "pandas.DataFrame."
    )


# ==========================================================
# MISSING VALUES
# ==========================================================

def missing_count(
    df
):

    return int(
        df.isna()
        .sum()
        .sum()
    )


def missing_percentage(
    df
):

    total = (
        df.shape[0]
        * df.shape[1]
    )

    if total == 0:

        return 0.0

    return (
        missing_count(df)
        / total
        * 100
    )


# ==========================================================
# DUPLICATES
# ==========================================================

def duplicate_count(
    df
):

    return int(
        df.duplicated()
        .sum()
    )


def duplicate_percentage(
    df
):

    if len(df) == 0:

        return 0.0

    return (
        duplicate_count(df)
        / len(df)
        * 100
    )


# ==========================================================
# CONSTANT VARIABLES
# ==========================================================

def get_constant_columns(
    df
):

    result = []

    for column in df.columns:

        if (
            df[column]
            .nunique(
                dropna=False
            )
            <= 1
        ):

            result.append(
                column
            )

    return result


# ==========================================================
# LOW VARIANCE VARIABLES
# ==========================================================

def low_variance_columns(
    df,
    threshold=0.0
):

    numeric = df.select_dtypes(
        include=np.number
    )

    variances = (
        numeric
        .var()
    )

    return list(
        variances[
            variances <= threshold
        ].index
    )


# ==========================================================
# CARDINALITY
# ==========================================================

def cardinality(
    df
):

    result = {}

    for column in df.columns:

        result[column] = int(
            df[column]
            .nunique(
                dropna=True
            )
        )

    return result


def high_cardinality_columns(
    df,
    threshold=50
):

    result = []

    for column in df.columns:

        unique = (
            df[column]
            .nunique(
                dropna=True
            )
        )

        if unique > threshold:

            result.append(
                column
            )

    return result


# ==========================================================
# IQR
# ==========================================================

def iqr_bounds(
    series,
    multiplier=1.5
):

    values = (
        pd.Series(series)
        .dropna()
    )

    q1 = values.quantile(
        0.25
    )

    q3 = values.quantile(
        0.75
    )

    iqr = q3 - q1

    lower = (
        q1
        - multiplier * iqr
    )

    upper = (
        q3
        + multiplier * iqr
    )

    return (
        lower,
        upper
    )


# ==========================================================
# OUTLIER MASK
# ==========================================================

def iqr_outlier_mask(
    series,
    multiplier=1.5
):

    lower, upper = (
        iqr_bounds(
            series,
            multiplier
        )
    )

    return (
        (series < lower)
        |
        (series > upper)
    )


def zscore_outlier_mask(
    series,
    threshold=3
):

    values = pd.Series(
        series
    )

    mean = values.mean()

    std = values.std()

    if std == 0:

        return pd.Series(
            False,
            index=values.index
        )

    zscore = (
        (values - mean)
        / std
    )

    return (
        zscore.abs()
        > threshold
    )


# ==========================================================
# STANDARDIZATION
# ==========================================================

def standardize_series(
    series
):

    values = pd.Series(
        series
    )

    mean = values.mean()

    std = values.std()

    if std == 0:

        return pd.Series(
            0.0,
            index=values.index,
            name=values.name
        )

    return (
        values - mean
    ) / std


# ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_series(
    series
):

    values = pd.Series(
        series
    )

    minimum = values.min()

    maximum = values.max()

    if maximum == minimum:

        return pd.Series(
            0.0,
            index=values.index,
            name=values.name
        )

    return (
        (values - minimum)
        /
        (maximum - minimum)
    )


# ==========================================================
# COEFFICIENT OF VARIATION
# ==========================================================

def coefficient_variation(
    series
):

    values = (
        pd.Series(series)
        .dropna()
    )

    mean = values.mean()

    std = values.std()

    if mean == 0:

        return np.nan

    return (
        std
        / abs(mean)
        * 100
    )


# ==========================================================
# SAFE DIVISION
# ==========================================================

def safe_divide(
    numerator,
    denominator
):

    if denominator == 0:

        return np.nan

    return (
        numerator
        / denominator
    )


# ==========================================================
# MEMORY USAGE
# ==========================================================

def memory_usage(
    df
):

    return (
        df.memory_usage(
            deep=True
        )
        .sum()
    )


def memory_usage_mb(
    df
):

    return (
        memory_usage(df)
        / 1024**2
    )


# ==========================================================
# DATAFRAME VALIDATION
# ==========================================================

def validate_dataframe(
    df
):

    if not isinstance(
        df,
        pd.DataFrame
    ):

        raise TypeError(
            "L'objet doit être "
            "un pandas.DataFrame."
        )

    if df.empty:

        raise ValueError(
            "Le DataFrame est vide."
        )

    return True


# ==========================================================
# TARGET VALIDATION
# ==========================================================

def validate_target(
    df,
    target
):

    if target not in df.columns:

        raise ValueError(
            f"La variable cible "
            f"'{target}' n'existe pas."
        )

    return True


# ==========================================================
# TRAIN / TEST COLUMN CONSISTENCY
# ==========================================================

def check_column_consistency(
    X_train,
    X_test
):

    train_columns = list(
        X_train.columns
    )

    test_columns = list(
        X_test.columns
    )

    missing_in_test = [
        column
        for column in train_columns
        if column not in test_columns
    ]

    extra_in_test = [
        column
        for column in test_columns
        if column not in train_columns
    ]

    same_order = (
        train_columns
        == test_columns
    )

    return {

        "same_columns":
            len(missing_in_test) == 0
            and
            len(extra_in_test) == 0,

        "same_order":
            same_order,

        "missing_in_test":
            missing_in_test,

        "extra_in_test":
            extra_in_test

    }


# ==========================================================
# ALIGN TRAIN / TEST
# ==========================================================

def align_columns(
    X_train,
    X_test
):

    check = (
        check_column_consistency(
            X_train,
            X_test
        )
    )

    if (
        check["missing_in_test"]
        or
        check["extra_in_test"]
    ):

        raise ValueError(
            "Les colonnes de X_train "
            "et X_test sont différentes."
        )

    return X_test[
        X_train.columns
    ].copy()


# ==========================================================
# CONVERT TO DATAFRAME
# ==========================================================

def to_dataframe(
    X,
    columns=None,
    index=None
):

    if isinstance(
        X,
        pd.DataFrame
    ):

        return X.copy()

    return pd.DataFrame(
        X,
        columns=columns,
        index=index
    )


# ==========================================================
# CONVERT TO SERIES
# ==========================================================

def to_series(
    y,
    name="target"
):

    if isinstance(
        y,
        pd.Series
    ):

        return y.copy()

    return pd.Series(
        y,
        name=name
    )


# ==========================================================
# SAVE DATAFRAME
# ==========================================================

def save_dataframe(
    df,
    filepath,
    index=False
):

    extension = (
        os.path.splitext(
            filepath
        )[1]
        .lower()
    )

    if extension == ".csv":

        df.to_csv(
            filepath,
            index=index
        )

    elif extension in [
        ".xlsx",
        ".xls"
    ]:

        df.to_excel(
            filepath,
            index=index
        )

    elif extension == ".parquet":

        df.to_parquet(
            filepath,
            index=index
        )

    else:

        raise ValueError(
            "Format non supporté. "
            "Utilisez CSV, Excel "
            "ou Parquet."
        )

    return filepath


# ==========================================================
# REMOVE INF
# ==========================================================

def replace_infinite(
    df,
    value=np.nan
):

    result = df.copy()

    numeric = (
        result.select_dtypes(
            include=np.number
        )
        .columns
    )

    result[numeric] = (
        result[numeric]
        .replace(
            [np.inf, -np.inf],
            value
        )
    )

    return result


# ==========================================================
# REMOVE EMPTY COLUMNS
# ==========================================================

def remove_empty_columns(
    df
):

    result = df.copy()

    return result.dropna(
        axis=1,
        how="all"
    )


# ==========================================================
# REMOVE EMPTY ROWS
# ==========================================================

def remove_empty_rows(
    df
):

    result = df.copy()

    return result.dropna(
        axis=0,
        how="all"
    )


# ==========================================================
# CLEAN COLUMN NAMES
# ==========================================================

def clean_column_names(
    df
):

    result = df.copy()

    result.columns = (

        result.columns
        .astype(str)
        .str.strip()
        .str.replace(
            " ",
            "_",
            regex=False
        )
        .str.replace(
            "-",
            "_",
            regex=False
        )

    )

    return result


# ==========================================================
# SUMMARY DICTIONARY
# ==========================================================

def dataframe_info(
    df
):

    return {

        "rows":
            df.shape[0],

        "columns":
            df.shape[1],

        "numeric_columns":
            get_numeric_columns(df),

        "categorical_columns":
            get_categorical_columns(df),

        "datetime_columns":
            get_datetime_columns(df),

        "constant_columns":
            get_constant_columns(df),

        "missing_values":
            missing_count(df),

        "missing_percentage":
            missing_percentage(df),

        "duplicates":
            duplicate_count(df),

        "duplicate_percentage":
            duplicate_percentage(df),

        "memory_mb":
            memory_usage_mb(df)

    }