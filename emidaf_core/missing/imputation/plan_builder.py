"""
=========================================================
EMIDAF Framework v1.0
Imputation Plan Builder
---------------------------------------------------------
Construction automatique d'un plan d'imputation à partir
du rapport produit par MissingAnalyzer.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from emidaf_core.missing.imputation.imputation_plan import (
    ColumnImputationDecision,
    ImputationPlan,
)


class ImputationPlanBuilder:
    """
    Construit automatiquement un ImputationPlan
    à partir du rapport de MissingAnalyzer.

    Formats acceptés pour imputation_candidates :

    1. Format réel produit par MissingAnalyzer :

        [
            {
                "column": "age",
                "dtype": "float64",
                "missing_percentage": 3.0,
                "recommended_strategy": "Mean",
            }
        ]

    2. Format dictionnaire historique/interne :

        {
            "age": {
                "strategy": "MEAN"
            }
        }

    Pour KNN et MICE, les predictors sont sélectionnés
    parmi les variables numériques disponibles.
    """

    def __init__(
        self,
        max_predictors: int = 5,
    ) -> None:

        if not isinstance(
            max_predictors,
            int,
        ):
            raise TypeError(
                "max_predictors must be an integer."
            )

        if max_predictors < 1:
            raise ValueError(
                "max_predictors must be greater than "
                "or equal to 1."
            )

        self.max_predictors = max_predictors

    # =====================================================
    # PUBLIC
    # =====================================================

    def build(
        self,
        report: dict[str, Any],
        dataframe: pd.DataFrame,
    ) -> ImputationPlan:

        self._validate_inputs(
            report=report,
            dataframe=dataframe,
        )

        candidates = report.get(
            "imputation_candidates",
            [],
        )

        normalized_candidates = (
            self._normalize_candidates(
                candidates
            )
        )

        plan = ImputationPlan(
            source="MissingAnalyzer",
            generated_automatically=True,
        )

        for column, candidate in (
            normalized_candidates.items()
        ):

            if column not in dataframe.columns:
                continue

            decision = self._build_decision(
                dataframe=dataframe,
                column=column,
                candidate=candidate,
            )

            plan.add(
                decision
            )

        return plan

    # =====================================================
    # CANDIDATES NORMALIZATION
    # =====================================================

    @classmethod
    def _normalize_candidates(
        cls,
        candidates: Any,
    ) -> dict[str, Any]:
        """
        Normalise la collection complète des candidats.
        """

        if isinstance(
            candidates,
            dict,
        ):
            return candidates

        if isinstance(
            candidates,
            list,
        ):

            normalized: dict[
                str,
                Any,
            ] = {}

            for candidate in candidates:

                if not isinstance(
                    candidate,
                    dict,
                ):
                    raise TypeError(
                        "Each item in "
                        "report['imputation_candidates'] "
                        "must be a dictionary."
                    )

                column = candidate.get(
                    "column"
                )

                if (
                    not isinstance(
                        column,
                        str,
                    )
                    or not column.strip()
                ):
                    raise ValueError(
                        "Each imputation candidate must "
                        "contain a valid 'column'."
                    )

                column = column.strip()

                strategy = candidate.get(
                    "recommended_strategy",
                    candidate.get(
                        "strategy",
                        candidate.get(
                            "method",
                            "REVIEW",
                        ),
                    ),
                )

                normalized[column] = {
                    **candidate,
                    "strategy": strategy,
                }

            return normalized

        raise TypeError(
            "report['imputation_candidates'] "
            "must be a list or dictionary."
        )

    # =====================================================
    # STRATEGY NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_strategy(
        strategy: str,
    ) -> str:
        """
        Normalise les libellés vers le vocabulaire
        canonique EMIDAF.
        """

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

        aliases = {
            "NONE": "NONE",
            "NO IMPUTATION": "NONE",

            "MEAN": "MEAN",
            "AVERAGE": "MEAN",

            "MODE": "MODE",
            "MOST FREQUENT": "MODE",

            "KNN": "KNN",
            "KNN IMPUTATION": "KNN",

            "MICE": "MICE",
            "ITERATIVE": "MICE",
            "ITERATIVE IMPUTATION": "MICE",

            "REVIEW": "REVIEW",
            "REVIEW VARIABLE": "REVIEW",
            "MANUAL REVIEW": "REVIEW",
        }

        return aliases.get(
            normalized,
            normalized,
        )

    # =====================================================
    # CANDIDATE NORMALIZATION
    # =====================================================

    @classmethod
    def _normalize_candidate(
        cls,
        candidate: Any,
    ) -> dict[str, Any]:

        if isinstance(
            candidate,
            str,
        ):

            return {
                "strategy":
                    cls._normalize_strategy(
                        candidate
                    )
            }

        if isinstance(
            candidate,
            dict,
        ):

            strategy = candidate.get(
                "strategy",
                candidate.get(
                    "recommended_strategy",
                    candidate.get(
                        "method",
                        "REVIEW",
                    ),
                ),
            )

            if not isinstance(
                strategy,
                str,
            ):
                raise TypeError(
                    "candidate strategy must be a string."
                )

            return {
                **candidate,
                "strategy":
                    cls._normalize_strategy(
                        strategy
                    ),
            }

        raise TypeError(
            "Each imputation candidate must be "
            "a string or dictionary."
        )

    # =====================================================
    # DECISION
    # =====================================================

    def _build_decision(
        self,
        dataframe: pd.DataFrame,
        column: str,
        candidate: Any,
    ) -> ColumnImputationDecision:

        candidate_data = (
            self._normalize_candidate(
                candidate
            )
        )

        strategy = candidate_data[
            "strategy"
        ]

        missing_rate = self._missing_rate(
            dataframe=dataframe,
            column=column,
        )

        applicable = (
            strategy != "REVIEW"
        )

        predictors: list[str] = []

        parameters: dict[
            str,
            Any,
        ] = {}

        if strategy in {
            "KNN",
            "MICE",
        }:

            predictors = (
                self._select_predictors(
                    dataframe=dataframe,
                    target=column,
                )
            )

            if not predictors:

                return ColumnImputationDecision(
                    column=column,
                    strategy="REVIEW",
                    reason=(
                        "No suitable numeric predictor "
                        "was available for multivariate "
                        "imputation."
                    ),
                    missing_rate=missing_rate,
                    applicable=False,
                    confidence=None,
                    predictors=[],
                    parameters={},
                )

            if strategy == "KNN":

                parameters = {
                    "n_neighbors": 5,
                    "weights": "uniform",
                }

            elif strategy == "MICE":

                parameters = {
                    "max_iter": 10,
                    "random_state": 42,
                    "initial_strategy": "mean",
                    "sample_posterior": False,
                }

        reason = self._build_reason(
            dataframe=dataframe,
            column=column,
            strategy=strategy,
            missing_rate=missing_rate,
        )

        return ColumnImputationDecision(
            column=column,
            strategy=strategy,
            reason=reason,
            missing_rate=missing_rate,
            applicable=applicable,
            confidence=None,
            predictors=predictors,
            parameters=parameters,
        )

    # =====================================================
    # MISSING RATE
    # =====================================================

    @staticmethod
    def _missing_rate(
        dataframe: pd.DataFrame,
        column: str,
    ) -> float:

        if len(
            dataframe
        ) == 0:
            return 0.0

        return round(
            float(
                dataframe[
                    column
                ]
                .isna()
                .mean()
                * 100.0
            ),
            2,
        )

    # =====================================================
    # PREDICTOR SELECTION
    # =====================================================

    def _select_predictors(
        self,
        dataframe: pd.DataFrame,
        target: str,
    ) -> list[str]:

        target_series = dataframe[
            target
        ]

        if not pd.api.types.is_numeric_dtype(
            target_series
        ):
            return []

        candidates = [
            column
            for column
            in dataframe.columns
            if (
                column != target
                and pd.api.types.is_numeric_dtype(
                    dataframe[column]
                )
                and dataframe[
                    column
                ].notna().sum() > 0
            )
        ]

        if not candidates:
            return []

        scored_predictors: list[
            tuple[str, float]
        ] = []

        for predictor in candidates:

            pair = dataframe[
                [
                    target,
                    predictor,
                ]
            ].dropna()

            if len(
                pair
            ) < 3:

                score = 0.0

            else:

                correlation = (
                    pair[
                        target
                    ].corr(
                        pair[
                            predictor
                        ]
                    )
                )

                if pd.isna(
                    correlation
                ):
                    score = 0.0

                else:
                    score = abs(
                        float(
                            correlation
                        )
                    )

            scored_predictors.append(
                (
                    predictor,
                    score,
                )
            )

        scored_predictors.sort(
            key=lambda item: (
                item[1],
                item[0],
            ),
            reverse=True,
        )

        return [
            predictor
            for predictor, _
            in scored_predictors[
                :self.max_predictors
            ]
        ]

    # =====================================================
    # REASON
    # =====================================================

    @staticmethod
    def _build_reason(
        dataframe: pd.DataFrame,
        column: str,
        strategy: str,
        missing_rate: float,
    ) -> str:

        is_numeric = (
            pd.api.types.is_numeric_dtype(
                dataframe[
                    column
                ]
            )
        )

        if strategy == "NONE":

            return (
                "No missing values require imputation."
            )

        if strategy == "MEAN":

            return (
                "Low missing rate in a numeric variable; "
                "mean imputation selected."
            )

        if strategy == "MODE":

            return (
                "Low missing rate in a categorical or "
                "discrete variable; mode imputation selected."
            )

        if strategy == "KNN":

            return (
                "Moderate missingness in a numeric variable; "
                "KNN imputation selected using auxiliary "
                "numeric predictors."
            )

        if strategy == "MICE":

            return (
                "Substantial missingness in a numeric variable; "
                "multivariate iterative imputation selected."
            )

        if strategy == "REVIEW":

            if missing_rate >= 40.0:
                return (
                    "High missing rate requires manual review "
                    "before automatic imputation."
                )

            if not is_numeric:
                return (
                    "Automatic multivariate imputation is not "
                    "appropriate for this variable."
                )

            return (
                "Automatic imputation requires manual review."
            )

        return (
            f"Strategy {strategy} selected."
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    @staticmethod
    def _validate_inputs(
        report: dict[str, Any],
        dataframe: pd.DataFrame,
    ) -> None:

        if not isinstance(
            report,
            dict,
        ):
            raise TypeError(
                "report must be a dictionary."
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )
