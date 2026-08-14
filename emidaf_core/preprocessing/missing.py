"""
=========================================================
EMIDAF Framework
Missing Data Analysis and Imputation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind

from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import (
    SimpleImputer,
    KNNImputer,
    IterativeImputer
)

from .base import (
    BasePreprocessing,
    PreprocessingResult
)

# ==========================================================
# MISSING DATA
# ==========================================================

class MissingData(
    BasePreprocessing
):

    """
    Complete missing-data analysis and imputation engine.
    """

    name = "Missing Data"

    def __init__(
        self,
        strategy="median"
    ):

        self.strategy = strategy
        self.imputer = None
        self.result = None

    # ==========================================================
# FIT
# ==========================================================

    def fit(
        self,
        X,
        y=None
    ):

        if not isinstance(X, pd.DataFrame):

            raise TypeError(
                "X doit être un pandas DataFrame."
            )

        self.imputer = SimpleImputer(
            strategy=self.strategy
        )

        numeric_columns = X.select_dtypes(
            include=np.number
        ).columns

        if len(numeric_columns) > 0:

            self.imputer.fit(
                X[numeric_columns]
            )

        return self

    # ==========================================================
# TRANSFORM
# ==========================================================

    def transform(
        self,
        X
    ):

        if self.imputer is None:

            raise RuntimeError(
                "Le modèle doit être ajusté avec fit()."
            )

        result = X.copy()

        numeric_columns = result.select_dtypes(
            include=np.number
        ).columns

        if len(numeric_columns) > 0:

            result[numeric_columns] = (
                self.imputer.transform(
                    result[numeric_columns]
                )
            )

        return result

    # ==========================================================
# MISSING COUNT
# ==========================================================

    @staticmethod
    def count(
        df
    ):

        return (
            df.isna()
            .sum()
            .sort_values(
                ascending=False
            )
        )

    # ==========================================================
# MISSING PERCENT
# ==========================================================

    @staticmethod
    def percentage(
        df
    ):

        return (
            df.isna()
            .mean()
            .mul(100)
            .round(2)
            .sort_values(
                ascending=False
            )
        )

    # ==========================================================
# MISSING SUMMARY
# ==========================================================

    @staticmethod
    def summary(
        df
    ):

        count = MissingData.count(df)

        percentage = MissingData.percentage(df)

        result = pd.DataFrame({

            "missing_count": count,

            "missing_percent": percentage

        })

        result["complete_count"] = (
            len(df)
            - result["missing_count"]
        )

        result["complete_percent"] = (
            100
            - result["missing_percent"]
        )

        return result

    # ==========================================================
# ROWS WITH MISSING
# ==========================================================

    @staticmethod
    def rows_with_missing(
        df
    ):

        return int(
            df.isna()
            .any(axis=1)
            .sum()
        )

    # ==========================================================
# COLUMNS WITH MISSING
# ==========================================================

    @staticmethod
    def columns_with_missing(
        df
    ):

        return list(
            df.columns[
                df.isna().any()
            ]
        )

    # ==========================================================
# MISSING INDICATOR
# ==========================================================

    @staticmethod
    def indicator(
        df
    ):

        return df.isna().astype(int)

    # ==========================================================
# MISSING PATTERNS
# ==========================================================

    @staticmethod
    def patterns(
        df
    ):

        indicators = (
            df.isna()
            .astype(int)
        )

        patterns = (
            indicators
            .value_counts()
            .reset_index(
                name="frequency"
            )
        )

        return patterns

    # ==========================================================
# DROP ROWS
# ==========================================================

    @staticmethod
    def drop_rows(
        df
    ):

        return df.dropna().copy()

    # ==========================================================
# DROP COLUMNS
# ==========================================================

    @staticmethod
    def drop_columns(
        df,
        threshold=0.5
    ):

        result = df.copy()

        missing_rate = (
            result.isna()
            .mean()
        )

        columns = missing_rate[
            missing_rate > threshold
        ].index

        return result.drop(
            columns=columns
        )

    # ==========================================================
# MEAN IMPUTATION
# ==========================================================

    @staticmethod
    def mean_imputation(
        df
    ):

        result = df.copy()

        columns = result.select_dtypes(
            include=np.number
        ).columns

        if len(columns) == 0:

            return result

        imputer = SimpleImputer(
            strategy="mean"
        )

        result[columns] = imputer.fit_transform(
            result[columns]
        )

        return result

    # ==========================================================
# MEDIAN IMPUTATION
# ==========================================================

    @staticmethod
    def median_imputation(
        df
    ):

        result = df.copy()

        columns = result.select_dtypes(
            include=np.number
        ).columns

        if len(columns) == 0:

            return result

        imputer = SimpleImputer(
            strategy="median"
        )

        result[columns] = imputer.fit_transform(
            result[columns]
        )

        return result

    # ==========================================================
# MODE IMPUTATION
# ==========================================================

    @staticmethod
    def mode_imputation(
        df
    ):

        result = df.copy()

        columns = result.select_dtypes(
            include=["object", "category", "bool"]
        ).columns

        if len(columns) == 0:

            return result

        imputer = SimpleImputer(
            strategy="most_frequent"
        )

        result[columns] = imputer.fit_transform(
            result[columns]
        )

        return result

    # ==========================================================
# KNN IMPUTATION
# ==========================================================

    @staticmethod
    def knn_imputation(
        df,
        n_neighbors=5
    ):

        result = df.copy()

        columns = result.select_dtypes(
            include=np.number
        ).columns

        if len(columns) == 0:

            return result

        imputer = KNNImputer(
            n_neighbors=n_neighbors
        )

        result[columns] = imputer.fit_transform(
            result[columns]
        )

        return result

    # ==========================================================
# MICE IMPUTATION
# ==========================================================

    @staticmethod
    def mice_imputation(
        df,
        max_iter=10,
        random_state=42
    ):

        result = df.copy()

        columns = result.select_dtypes(
            include=np.number
        ).columns

        if len(columns) == 0:

            return result

        imputer = IterativeImputer(
            max_iter=max_iter,
            random_state=random_state
        )

        result[columns] = imputer.fit_transform(
            result[columns]
        )

        return result

    # ==========================================================
# GROUP IMPUTATION
# ==========================================================

    @staticmethod
    def group_median(
        df,
        group_column,
        target_columns
    ):

        result = df.copy()

        for column in target_columns:

            result[column] = (
                result
                .groupby(group_column)[column]
                .transform(
                    lambda x:
                    x.fillna(x.median())
                )
            )

        return result

    # ==========================================================
# MCAR CHI-SQUARE
# ==========================================================

    @staticmethod
    def mcar_chi_square(
        df,
        alpha=0.05
    ):

        results = []

        missing_columns = (
            MissingData
            .columns_with_missing(df)
        )

        categorical_columns = df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns

        for missing_column in missing_columns:

            indicator = (
                df[missing_column]
                .isna()
                .astype(int)
            )

            for variable in categorical_columns:

                if variable == missing_column:

                    continue

                table = pd.crosstab(
                    indicator,
                    df[variable]
                )

                if table.shape[0] < 2:
                    continue

                if table.shape[1] < 2:
                    continue

                try:

                    chi2, p_value, _, _ = (
                        chi2_contingency(table)
                    )

                    results.append({

                        "missing_variable":
                            missing_column,

                        "categorical_variable":
                            variable,

                        "chi2":
                            chi2,

                        "p_value":
                            p_value,

                        "significant":
                            p_value < alpha

                    })

                except ValueError:

                    continue

        return pd.DataFrame(results)

    # ==========================================================
# MAR TEST
# ==========================================================

    @staticmethod
    def mar_ttest(
        df,
        missing_variable,
        correlated_variables,
        alpha=0.05
    ):

        results = []

        missing_indicator = (
            df[missing_variable]
            .isna()
        )

        for variable in correlated_variables:

            if variable == missing_variable:
                continue

            if not pd.api.types.is_numeric_dtype(
                df[variable]
            ):
                continue

            group_missing = (
                df.loc[
                    missing_indicator,
                    variable
                ]
                .dropna()
            )

            group_observed = (
                df.loc[
                    ~missing_indicator,
                    variable
                ]
                .dropna()
            )

            if len(group_missing) < 2:
                continue

            if len(group_observed) < 2:
                continue

            statistic, p_value = ttest_ind(
                group_missing,
                group_observed,
                equal_var=False
            )

            results.append({

                "missing_variable":
                    missing_variable,

                "variable":
                    variable,

                "statistic":
                    statistic,

                "p_value":
                    p_value,

                "significant":
                    p_value < alpha

            })

        return pd.DataFrame(results)

    # ==========================================================
# MECHANISM CLASSIFICATION
# ==========================================================

    @staticmethod
    def classify_mechanism(
        df,
        alpha=0.05
    ):

        results = []

        missing_columns = (
            MissingData
            .columns_with_missing(df)
        )

        numeric_columns = list(
            df.select_dtypes(
                include=np.number
            ).columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "bool"
                ]
            ).columns
        )

        for missing_column in missing_columns:

            chi_results = (
                MissingData.mcar_chi_square(
                    df,
                    alpha
                )
            )

            if len(chi_results) > 0:

                current_chi = chi_results[
                    chi_results[
                        "missing_variable"
                    ]
                    == missing_column
                ]

                chi_significant = (
                    current_chi[
                        "significant"
                    ].any()
                )

            else:

                chi_significant = False

            correlated = [
                column
                for column in numeric_columns
                if column != missing_column
            ]

            mar_results = (
                MissingData.mar_ttest(
                    df,
                    missing_column,
                    correlated,
                    alpha
                )
            )

            mar_significant = False

            if len(mar_results) > 0:

                mar_significant = (
                    mar_results[
                        "significant"
                    ].any()
                )

            if (
                not chi_significant
                and not mar_significant
            ):

                mechanism = "MCAR"

            elif mar_significant:

                mechanism = "MAR"

            else:

                mechanism = "MNAR"

            results.append({

                "variable":
                    missing_column,

                "mechanism":
                    mechanism,

                "chi_square_evidence":
                    chi_significant,

                "mar_evidence":
                    mar_significant

            })

        return pd.DataFrame(results)

    # ==========================================================
# INSPECT
# ==========================================================

    @staticmethod
    def inspect(
        df
    ):

        result = PreprocessingResult(

            step="Missing Data",

            input_shape=df.shape,

            output_shape=df.shape,

            variables=list(
                df.columns
            )
        )

        summary = MissingData.summary(df)

        result.statistics = {

            "summary":
                summary,

            "missing_rows":
                MissingData.rows_with_missing(
                    df
                ),

            "missing_columns":
                MissingData.columns_with_missing(
                    df
                ),

            "patterns":
                MissingData.patterns(
                    df
                ),

            "mechanisms":
                MissingData.classify_mechanism(
                    df
                )

        }

        return result

    # ==========================================================
# SERVICE
# ==========================================================

class Missing:

    count = MissingData.count

    percentage = MissingData.percentage

    summary = MissingData.summary

    rows_with_missing = (
        MissingData.rows_with_missing
    )

    columns_with_missing = (
        MissingData.columns_with_missing
    )

    indicator = MissingData.indicator

    patterns = MissingData.patterns

    drop_rows = MissingData.drop_rows

    drop_columns = MissingData.drop_columns

    mean_imputation = (
        MissingData.mean_imputation
    )

    median_imputation = (
        MissingData.median_imputation
    )

    mode_imputation = (
        MissingData.mode_imputation
    )

    knn_imputation = (
        MissingData.knn_imputation
    )

    mice_imputation = (
        MissingData.mice_imputation
    )

    group_median = (
        MissingData.group_median
    )

    mcar_chi_square = (
        MissingData.mcar_chi_square
    )

    mar_ttest = (
        MissingData.mar_ttest
    )

    classify_mechanism = (
        MissingData.classify_mechanism
    )

    inspect = MissingData.inspect