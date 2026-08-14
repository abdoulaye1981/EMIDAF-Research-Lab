"""
=========================================================
EMIDAF Framework
Preprocessing Interpretation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ==========================================================
# INTERPRETATION
# ==========================================================

class PreprocessingInterpreter:

    """
    Interpretation engine for preprocessing diagnostics.
    """

    name = "Preprocessing Interpretation"

    # ======================================================
    # MISSING VALUES
    # ======================================================

    @staticmethod
    def missing_values(
        df
    ):

        count = df.isna().sum()

        percentage = (
            count
            / len(df)
            * 100
        )

        result = pd.DataFrame({

            "missing_count":
                count,

            "missing_percentage":
                percentage

        })

        result[
            "status"
        ] = np.where(

            result[
                "missing_count"
            ] == 0,

            "Complete",

            "Missing values"

        )

        return result.sort_values(
            "missing_percentage",
            ascending=False
        )


    # ======================================================
    # DUPLICATES
    # ======================================================

    @staticmethod
    def duplicates(
        df
    ):

        count = df.duplicated().sum()

        percentage = (
            count
            / len(df)
            * 100
        )

        return {

            "duplicate_count":
                count,

            "duplicate_percentage":
                percentage,

            "status":
                (
                    "No duplicates"
                    if count == 0
                    else "Duplicates detected"
                )

        }


    # ======================================================
    # OUTLIERS
    # ======================================================

    @staticmethod
    def outlier_summary(
        df,
        method="iqr"
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        results = []

        for column in numeric.columns:

            values = (
                numeric[column]
                .dropna()
            )

            if len(values) == 0:

                continue

            if method == "iqr":

                q1 = values.quantile(
                    0.25
                )

                q3 = values.quantile(
                    0.75
                )

                iqr = q3 - q1

                lower = (
                    q1 - 1.5 * iqr
                )

                upper = (
                    q3 + 1.5 * iqr
                )

                outliers = (
                    (values < lower)
                    |
                    (values > upper)
                )

            elif method == "zscore":

                mean = values.mean()

                std = values.std()

                if std == 0:

                    outliers = (
                        pd.Series(
                            False,
                            index=values.index
                        )
                    )

                else:

                    z = (
                        (values - mean)
                        / std
                    )

                    outliers = (
                        abs(z) > 3
                    )

            else:

                raise ValueError(
                    "method doit être "
                    "'iqr' ou 'zscore'."
                )

            count = int(
                outliers.sum()
            )

            percentage = (
                count
                / len(values)
                * 100
            )

            results.append({

                "variable":
                    column,

                "outlier_count":
                    count,

                "outlier_percentage":
                    percentage,

                "status":
                    (
                        "Outliers detected"
                        if count > 0
                        else "No outliers"
                    )

            })

        return (
            pd.DataFrame(results)
            .sort_values(
                "outlier_percentage",
                ascending=False
            )
            .reset_index(drop=True)
        )


    # ======================================================
    # SKEWNESS
    # ======================================================

    @staticmethod
    def skewness(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        result = (
            numeric
            .skew()
            .to_frame(
                "skewness"
            )
        )

        def interpret(value):

            if abs(value) < 0.5:

                return "Approximately symmetric"

            if abs(value) < 1:

                return "Moderately asymmetric"

            return "Highly asymmetric"

        result[
            "interpretation"
        ] = result[
            "skewness"
        ].apply(
            interpret
        )

        return result


    # ======================================================
    # KURTOSIS
    # ======================================================

    @staticmethod
    def kurtosis(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        result = (
            numeric
            .kurtosis()
            .to_frame(
                "kurtosis"
            )
        )

        def interpret(value):

            if value > 1:

                return "Leptokurtic"

            if value < -1:

                return "Platykurtic"

            return "Approximately mesokurtic"

        result[
            "interpretation"
        ] = result[
            "kurtosis"
        ].apply(
            interpret
        )

        return result


    # ======================================================
    # COEFFICIENT OF VARIATION
    # ======================================================

    @staticmethod
    def coefficient_variation(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        results = []

        for column in numeric.columns:

            values = (
                numeric[column]
                .dropna()
            )

            mean = values.mean()

            std = values.std()

            if mean == 0:

                cv = np.nan

            else:

                cv = (
                    std
                    / abs(mean)
                    * 100
                )

            results.append({

                "variable":
                    column,

                "mean":
                    mean,

                "std":
                    std,

                "CV_percentage":
                    cv

            })

        return pd.DataFrame(
            results
        )


    # ======================================================
    # NORMALITY
    # ======================================================

    @staticmethod
    def normality_interpretation(
        p_value,
        alpha=0.05
    ):

        if p_value > alpha:

            return (
                "Normality not rejected"
            )

        return (
            "Normality rejected"
        )


    # ======================================================
    # CORRELATION
    # ======================================================

    @staticmethod
    def correlation_strength(
        correlation
    ):

        value = abs(
            correlation
        )

        if value < 0.1:

            return "Negligible"

        if value < 0.3:

            return "Weak"

        if value < 0.5:

            return "Moderate"

        if value < 0.7:

            return "Strong"

        if value < 0.9:

            return "Very strong"

        return "Extremely strong"


    @staticmethod
    def interpret_correlation(
        correlation
    ):

        strength = (
            PreprocessingInterpreter
            .correlation_strength(
                correlation
            )
        )

        direction = (
            "positive"
            if correlation > 0
            else
            "negative"
            if correlation < 0
            else
            "null"
        )

        return (
            f"{strength} {direction} correlation"
        )


    # ======================================================
    # CORRELATION MATRIX
    # ======================================================

    @staticmethod
    def correlation_pairs(
        df,
        threshold=0.8,
        method="pearson"
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        matrix = (
            numeric.corr(
                method=method
            )
        )

        variables = (
            matrix.columns
        )

        results = []

        for i in range(
            len(variables)
        ):

            for j in range(
                i + 1,
                len(variables)
            ):

                correlation = (
                    matrix.loc[
                        variables[i],
                        variables[j]
                    ]
                )

                if abs(
                    correlation
                ) >= threshold:

                    results.append({

                        "variable_1":
                            variables[i],

                        "variable_2":
                            variables[j],

                        "correlation":
                            correlation,

                        "strength":
                            PreprocessingInterpreter
                            .correlation_strength(
                                correlation
                            ),

                        "interpretation":
                            PreprocessingInterpreter
                            .interpret_correlation(
                                correlation
                            )

                    })

        return (
            pd.DataFrame(results)
            .sort_values(
                "correlation",
                key=lambda x: abs(x),
                ascending=False
            )
            .reset_index(drop=True)
        )


    # ======================================================
    # VIF
    # ======================================================

    @staticmethod
    def vif(
        vif_dataframe,
        threshold=5
    ):

        result = (
            vif_dataframe
            .copy()
        )

        if "VIF" not in result.columns:

            raise ValueError(
                "La colonne 'VIF' "
                "est absente."
            )

        result[
            "status"
        ] = np.where(

            result["VIF"] >= threshold,

            "High multicollinearity",

            "Acceptable"

        )

        result[
            "interpretation"
        ] = result[
            "VIF"
        ].apply(

            lambda value:
                (
                    "Severe multicollinearity"
                    if value >= 10
                    else
                    "Moderate multicollinearity"
                    if value >= 5
                    else
                    "Low multicollinearity"
                )

        )

        return result


    # ======================================================
    # ENCODING
    # ======================================================

    @staticmethod
    def encoding_summary(
        df
    ):

        categorical = (
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            )
        )

        results = []

        for column in categorical.columns:

            n_unique = (
                categorical[column]
                .nunique(
                    dropna=False
                )
            )

            results.append({

                "variable":
                    column,

                "unique_values":
                    n_unique,

                "status":
                    (
                        "Low cardinality"
                        if n_unique <= 10
                        else
                        "High cardinality"
                    )

            })

        return pd.DataFrame(
            results
        )


    # ======================================================
    # SCALING
    # ======================================================

    @staticmethod
    def scaling_summary(
        df
    ):

        numeric = (
            df.select_dtypes(
                include=np.number
            )
        )

        results = []

        for column in numeric.columns:

            mean = (
                numeric[column]
                .mean()
            )

            std = (
                numeric[column]
                .std()
            )

            results.append({

                "variable":
                    column,

                "mean":
                    mean,

                "std":
                    std,

                "approximately_standardized":
                    (
                        abs(mean) < 0.1
                        and
                        abs(std - 1) < 0.1
                    )

            })

        return pd.DataFrame(
            results
        )


    # ======================================================
    # FEATURE SELECTION
    # ======================================================

    @staticmethod
    def feature_selection(
        original_columns,
        selected_columns
    ):

        original = set(
            original_columns
        )

        selected = set(
            selected_columns
        )

        removed = (
            original
            - selected
        )

        return {

            "original_features":
                len(original),

            "selected_features":
                len(selected),

            "removed_features":
                len(removed),

            "features_removed":
                sorted(
                    removed
                ),

            "features_selected":
                sorted(
                    selected
                )

        }


    # ======================================================
    # COMPLETE DATASET DIAGNOSTIC
    # ======================================================

    @staticmethod
    def complete_diagnostic(
        df
    ):

        return {

            "shape":
                df.shape,

            "missing":
                PreprocessingInterpreter
                .missing_values(
                    df
                ),

            "duplicates":
                PreprocessingInterpreter
                .duplicates(
                    df
                ),

            "outliers":
                PreprocessingInterpreter
                .outlier_summary(
                    df
                ),

            "skewness":
                PreprocessingInterpreter
                .skewness(
                    df
                ),

            "kurtosis":
                PreprocessingInterpreter
                .kurtosis(
                    df
                ),

            "coefficient_variation":
                PreprocessingInterpreter
                .coefficient_variation(
                    df
                ),

            "encoding":
                PreprocessingInterpreter
                .encoding_summary(
                    df
                )

        }


# ==========================================================
# PUBLIC API
# ==========================================================

class Interpreter:

    missing_values = (
        PreprocessingInterpreter
        .missing_values
    )

    duplicates = (
        PreprocessingInterpreter
        .duplicates
    )

    outlier_summary = (
        PreprocessingInterpreter
        .outlier_summary
    )

    skewness = (
        PreprocessingInterpreter
        .skewness
    )

    kurtosis = (
        PreprocessingInterpreter
        .kurtosis
    )

    coefficient_variation = (
        PreprocessingInterpreter
        .coefficient_variation
    )

    normality_interpretation = (
        PreprocessingInterpreter
        .normality_interpretation
    )

    correlation_strength = (
        PreprocessingInterpreter
        .correlation_strength
    )

    interpret_correlation = (
        PreprocessingInterpreter
        .interpret_correlation
    )

    correlation_pairs = (
        PreprocessingInterpreter
        .correlation_pairs
    )

    vif = (
        PreprocessingInterpreter
        .vif
    )

    encoding_summary = (
        PreprocessingInterpreter
        .encoding_summary
    )

    scaling_summary = (
        PreprocessingInterpreter
        .scaling_summary
    )

    feature_selection = (
        PreprocessingInterpreter
        .feature_selection
    )

    complete_diagnostic = (
        PreprocessingInterpreter
        .complete_diagnostic
    )