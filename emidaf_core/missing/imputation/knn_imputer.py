"""
=========================================================
EMIDAF Framework v1.0
KNN Imputer
---------------------------------------------------------
Imputation des valeurs manquantes par K-Nearest Neighbors.
=========================================================
"""

from __future__ import annotations

import pandas as pd

from sklearn.impute import KNNImputer as SKKNNImputer

from emidaf_core.missing.imputation.base_imputer import (
    BaseImputer,
)


class KNNImputer(BaseImputer):
    """
    Imputation KNN pour variables numériques.

    Les colonnes non numériques ne sont pas transformées.
    """

    name = "KNN"

    def __init__(
        self,
        n_neighbors: int = 5,
        weights: str = "uniform",
    ) -> None:

        if not isinstance(
            n_neighbors,
            int,
        ):
            raise TypeError(
                "n_neighbors must be an integer."
            )

        if n_neighbors < 1:
            raise ValueError(
                "n_neighbors must be greater than or equal to 1."
            )

        if weights not in {
            "uniform",
            "distance",
        }:
            raise ValueError(
                "weights must be 'uniform' or 'distance'."
            )

        self.n_neighbors = n_neighbors
        self.weights = weights

    # =====================================================
    # IMPUTATION
    # =====================================================

    def impute(
        self,
        dataframe: pd.DataFrame,
        columns: list[str],
        **kwargs,
    ) -> pd.DataFrame:

        if not columns:
            return dataframe

        non_numeric_columns = [
            column
            for column in columns
            if not pd.api.types.is_numeric_dtype(
                dataframe[column]
            )
        ]

        if non_numeric_columns:
            raise TypeError(
                "KNN imputation requires numeric columns. "
                "Non-numeric column(s): "
                + ", ".join(
                    non_numeric_columns
                )
            )

        fully_missing_columns = [
            column
            for column in columns
            if dataframe[column].notna().sum() == 0
        ]

        if fully_missing_columns:
            raise ValueError(
                "KNN imputation cannot be applied to "
                "entirely missing column(s): "
                + ", ".join(
                    fully_missing_columns
                )
            )

        imputer = SKKNNImputer(
            n_neighbors=self.n_neighbors,
            weights=self.weights,
        )

        transformed = imputer.fit_transform(
            dataframe[
                columns
            ]
        )

        dataframe.loc[
            :,
            columns,
        ] = transformed

        return dataframe
