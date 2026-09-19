"""
=========================================================
EMIDAF Framework v1.0
Missing Imputer
---------------------------------------------------------
Orchestrateur des stratégies d'imputation.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from emidaf_core.missing.imputation.base_imputer import (
    BaseImputer,
    ImputationResult,
)
from emidaf_core.missing.imputation.simple_imputer import (
    SimpleImputer,
)
from emidaf_core.missing.imputation.knn_imputer import (
    KNNImputer,
)
from emidaf_core.missing.imputation.mice_imputer import (
    MICEImputer,
)


class MissingImputer:
    """
    Orchestrateur principal des stratégies
    d'imputation EMIDAF.

    Stratégies supportées :

    - NONE
    - MEAN
    - MODE
    - KNN
    - MICE
    - REVIEW
    """

    SUPPORTED_STRATEGIES = {
        "NONE",
        "MEAN",
        "MODE",
        "KNN",
        "MICE",
        "REVIEW",
    }

    # =====================================================
    # PUBLIC
    # =====================================================

    def execute(
        self,
        dataframe: pd.DataFrame,
        strategy: str,
        columns: list[str] | None = None,
        **kwargs: Any,
    ) -> ImputationResult:
        """
        Exécute la stratégie d'imputation demandée.
        """

        BaseImputer._validate_dataframe(
            dataframe
        )

        strategy = self._normalize_strategy(
            strategy
        )

        selected_columns = (
            BaseImputer._resolve_columns(
                dataframe=dataframe,
                columns=columns,
            )
        )

        if strategy == "NONE":
            return self._no_action_result(
                dataframe=dataframe,
                columns=selected_columns,
                strategy="NONE",
                message=(
                    "No imputation was required."
                ),
                action_required=False,
            )

        if strategy == "REVIEW":
            return self._no_action_result(
                dataframe=dataframe,
                columns=selected_columns,
                strategy="REVIEW",
                message=(
                    "Automatic imputation was not applied. "
                    "Manual review is required."
                ),
                action_required=True,
            )

        if strategy == "MEAN":

            imputer = SimpleImputer(
                strategy="MEAN"
            )

        elif strategy == "MODE":

            imputer = SimpleImputer(
                strategy="MODE"
            )

        elif strategy == "KNN":

            imputer = KNNImputer(
                n_neighbors=kwargs.get(
                    "n_neighbors",
                    5,
                ),
                weights=kwargs.get(
                    "weights",
                    "uniform",
                ),
            )

        elif strategy == "MICE":

            imputer = MICEImputer(
                max_iter=kwargs.get(
                    "max_iter",
                    10,
                ),
                random_state=kwargs.get(
                    "random_state",
                    42,
                ),
                initial_strategy=kwargs.get(
                    "initial_strategy",
                    "mean",
                ),
                sample_posterior=kwargs.get(
                    "sample_posterior",
                    False,
                ),
            )

        else:
            raise RuntimeError(
                "Unsupported internal strategy."
            )

        return imputer.execute(
            dataframe=dataframe,
            columns=selected_columns,
        )

    # =====================================================
    # STRATEGY
    # =====================================================

    @classmethod
    def _normalize_strategy(
        cls,
        strategy: str,
    ) -> str:

        if not isinstance(
            strategy,
            str,
        ):
            raise TypeError(
                "strategy must be a string."
            )

        normalized = (
            strategy
            .strip()
            .upper()
        )

        if normalized not in (
            cls.SUPPORTED_STRATEGIES
        ):
            raise ValueError(
                "Unsupported imputation strategy: "
                f"'{strategy}'. "
                "Supported strategies are: "
                + ", ".join(
                    sorted(
                        cls.SUPPORTED_STRATEGIES
                    )
                )
                + "."
            )

        return normalized

    # =====================================================
    # NO ACTION
    # =====================================================

    @staticmethod
    def _no_action_result(
        dataframe: pd.DataFrame,
        columns: list[str],
        strategy: str,
        message: str,
        action_required: bool,
    ) -> ImputationResult:

        missing_count = (
            int(
                dataframe[
                    columns
                ]
                .isna()
                .sum()
                .sum()
            )
            if columns
            else 0
        )

        return ImputationResult(
            dataframe=dataframe.copy(
                deep=True
            ),
            strategy=strategy,
            columns=list(
                columns
            ),
            values_imputed=0,
            success=True,
            message=message,
            details={
                "missing_before": missing_count,
                "missing_after": missing_count,
                "action_required": action_required,
            },
        )
