"""
=========================================================
EMIDAF Framework v1.0
Imputation Plan Executor
---------------------------------------------------------
Exécution d'un plan d'imputation colonne par colonne.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

import pandas as pd

from emidaf_core.missing.imputation.imputation_plan import (
    ImputationPlan,
)
from emidaf_core.missing.imputation.missing_imputer import (
    MissingImputer,
)


@dataclass(slots=True)
class ColumnExecutionResult:
    """
    Résultat d'exécution pour une colonne.
    """

    column: str
    strategy: str
    success: bool
    values_imputed: int
    message: str
    details: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class PlanExecutionResult:
    """
    Résultat global de l'exécution d'un plan.
    """

    dataframe: pd.DataFrame
    results: list[ColumnExecutionResult]
    success: bool
    total_values_imputed: int
    review_required: list[str]
    errors: list[str]


class ImputationPlanExecutor:
    """
    Exécute un ImputationPlan sur un DataFrame.
    """

    MULTIVARIATE_STRATEGIES = {
        "KNN",
        "MICE",
    }

    def __init__(
        self,
    ) -> None:

        self.imputer = MissingImputer()

    # =====================================================
    # PUBLIC
    # =====================================================

    def execute(
        self,
        dataframe: pd.DataFrame,
        plan: ImputationPlan,
    ) -> PlanExecutionResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        if not isinstance(
            plan,
            ImputationPlan,
        ):
            raise TypeError(
                "plan must be an ImputationPlan."
            )

        working_dataframe = dataframe.copy(
            deep=True
        )

        results: list[
            ColumnExecutionResult
        ] = []

        review_required: list[str] = []
        errors: list[str] = []

        total_values_imputed = 0

        for decision in plan.decisions:

            # =============================================
            # TARGET EXISTS
            # =============================================

            if (
                decision.column
                not in working_dataframe.columns
            ):

                message = (
                    f"Column '{decision.column}' "
                    "does not exist in dataframe."
                )

                errors.append(
                    message
                )

                results.append(
                    ColumnExecutionResult(
                        column=decision.column,
                        strategy=decision.strategy,
                        success=False,
                        values_imputed=0,
                        message=message,
                    )
                )

                continue

            # =============================================
            # PREDICTORS EXIST
            # =============================================

            missing_predictors = [
                predictor
                for predictor
                in decision.predictors
                if (
                    predictor
                    not in working_dataframe.columns
                )
            ]

            if missing_predictors:

                message = (
                    f"{decision.column}: "
                    "unknown predictor(s): "
                    + ", ".join(
                        missing_predictors
                    )
                )

                errors.append(
                    message
                )

                results.append(
                    ColumnExecutionResult(
                        column=decision.column,
                        strategy=decision.strategy,
                        success=False,
                        values_imputed=0,
                        message=message,
                    )
                )

                continue

            # =============================================
            # REVIEW
            # =============================================

            if (
                decision.strategy
                == "REVIEW"
                or not decision.applicable
            ):

                review_required.append(
                    decision.column
                )

            try:

                if (
                    decision.strategy
                    in self.MULTIVARIATE_STRATEGIES
                    and decision.predictors
                ):

                    execution_result = (
                        self._execute_multivariate(
                            dataframe=working_dataframe,
                            column=decision.column,
                            predictors=(
                                decision.predictors
                            ),
                            strategy=(
                                decision.strategy
                            ),
                            parameters=(
                                decision.parameters
                            ),
                        )
                    )

                else:

                    execution_result = (
                        self.imputer.execute(
                            dataframe=working_dataframe,
                            strategy=decision.strategy,
                            columns=[
                                decision.column
                            ],
                            **decision.parameters,
                        )
                    )

                    working_dataframe = (
                        execution_result.dataframe
                    )

                total_values_imputed += (
                    execution_result.values_imputed
                )

                details = dict(
                    execution_result.details
                )

                details["predictors"] = list(
                    decision.predictors
                )

                results.append(
                    ColumnExecutionResult(
                        column=decision.column,
                        strategy=decision.strategy,
                        success=(
                            execution_result.success
                        ),
                        values_imputed=(
                            execution_result.values_imputed
                        ),
                        message=(
                            execution_result.message
                        ),
                        details=details,
                    )
                )

            except (
                TypeError,
                ValueError,
                RuntimeError,
            ) as exc:

                message = (
                    f"{decision.column}: {exc}"
                )

                errors.append(
                    message
                )

                results.append(
                    ColumnExecutionResult(
                        column=decision.column,
                        strategy=decision.strategy,
                        success=False,
                        values_imputed=0,
                        message=str(
                            exc
                        ),
                        details={
                            "predictors":
                                list(
                                    decision.predictors
                                )
                        },
                    )
                )

        return PlanExecutionResult(
            dataframe=working_dataframe,
            results=results,
            success=(
                len(errors) == 0
            ),
            total_values_imputed=(
                total_values_imputed
            ),
            review_required=(
                review_required
            ),
            errors=errors,
        )

    # =====================================================
    # MULTIVARIATE EXECUTION
    # =====================================================

    def _execute_multivariate(
        self,
        dataframe: pd.DataFrame,
        column: str,
        predictors: list[str],
        strategy: str,
        parameters: dict[str, Any],
    ):

        model_columns = [
            column,
            *predictors,
        ]

        temporary_dataframe = (
            dataframe[
                model_columns
            ].copy(
                deep=True
            )
        )

        missing_before = int(
            dataframe[
                column
            ].isna().sum()
        )

        result = self.imputer.execute(
            dataframe=temporary_dataframe,
            strategy=strategy,
            columns=model_columns,
            **parameters,
        )

        # =================================================
        # IMPORTANT :
        # seule la cible est réinjectée.
        # Les predictors restent inchangés dans le
        # DataFrame principal.
        # =================================================

        dataframe.loc[
            :,
            column,
        ] = result.dataframe[
            column
        ]

        missing_after = int(
            dataframe[
                column
            ].isna().sum()
        )

        values_imputed = max(
            0,
            missing_before
            - missing_after,
        )

        result.dataframe = dataframe

        result.columns = [
            column
        ]

        result.values_imputed = (
            values_imputed
        )

        result.details = {
            **result.details,
            "target": column,
            "predictors": list(
                predictors
            ),
            "target_missing_before":
                missing_before,
            "target_missing_after":
                missing_after,
        }

        return result
