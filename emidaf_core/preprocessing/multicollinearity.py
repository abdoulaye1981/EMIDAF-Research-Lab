"""
=========================================================
EMIDAF Framework
Multicollinearity Analysis
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import pearsonr, spearmanr

from statsmodels.stats.outliers_influence import (
    variance_inflation_factor
)

from statsmodels.tools.tools import (
    add_constant
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)
# ==========================================================
# MULTICOLLINEARITY
# ==========================================================

class Multicollinearity(
    BasePreprocessing
):

    """
    Complete multicollinearity analysis engine.
    """

    name = "Multicollinearity"

    def __init__(
        self,
        method="pearson",
        threshold=0.8,
        vif_threshold=5.0
    ):

        self.method = method
        self.threshold = threshold
        self.vif_threshold = vif_threshold

        self.correlation_matrix = None
        self.vif_results = None
        self.high_correlations = None
        self.features = None
        self.result = None
    # ==========================================================
# NUMERIC COLUMNS
# ==========================================================

    @staticmethod
    def numeric_columns(
        df
    ):

        return list(
            df.select_dtypes(
                include=np.number
            ).columns
        )
    # ==========================================================
# PEARSON CORRELATION MATRIX
# ==========================================================

    @staticmethod
    def pearson_matrix(
        df,
        columns=None
    ):

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        if not columns:

            raise ValueError(
                "Aucune variable numérique."
            )

        return df[
            columns
        ].corr(
            method="pearson"
        )
    # ==========================================================
# SPEARMAN CORRELATION MATRIX
# ==========================================================

    @staticmethod
    def spearman_matrix(
        df,
        columns=None
    ):

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        if not columns:

            raise ValueError(
                "Aucune variable numérique."
            )

        return df[
            columns
        ].corr(
            method="spearman"
        )
    # ==========================================================
# CORRELATION MATRIX
# ==========================================================

    @staticmethod
    def correlation_matrix(
        df,
        columns=None,
        method="pearson"
    ):

        if method not in [
            "pearson",
            "spearman",
            "kendall"
        ]:

            raise ValueError(
                "method doit être "
                "'pearson', 'spearman' ou 'kendall'."
            )

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        return df[
            columns
        ].corr(
            method=method
        )
    # ==========================================================
# HIGH CORRELATIONS
# ==========================================================

    @staticmethod
    def high_correlations(
        df,
        threshold=0.8,
        method="pearson",
        absolute=True
    ):

        matrix = (
            Multicollinearity
            .correlation_matrix(
                df,
                method=method
            )
        )

        variables = matrix.columns

        results = []

        for i in range(
            len(variables)
        ):

            for j in range(
                i + 1,
                len(variables)
            ):

                variable1 = variables[i]
                variable2 = variables[j]

                correlation = (
                    matrix.loc[
                        variable1,
                        variable2
                    ]
                )

                value = (
                    abs(correlation)
                    if absolute
                    else correlation
                )

                if value >= threshold:

                    results.append({

                        "variable_1":
                            variable1,

                        "variable_2":
                            variable2,

                        "correlation":
                            correlation,

                        "absolute_correlation":
                            abs(correlation),

                        "threshold":
                            threshold

                    })

        result = pd.DataFrame(
            results
        )

        if not result.empty:

            result = result.sort_values(
                "absolute_correlation",
                ascending=False
            ).reset_index(
                drop=True
            )

        return result
    # ==========================================================
# VIF
# ==========================================================

    @staticmethod
    def vif(
        df,
        columns=None,
        add_intercept=True
    ):

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        if not columns:

            raise ValueError(
                "Aucune variable numérique."
            )

        data = df[
            columns
        ].copy()

        if data.isna().any().any():

            raise ValueError(
                "Les variables contiennent "
                "des valeurs manquantes. "
                "Traitez les valeurs manquantes "
                "avant le calcul du VIF."
            )

        if add_intercept:

            data = add_constant(
                data,
                has_constant="add"
            )

        results = []

        for index, column in enumerate(
            data.columns
        ):

            if column == "const":

                continue

            try:

                vif_value = (
                    variance_inflation_factor(
                        data.values,
                        index
                    )
                )

            except Exception:

                vif_value = np.inf

            tolerance = (
                1 / vif_value
                if np.isfinite(vif_value)
                and vif_value != 0
                else 0
            )

            results.append({

                "variable":
                    column,

                "VIF":
                    vif_value,

                "Tolerance":
                    tolerance

            })

        return (
            pd.DataFrame(results)
            .sort_values(
                "VIF",
                ascending=False
            )
            .reset_index(drop=True)
        )
    # ==========================================================
# VIF INTERPRETATION
# ==========================================================

    @staticmethod
    def interpret_vif(
        vif_value
    ):

        if np.isinf(vif_value):

            return (
                "Multicolinéarité parfaite "
                "ou quasi parfaite"
            )

        if vif_value < 5:

            return (
                "Multicolinéarité faible "
                "ou acceptable"
            )

        if vif_value < 10:

            return (
                "Multicolinéarité modérée "
                "à surveiller"
            )

        return (
            "Forte multicolinéarité"
        )
    # ==========================================================
# VIF DIAGNOSTIC
# ==========================================================

    @staticmethod
    def vif_diagnostic(
        df,
        columns=None,
        vif_threshold=5.0
    ):

        result = (
            Multicollinearity
            .vif(
                df,
                columns=columns
            )
        )

        result[
            "Interpretation"
        ] = result[
            "VIF"
        ].apply(
            Multicollinearity
            .interpret_vif
        )

        result[
            "Problematique"
        ] = (
            result["VIF"]
            >= vif_threshold
        )

        return result
    # ==========================================================
# VARIABLES VIF
# ==========================================================

    @staticmethod
    def variables_vif(
        df,
        columns=None,
        vif_threshold=5.0
    ):

        result = (
            Multicollinearity
            .vif(
                df,
                columns=columns
            )
        )

        selected_for_removal = list(
            result.loc[
                result["VIF"]
                >= vif_threshold,
                "variable"
            ]
        )

        return selected_for_removal
    # ==========================================================
# KEEP VARIABLES
# ==========================================================

    @staticmethod
    def variables_to_keep(
        df,
        columns=None,
        vif_threshold=5.0
    ):

        result = (
            Multicollinearity
            .vif(
                df,
                columns=columns
            )
        )

        return list(
            result.loc[
                result["VIF"]
                < vif_threshold,
                "variable"
            ]
        )
    # ==========================================================
# REMOVE VARIABLES
# ==========================================================

    @staticmethod
    def remove_variables(
        df,
        variables
    ):

        variables = list(
            variables
        )

        missing = [
            variable
            for variable in variables
            if variable not in df.columns
        ]

        if missing:

            raise KeyError(
                f"Variables inexistantes : "
                f"{missing}"
            )

        return df.drop(
            columns=variables
        ).copy()
    # ==========================================================
# VIF ITERATIVE SELECTION
# ==========================================================

    @staticmethod
    def vif_selection(
        df,
        columns=None,
        threshold=5.0,
        max_iterations=100
    ):

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        remaining = list(
            columns
        )

        history = []

        iteration = 0

        while (
            len(remaining) > 1
            and iteration < max_iterations
        ):

            iteration += 1

            current_vif = (
                Multicollinearity
                .vif(
                    df,
                    columns=remaining
                )
            )

            max_row = (
                current_vif
                .iloc[0]
            )

            max_variable = (
                max_row["variable"]
            )

            max_vif = (
                max_row["VIF"]
            )

            history.append({

                "iteration":
                    iteration,

                "variable":
                    max_variable,

                "VIF":
                    max_vif,

                "remaining_variables":
                    len(remaining)

            })

            if max_vif < threshold:

                break

            remaining.remove(
                max_variable
            )

        final_vif = (
            Multicollinearity
            .vif(
                df,
                columns=remaining
            )
        )

        return {

            "selected":
                remaining,

            "removed":
                [
                    column
                    for column in columns
                    if column not in remaining
                ],

            "history":
                pd.DataFrame(history),

            "final_vif":
                final_vif

        }
    # ==========================================================
# COMPLETE DIAGNOSTIC
# ==========================================================

    @staticmethod
    def diagnostic(
        df,
        columns=None,
        correlation_threshold=0.8,
        vif_threshold=5.0,
        method="pearson"
    ):

        if columns is None:

            columns = (
                Multicollinearity
                .numeric_columns(df)
            )

        matrix = (
            Multicollinearity
            .correlation_matrix(
                df,
                columns=columns,
                method=method
            )
        )

        high_corr = (
            Multicollinearity
            .high_correlations(
                df,
                threshold=correlation_threshold,
                method=method
            )
        )

        vif_result = (
            Multicollinearity
            .vif_diagnostic(
                df,
                columns=columns,
                vif_threshold=vif_threshold
            )
        )

        return {

            "correlation_matrix":
                matrix,

            "high_correlations":
                high_corr,

            "vif":
                vif_result

        }
    # ==========================================================
# PEARSON VS SPEARMAN
# ==========================================================

    @staticmethod
    def compare_methods(
        df,
        columns=None
    ):

        pearson = (
            Multicollinearity
            .correlation_matrix(
                df,
                columns=columns,
                method="pearson"
            )
        )

        spearman = (
            Multicollinearity
            .correlation_matrix(
                df,
                columns=columns,
                method="spearman"
            )
        )

        return {

            "pearson":
                pearson,

            "spearman":
                spearman

        }
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        self.features = (
            Multicollinearity
            .numeric_columns(X)
        )

        self.correlation_matrix = (
            Multicollinearity
            .correlation_matrix(
                X,
                columns=self.features,
                method=self.method
            )
        )

        self.high_correlations = (
            Multicollinearity
            .high_correlations(
                X,
                threshold=self.threshold,
                method=self.method
            )
        )

        self.vif_results = (
            Multicollinearity
            .vif(
                X,
                columns=self.features
            )
        )

        return self
    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        if self.features is None:

            raise RuntimeError(
                "Le diagnostic doit être "
                "ajusté avec fit()."
            )

        return X.copy()
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        numeric = (
            Multicollinearity
            .numeric_columns(df)
        )

        result = PreprocessingResult(

            step="Multicollinearity",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=numeric

        )

        result.statistics = {

            "numeric_variables":
                numeric,

            "number_of_variables":
                len(numeric)

        }

        return result
# ==========================================================
# PUBLIC API
# ==========================================================

class MulticollinearityAnalyzer:

    numeric_columns = (
        Multicollinearity
        .numeric_columns
    )

    pearson_matrix = (
        Multicollinearity
        .pearson_matrix
    )

    spearman_matrix = (
        Multicollinearity
        .spearman_matrix
    )

    correlation_matrix = (
        Multicollinearity
        .correlation_matrix
    )

    high_correlations = (
        Multicollinearity
        .high_correlations
    )

    vif = (
        Multicollinearity
        .vif
    )

    interpret_vif = (
        Multicollinearity
        .interpret_vif
    )

    vif_diagnostic = (
        Multicollinearity
        .vif_diagnostic
    )

    variables_vif = (
        Multicollinearity
        .variables_vif
    )

    variables_to_keep = (
        Multicollinearity
        .variables_to_keep
    )

    remove_variables = (
        Multicollinearity
        .remove_variables
    )

    vif_selection = (
        Multicollinearity
        .vif_selection
    )

    diagnostic = (
        Multicollinearity
        .diagnostic
    )

    compare_methods = (
        Multicollinearity
        .compare_methods
    )

    inspect = (
        Multicollinearity
        .inspect
    )