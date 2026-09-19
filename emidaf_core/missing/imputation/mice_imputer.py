"""
=========================================================
EMIDAF Framework v1.0
MICE Imputer
---------------------------------------------------------
Imputation multivariée itérative inspirée de MICE.
=========================================================
"""

from __future__ import annotations

import pandas as pd

from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

from emidaf_core.missing.imputation.base_imputer import (
    BaseImputer,
)


class MICEImputer(BaseImputer):
    """
    Imputation multivariée itérative pour variables numériques.

    Remarque :
    sklearn IterativeImputer correspond à une approche
    d'imputation itérative de type MICE-like.

    Ce composant n'est pas une implémentation complète
    de multiple imputation avec génération de plusieurs
    jeux imputés.
    """

    name = "MICE"

    def __init__(
        self,
        max_iter: int = 10,
        random_state: int | None = 42,
        initial_strategy: str = "mean",
        sample_posterior: bool = False,
    ) -> None:

        if not isinstance(
            max_iter,
            int,
        ):
            raise TypeError(
                "max_iter must be an integer."
            )

        if max_iter < 1:
            raise ValueError(
                "max_iter must be greater than or equal to 1."
            )

        if (
            random_state is not None
            and not isinstance(
                random_state,
                int,
            )
        ):
            raise TypeError(
                "random_state must be an integer or None."
            )

        allowed_initial_strategies = {
            "mean",
            "median",
            "most_frequent",
            "constant",
        }

        if (
            initial_strategy
            not in allowed_initial_strategies
        ):
            raise ValueError(
                "initial_strategy must be one of: "
                "'mean', 'median', 'most_frequent', "
                "'constant'."
            )

        if not isinstance(
            sample_posterior,
            bool,
        ):
            raise TypeError(
                "sample_posterior must be a boolean."
            )

        self.max_iter = max_iter
        self.random_state = random_state
        self.initial_strategy = initial_strategy
        self.sample_posterior = sample_posterior

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
                "MICE imputation requires numeric columns. "
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
                "MICE imputation cannot be applied to "
                "entirely missing column(s): "
                + ", ".join(
                    fully_missing_columns
                )
            )

        imputer = IterativeImputer(
            max_iter=self.max_iter,
            random_state=self.random_state,
            initial_strategy=self.initial_strategy,
            sample_posterior=self.sample_posterior,
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
