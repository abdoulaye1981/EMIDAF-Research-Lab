"""
=========================================================
EMIDAF Framework
Feature Selection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import pearsonr, spearmanr

from sklearn.feature_selection import (
    VarianceThreshold,
    SelectKBest,
    SelectPercentile,
    f_classif,
    f_regression,
    chi2,
    mutual_info_classif,
    mutual_info_regression
)

from sklearn.feature_selection import RFE

from sklearn.base import clone

from .base import (
    BasePreprocessing,
    PreprocessingResult
)
# ==========================================================
# FEATURE SELECTION
# ==========================================================

class FeatureSelection(
    BasePreprocessing
):

    """
    Complete feature selection engine.
    """

    name = "Feature Selection"

    def __init__(
        self,
        method="variance"
    ):

        self.method = method
        self.selector = None
        self.features = None
        self.scores = None
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
# VARIANCE THRESHOLD
# ==========================================================

    @staticmethod
    def variance_threshold(
        X,
        threshold=0.0
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        if numeric.empty:

            raise ValueError(
                "Aucune variable numérique."
            )

        selector = VarianceThreshold(
            threshold=threshold
        )

        selector.fit(
            numeric
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        removed = list(
            numeric.columns[
                ~selector.get_support()
            ]
        )

        return {
            "selected": selected,
            "removed": removed,
            "selector": selector
        }
    # ==========================================================
# PEARSON
# ==========================================================

    @staticmethod
    def correlation_pearson(
        X,
        y,
        threshold=0.0
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        results = []

        for column in numeric.columns:

            data = pd.concat(
                [
                    numeric[column],
                    pd.Series(
                        y,
                        index=numeric.index,
                        name="target"
                    )
                ],
                axis=1
            ).dropna()

            if len(data) < 3:

                continue

            correlation, pvalue = pearsonr(
                data[column],
                data["target"]
            )

            results.append({

                "variable": column,

                "correlation": correlation,

                "abs_correlation":
                    abs(correlation),

                "p_value": pvalue,

                "selected":
                    abs(correlation)
                    >= threshold

            })

        return (
            pd.DataFrame(results)
            .sort_values(
                "abs_correlation",
                ascending=False
            )
            .reset_index(drop=True)
        )
    # ==========================================================
# SPEARMAN
# ==========================================================

    @staticmethod
    def correlation_spearman(
        X,
        y,
        threshold=0.0
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        results = []

        for column in numeric.columns:

            data = pd.concat(
                [
                    numeric[column],
                    pd.Series(
                        y,
                        index=numeric.index,
                        name="target"
                    )
                ],
                axis=1
            ).dropna()

            if len(data) < 3:

                continue

            correlation, pvalue = spearmanr(
                data[column],
                data["target"]
            )

            results.append({

                "variable": column,

                "correlation": correlation,

                "abs_correlation":
                    abs(correlation),

                "p_value": pvalue,

                "selected":
                    abs(correlation)
                    >= threshold

            })

        return (
            pd.DataFrame(results)
            .sort_values(
                "abs_correlation",
                ascending=False
            )
            .reset_index(drop=True)
        )
    # ==========================================================
# ANOVA
# ==========================================================

    @staticmethod
    def anova(
        X,
        y,
        k=10
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        k = min(
            k,
            numeric.shape[1]
        )

        selector = SelectKBest(
            score_func=f_classif,
            k=k
        )

        selector.fit(
            numeric,
            y
        )

        scores = pd.DataFrame({

            "variable":
                numeric.columns,

            "score":
                selector.scores_,

            "p_value":
                selector.pvalues_

        }).sort_values(
            "score",
            ascending=False
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        return {
            "selected": selected,
            "scores": scores,
            "selector": selector
        }
    # ==========================================================
# CHI SQUARE
# ==========================================================

    @staticmethod
    def chi2(
        X,
        y,
        k=10
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        if (numeric < 0).any().any():

            raise ValueError(
                "Le test du chi² nécessite "
                "des variables non négatives."
            )

        k = min(
            k,
            numeric.shape[1]
        )

        selector = SelectKBest(
            score_func=chi2,
            k=k
        )

        selector.fit(
            numeric,
            y
        )

        scores = pd.DataFrame({

            "variable":
                numeric.columns,

            "score":
                selector.scores_,

            "p_value":
                selector.pvalues_

        }).sort_values(
            "score",
            ascending=False
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        return {
            "selected": selected,
            "scores": scores,
            "selector": selector
        }
    # ==========================================================
# MUTUAL INFORMATION CLASSIFICATION
# ==========================================================

    @staticmethod
    def mutual_information_classification(
        X,
        y,
        k=10
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        k = min(
            k,
            numeric.shape[1]
        )

        selector = SelectKBest(
            score_func=mutual_info_classif,
            k=k
        )

        selector.fit(
            numeric,
            y
        )

        scores = pd.DataFrame({

            "variable":
                numeric.columns,

            "score":
                selector.scores_

        }).sort_values(
            "score",
            ascending=False
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        return {
            "selected": selected,
            "scores": scores,
            "selector": selector
        }
    # ==========================================================
# MUTUAL INFORMATION REGRESSION
# ==========================================================

    @staticmethod
    def mutual_information_regression(
        X,
        y,
        k=10
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        k = min(
            k,
            numeric.shape[1]
        )

        selector = SelectKBest(
            score_func=mutual_info_regression,
            k=k
        )

        selector.fit(
            numeric,
            y
        )

        scores = pd.DataFrame({

            "variable":
                numeric.columns,

            "score":
                selector.scores_

        }).sort_values(
            "score",
            ascending=False
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        return {
            "selected": selected,
            "scores": scores,
            "selector": selector
        }
    # ==========================================================
# PERCENTILE
# ==========================================================

    @staticmethod
    def percentile(
        X,
        y,
        percentile=50,
        task="classification"
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        if task == "classification":

            score_function = f_classif

        elif task == "regression":

            score_function = f_regression

        else:

            raise ValueError(
                "task doit être "
                "'classification' ou 'regression'."
            )

        selector = SelectPercentile(
            score_func=score_function,
            percentile=percentile
        )

        selector.fit(
            numeric,
            y
        )

        selected = list(
            numeric.columns[
                selector.get_support()
            ]
        )

        scores = pd.DataFrame({

            "variable":
                numeric.columns,

            "score":
                selector.scores_,

            "p_value":
                selector.pvalues_

        }).sort_values(
            "score",
            ascending=False
        )

        return {
            "selected": selected,
            "scores": scores,
            "selector": selector
        }
    # ==========================================================
# RFE
# ==========================================================

    @staticmethod
    def rfe(
        X,
        y,
        estimator,
        n_features_to_select=None,
        step=1
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        if n_features_to_select is None:

            n_features_to_select = max(
                1,
                numeric.shape[1] // 2
            )

        selector = RFE(

            estimator=clone(
                estimator
            ),

            n_features_to_select=
                n_features_to_select,

            step=step

        )

        selector.fit(
            numeric,
            y
        )

        results = pd.DataFrame({

            "variable":
                numeric.columns,

            "selected":
                selector.support_,

            "ranking":
                selector.ranking_

        }).sort_values(
            "ranking"
        )

        selected = list(
            numeric.columns[
                selector.support_
            ]
        )

        return {
            "selected": selected,
            "results": results,
            "selector": selector
        }
    # ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

    @staticmethod
    def importance(
        X,
        y,
        estimator,
        threshold=None
    ):

        numeric = X.select_dtypes(
            include=np.number
        )

        model = clone(
            estimator
        )

        model.fit(
            numeric,
            y
        )

        if hasattr(
            model,
            "feature_importances_"
        ):

            importance = (
                model.feature_importances_
            )

        elif hasattr(
            model,
            "coef_"
        ):

            coef = model.coef_

            if np.ndim(coef) > 1:

                importance = np.mean(
                    np.abs(coef),
                    axis=0
                )

            else:

                importance = np.abs(
                    coef
                )

        else:

            raise ValueError(
                "L'estimateur doit fournir "
                "'feature_importances_' ou 'coef_'."
            )

        results = pd.DataFrame({

            "variable":
                numeric.columns,

            "importance":
                importance

        }).sort_values(
            "importance",
            ascending=False
        )

        if threshold is None:

            threshold = (
                results["importance"]
                .median()
            )

        results["selected"] = (
            results["importance"]
            >= threshold
        )

        selected = list(
            results.loc[
                results["selected"],
                "variable"
            ]
        )

        return {
            "selected": selected,
            "results": results,
            "model": model
        }
    # ==========================================================
# APPLY SELECTION
# ==========================================================

    @staticmethod
    def select(
        X,
        selected_features
    ):

        selected_features = list(
            selected_features
        )

        missing = [
            column
            for column in selected_features
            if column not in X.columns
        ]

        if missing:

            raise KeyError(
                f"Variables inexistantes : {missing}"
            )

        return X[
            selected_features
        ].copy()
    # ==========================================================
# COMPARE CORRELATIONS
# ==========================================================

    @staticmethod
    def compare_correlations(
        X,
        y
    ):

        pearson = (
            FeatureSelection
            .correlation_pearson(
                X,
                y
            )
        )

        spearman = (
            FeatureSelection
            .correlation_spearman(
                X,
                y
            )
        )

        result = pearson[
            [
                "variable",
                "correlation",
                "p_value"
            ]
        ].rename(
            columns={
                "correlation":
                    "pearson",
                "p_value":
                    "pearson_pvalue"
            }
        )

        spearman = spearman[
            [
                "variable",
                "correlation",
                "p_value"
            ]
        ].rename(
            columns={
                "correlation":
                    "spearman",
                "p_value":
                    "spearman_pvalue"
            }
        )

        result = result.merge(
            spearman,
            on="variable",
            how="outer"
        )

        return result
    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        if y is None:

            raise ValueError(
                "La variable cible y est nécessaire."
            )

        if self.method == "variance":

            self.result = (
                self.variance_threshold(
                    X
                )
            )

            self.features = (
                self.result["selected"]
            )

        else:

            raise ValueError(
                "Pour fit(), utiliser "
                "'variance'."
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
                "Le sélecteur doit être ajusté "
                "avec fit()."
            )

        return self.select(
            X,
            self.features
        )
    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        X
    ):

        numeric = (
            FeatureSelection
            .numeric_columns(X)
        )

        result = PreprocessingResult(

            step="Feature Selection",

            input_shape=X.shape,

            output_shape=X.shape,

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

class Selector:

    numeric_columns = (
        FeatureSelection.numeric_columns
    )

    variance = (
        FeatureSelection.variance_threshold
    )

    pearson = (
        FeatureSelection.correlation_pearson
    )

    spearman = (
        FeatureSelection.correlation_spearman
    )

    compare_correlations = (
        FeatureSelection.compare_correlations
    )

    anova = (
        FeatureSelection.anova
    )

    chi2 = (
        FeatureSelection.chi2
    )

    mutual_info_classification = (
        FeatureSelection
        .mutual_information_classification
    )

    mutual_info_regression = (
        FeatureSelection
        .mutual_information_regression
    )

    percentile = (
        FeatureSelection.percentile
    )

    rfe = FeatureSelection.rfe

    importance = (
        FeatureSelection.importance
    )

    select = FeatureSelection.select

    inspect = FeatureSelection.inspect