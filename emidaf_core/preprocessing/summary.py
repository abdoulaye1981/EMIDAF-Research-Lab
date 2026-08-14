"""
=========================================================
EMIDAF Framework
Preprocessing Summary
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ==========================================================
# PREPROCESSING SUMMARY
# ==========================================================

class PreprocessingSummary:

    """
    Central summary engine for preprocessing.
    """

    name = "Preprocessing Summary"

    # ======================================================
    # DATASET OVERVIEW
    # ======================================================

    @staticmethod
    def overview(df):

        return pd.DataFrame({

            "metric": [
                "Rows",
                "Columns",
                "Numeric variables",
                "Categorical variables",
                "Missing values",
                "Duplicate rows"
            ],

            "value": [

                df.shape[0],

                df.shape[1],

                len(
                    df.select_dtypes(
                        include=np.number
                    ).columns
                ),

                len(
                    df.select_dtypes(
                        include=[
                            "object",
                            "category",
                            "bool"
                        ]
                    ).columns
                ),

                int(
                    df.isna().sum().sum()
                ),

                int(
                    df.duplicated().sum()
                )

            ]

        })


    # ======================================================
    # VARIABLE SUMMARY
    # ======================================================

    @staticmethod
    def variable_summary(df):

        rows = []

        for column in df.columns:

            series = df[column]

            dtype = series.dtype

            missing = int(
                series.isna().sum()
            )

            non_missing = int(
                series.notna().sum()
            )

            unique = int(
                series.nunique(
                    dropna=True
                )
            )

            rows.append({

                "variable":
                    column,

                "dtype":
                    str(dtype),

                "non_missing":
                    non_missing,

                "missing":
                    missing,

                "missing_percentage":
                    (
                        missing
                        / len(df)
                        * 100
                    ),

                "unique":
                    unique,

                "constant":
                    unique <= 1

            })

        return pd.DataFrame(
            rows
        )


    # ======================================================
    # NUMERIC SUMMARY
    # ======================================================

    @staticmethod
    def numeric_summary(df):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        if numeric.empty:

            return pd.DataFrame()

        result = pd.DataFrame({

            "count":
                numeric.count(),

            "missing":
                numeric.isna().sum(),

            "mean":
                numeric.mean(),

            "std":
                numeric.std(),

            "min":
                numeric.min(),

            "q1":
                numeric.quantile(
                    0.25
                ),

            "median":
                numeric.median(),

            "q3":
                numeric.quantile(
                    0.75
                ),

            "max":
                numeric.max(),

            "skewness":
                numeric.skew(),

            "kurtosis":
                numeric.kurtosis()

        })

        result[
            "CV_percentage"
        ] = (
            result["std"]
            /
            result["mean"].abs()
            * 100
        )

        return result


    # ======================================================
    # CATEGORICAL SUMMARY
    # ======================================================

    @staticmethod
    def categorical_summary(df):

        categorical = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
        )

        rows = []

        for column in categorical.columns:

            series = categorical[column]

            counts = (
                series
                .value_counts(
                    dropna=False
                )
            )

            if len(counts) > 0:

                mode = counts.index[0]

                mode_frequency = (
                    counts.iloc[0]
                )

            else:

                mode = np.nan

                mode_frequency = 0

            rows.append({

                "variable":
                    column,

                "unique":
                    series.nunique(
                        dropna=True
                    ),

                "missing":
                    series.isna().sum(),

                "mode":
                    mode,

                "mode_frequency":
                    mode_frequency,

                "mode_percentage":
                    (
                        mode_frequency
                        / len(series)
                        * 100
                    )

            })

        return pd.DataFrame(
            rows
        )


    # ======================================================
    # MISSING SUMMARY
    # ======================================================

    @staticmethod
    def missing_summary(df):

        result = pd.DataFrame({

            "variable":
                df.columns,

            "missing_count":
                df.isna().sum().values,

            "missing_percentage":
                (
                    df.isna().mean()
                    .values
                    * 100
                )

        })

        result[
            "status"
        ] = np.where(

            result[
                "missing_count"
            ] == 0,

            "Complete",

            np.where(

                result[
                    "missing_percentage"
                ] < 5,

                "Low missingness",

                np.where(

                    result[
                        "missing_percentage"
                    ] < 20,

                    "Moderate missingness",

                    "High missingness"

                )

            )

        )

        return result.sort_values(
            "missing_percentage",
            ascending=False
        )


    # ======================================================
    # DUPLICATE SUMMARY
    # ======================================================

    @staticmethod
    def duplicate_summary(df):

        duplicate_count = int(
            df.duplicated().sum()
        )

        percentage = (
            duplicate_count
            / len(df)
            * 100
        )

        return pd.DataFrame({

            "metric": [
                "Duplicate rows",
                "Duplicate percentage"
            ],

            "value": [
                duplicate_count,
                percentage
            ]

        })


    # ======================================================
    # OUTLIER SUMMARY
    # ======================================================

    @staticmethod
    def outlier_summary(
        df,
        multiplier=1.5
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        rows = []

        for column in numeric.columns:

            values = (
                numeric[column]
                .dropna()
            )

            if values.empty:

                continue

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

            mask = (
                (values < lower)
                |
                (values > upper)
            )

            count = int(
                mask.sum()
            )

            rows.append({

                "variable":
                    column,

                "Q1":
                    q1,

                "Q3":
                    q3,

                "IQR":
                    iqr,

                "lower_bound":
                    lower,

                "upper_bound":
                    upper,

                "outlier_count":
                    count,

                "outlier_percentage":
                    (
                        count
                        / len(values)
                        * 100
                    )

            })

        return (
            pd.DataFrame(rows)
            .sort_values(
                "outlier_percentage",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


    # ======================================================
    # DISTRIBUTION SUMMARY
    # ======================================================

    @staticmethod
    def distribution_summary(df):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        rows = []

        for column in numeric.columns:

            series = (
                numeric[column]
                .dropna()
            )

            if series.empty:

                continue

            skew = series.skew()

            kurt = series.kurtosis()

            if abs(skew) < 0.5:

                skew_interpretation = (
                    "Approximately symmetric"
                )

            elif abs(skew) < 1:

                skew_interpretation = (
                    "Moderately asymmetric"
                )

            else:

                skew_interpretation = (
                    "Highly asymmetric"
                )

            if kurt > 1:

                kurt_interpretation = (
                    "Leptokurtic"
                )

            elif kurt < -1:

                kurt_interpretation = (
                    "Platykurtic"
                )

            else:

                kurt_interpretation = (
                    "Approximately mesokurtic"
                )

            rows.append({

                "variable":
                    column,

                "skewness":
                    skew,

                "skewness_interpretation":
                    skew_interpretation,

                "kurtosis":
                    kurt,

                "kurtosis_interpretation":
                    kurt_interpretation

            })

        return pd.DataFrame(
            rows
        )


    # ======================================================
    # CORRELATION SUMMARY
    # ======================================================

    @staticmethod
    def correlation_summary(
        df,
        threshold=0.8,
        method="pearson"
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        if numeric.shape[1] < 2:

            return pd.DataFrame()

        matrix = numeric.corr(
            method=method
        )

        rows = []

        columns = matrix.columns

        for i in range(
            len(columns)
        ):

            for j in range(
                i + 1,
                len(columns)
            ):

                correlation = (
                    matrix.iloc[
                        i,
                        j
                    ]
                )

                if abs(
                    correlation
                ) >= threshold:

                    rows.append({

                        "variable_1":
                            columns[i],

                        "variable_2":
                            columns[j],

                        "correlation":
                            correlation,

                        "absolute_correlation":
                            abs(correlation)

                    })

        if not rows:

            return pd.DataFrame(
                columns=[
                    "variable_1",
                    "variable_2",
                    "correlation",
                    "absolute_correlation"
                ]
            )

        return (
            pd.DataFrame(rows)
            .sort_values(
                "absolute_correlation",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )


    # ======================================================
    # TARGET SUMMARY
    # ======================================================

    @staticmethod
    def target_summary(
        y
    ):

        series = pd.Series(
            y,
            name="target"
        )

        counts = (
            series
            .value_counts(
                dropna=False
            )
        )

        percentages = (
            series
            .value_counts(
                normalize=True,
                dropna=False
            )
            * 100
        )

        result = pd.DataFrame({

            "count":
                counts,

            "percentage":
                percentages

        })

        result.index.name = (
            "class"
        )

        return result


    # ======================================================
    # CLASS IMBALANCE
    # ======================================================

    @staticmethod
    def imbalance_summary(
        y
    ):

        distribution = (
            PreprocessingSummary
            .target_summary(
                y
            )
        )

        counts = distribution[
            "count"
        ]

        maximum = counts.max()

        minimum = counts.min()

        if minimum == 0:

            ratio = np.inf

        else:

            ratio = (
                maximum
                / minimum
            )

        return pd.DataFrame({

            "metric": [

                "Majority class",

                "Minority class",

                "Majority count",

                "Minority count",

                "Imbalance ratio"

            ],

            "value": [

                counts.idxmax(),

                counts.idxmin(),

                maximum,

                minimum,

                ratio

            ]

        })


    # ======================================================
    # FEATURE SUMMARY
    # ======================================================

    @staticmethod
    def feature_summary(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        categorical = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
        )

        return pd.DataFrame({

            "type": [

                "Numeric",

                "Categorical",

                "Total"

            ],

            "count": [

                numeric.shape[1],

                categorical.shape[1],

                df.shape[1]

            ]

        })


    # ======================================================
    # COMPLETE SUMMARY
    # ======================================================

    @staticmethod
    def complete_summary(
        df,
        target=None
    ):

        result = {

            "overview":
                PreprocessingSummary
                .overview(df),

            "variables":
                PreprocessingSummary
                .variable_summary(df),

            "numeric":
                PreprocessingSummary
                .numeric_summary(df),

            "categorical":
                PreprocessingSummary
                .categorical_summary(df),

            "missing":
                PreprocessingSummary
                .missing_summary(df),

            "duplicates":
                PreprocessingSummary
                .duplicate_summary(df),

            "outliers":
                PreprocessingSummary
                .outlier_summary(df),

            "distribution":
                PreprocessingSummary
                .distribution_summary(df),

            "correlation":
                PreprocessingSummary
                .correlation_summary(df),

            "features":
                PreprocessingSummary
                .feature_summary(df)

        }

        if target is not None:

            if target in df.columns:

                result["target"] = (
                    PreprocessingSummary
                    .target_summary(
                        df[target]
                    )
                )

                result["imbalance"] = (
                    PreprocessingSummary
                    .imbalance_summary(
                        df[target]
                    )
                )

        return result


# ==========================================================
# PUBLIC API
# ==========================================================

class Summary:

    overview = (
        PreprocessingSummary
        .overview
    )

    variable_summary = (
        PreprocessingSummary
        .variable_summary
    )

    numeric_summary = (
        PreprocessingSummary
        .numeric_summary
    )

    categorical_summary = (
        PreprocessingSummary
        .categorical_summary
    )

    missing_summary = (
        PreprocessingSummary
        .missing_summary
    )

    duplicate_summary = (
        PreprocessingSummary
        .duplicate_summary
    )

    outlier_summary = (
        PreprocessingSummary
        .outlier_summary
    )

    distribution_summary = (
        PreprocessingSummary
        .distribution_summary
    )

    correlation_summary = (
        PreprocessingSummary
        .correlation_summary
    )

    target_summary = (
        PreprocessingSummary
        .target_summary
    )

    imbalance_summary = (
        PreprocessingSummary
        .imbalance_summary
    )

    feature_summary = (
        PreprocessingSummary
        .feature_summary
    )

    complete_summary = (
        PreprocessingSummary
        .complete_summary
    )