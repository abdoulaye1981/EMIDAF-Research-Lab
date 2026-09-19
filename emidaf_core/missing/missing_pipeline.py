"""
=========================================================
EMIDAF Framework v1.0
Missing Data Pipeline
---------------------------------------------------------
Façade de haut niveau pour l'analyse, la planification
et le traitement des valeurs manquantes.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from emidaf_core.dataset.profiler.analyzers.missing_analyzer import (
    MissingAnalyzer,
)
from emidaf_core.dataset.profiler.profile_context import (
    ProfileContext,
)
from emidaf_core.missing.imputation.imputation_plan import (
    ImputationPlan,
)
from emidaf_core.missing.imputation.plan_builder import (
    ImputationPlanBuilder,
)
from emidaf_core.missing.imputation.plan_executor import (
    ImputationPlanExecutor,
)


@dataclass(slots=True)
class MissingPipelineResult:
    """
    Résultat global et auditable du pipeline
    de traitement des valeurs manquantes.
    """

    dataframe: pd.DataFrame
    report: dict[str, Any]
    plan: ImputationPlan
    execution: Any | None
    analysis_result: Any
    applied: bool
    success: bool
    initial_missing_values: int = 0

    # =====================================================
    # BASIC METRICS
    # =====================================================

    @property
    def total_values_imputed(
        self,
    ) -> int:
        """
        Nombre total de valeurs effectivement imputées.
        """

        if self.execution is None:
            return 0

        return int(
            getattr(
                self.execution,
                "total_values_imputed",
                0,
            )
        )

    @property
    def final_missing_values(
        self,
    ) -> int:
        """
        Nombre de valeurs manquantes restantes
        après le pipeline.
        """

        return int(
            self.dataframe
            .isna()
            .sum()
            .sum()
        )

    @property
    def missing_values_reduction(
        self,
    ) -> int:
        """
        Réduction du nombre total de valeurs manquantes.
        """

        return (
            self.initial_missing_values
            - self.final_missing_values
        )

    @property
    def review_required(
        self,
    ) -> list[str]:
        """
        Variables nécessitant une revue manuelle.
        """

        if self.execution is not None:

            value = getattr(
                self.execution,
                "review_required",
                [],
            )

            return list(
                value
            )

        review_decisions = getattr(
            self.plan,
            "review_required",
            [],
        )

        if callable(
            review_decisions
        ):
            review_decisions = (
                review_decisions()
            )

        return [
            decision.column
            for decision
            in review_decisions
        ]

    # =====================================================
    # STRATEGIES
    # =====================================================

    @property
    def strategies(
        self,
    ) -> dict[str, str]:
        """
        Stratégie retenue pour chaque variable
        présente dans le plan.
        """

        value = getattr(
            self.plan,
            "strategies",
            {},
        )

        if callable(
            value
        ):
            value = value()

        if isinstance(
            value,
            dict,
        ):
            return dict(
                value
            )

        decisions = getattr(
            self.plan,
            "decisions",
            [],
        )

        return {
            decision.column:
                decision.strategy
            for decision
            in decisions
        }

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Retourne une synthèse compacte du pipeline.
        """

        rows, columns = (
            self.dataframe.shape
        )

        return {
            "success":
                self.success,

            "imputation_applied":
                self.applied,

            "rows":
                int(rows),

            "columns":
                int(columns),

            "initial_missing_values":
                int(
                    self.initial_missing_values
                ),

            "final_missing_values":
                int(
                    self.final_missing_values
                ),

            "missing_values_reduction":
                int(
                    self.missing_values_reduction
                ),

            "total_values_imputed":
                int(
                    self.total_values_imputed
                ),

            "review_required":
                self.review_required,

            "strategies":
                self.strategies,
        }

    # =====================================================
    # SUMMARY DATAFRAME
    # =====================================================

    def summary_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Retourne une vue tabulaire du plan d'imputation.

        Une ligne est produite pour chaque variable
        présente dans le plan.

        Colonnes
        --------
        column:
            Nom de la variable.

        missing_rate:
            Pourcentage de valeurs manquantes.

        strategy:
            Stratégie d'imputation retenue.

        predictors:
            Variables auxiliaires utilisées par KNN/MICE.

        applicable:
            Indique si la stratégie peut être exécutée
            automatiquement.

        review_required:
            Indique si une intervention humaine est requise.

        parameters:
            Paramètres utilisés par la stratégie.
        """

        decisions = getattr(
            self.plan,
            "decisions",
            [],
        )

        rows: list[
            dict[str, Any]
        ] = []

        review_columns = set(
            self.review_required
        )

        for decision in decisions:

            predictors = list(
                getattr(
                    decision,
                    "predictors",
                    [],
                )
            )

            parameters = dict(
                getattr(
                    decision,
                    "parameters",
                    {},
                )
            )

            column = getattr(
                decision,
                "column",
                "",
            )

            strategy = getattr(
                decision,
                "strategy",
                "",
            )

            missing_rate = float(
                getattr(
                    decision,
                    "missing_rate",
                    0.0,
                )
            )

            applicable = bool(
                getattr(
                    decision,
                    "applicable",
                    True,
                )
            )

            rows.append(
                {
                    "column":
                        column,

                    "missing_rate":
                        missing_rate,

                    "strategy":
                        strategy,

                    "predictors":
                        predictors,

                    "applicable":
                        applicable,

                    "review_required":
                        column
                        in review_columns,

                    "parameters":
                        parameters,
                }
            )

        return pd.DataFrame(
            rows,
            columns=[
                "column",
                "missing_rate",
                "strategy",
                "predictors",
                "applicable",
                "review_required",
                "parameters",
            ],
        )

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Sérialise le résultat du pipeline sous une forme
        exploitable par une API, une CLI ou un rapport.

        Le DataFrame complet n'est volontairement pas
        inclus afin d'éviter une sérialisation massive.
        """

        plan_to_dict = getattr(
            self.plan,
            "to_dict",
            None,
        )

        if callable(
            plan_to_dict
        ):
            plan_data = (
                plan_to_dict()
            )
        else:
            plan_data = {
                "strategies":
                    self.strategies
            }

        return {
            "summary":
                self.summary(),

            "report":
                self.report,

            "plan":
                plan_data,
        }


class MissingPipeline:
    """
    Pipeline haut niveau pour l'analyse et
    l'imputation des valeurs manquantes.

    Architecture
    ------------
    MissingAnalyzer
        ->
    ImputationPlanBuilder
        ->
    ImputationPlanExecutor
    """

    def __init__(
        self,
        analyzer: MissingAnalyzer | None = None,
        plan_builder: ImputationPlanBuilder | None = None,
        plan_executor: ImputationPlanExecutor | None = None,
    ) -> None:

        self.analyzer = (
            analyzer
            if analyzer is not None
            else MissingAnalyzer()
        )

        self.plan_builder = (
            plan_builder
            if plan_builder is not None
            else ImputationPlanBuilder()
        )

        self.plan_executor = (
            plan_executor
            if plan_executor is not None
            else ImputationPlanExecutor()
        )

    # =====================================================
    # PUBLIC API
    # =====================================================

    def run(
        self,
        dataframe: pd.DataFrame,
        apply_imputation: bool = True,
        copy_input: bool = True,
    ) -> MissingPipelineResult:
        """
        Exécute le pipeline complet.
        """

        self._validate_inputs(
            dataframe=dataframe,
            apply_imputation=apply_imputation,
            copy_input=copy_input,
        )

        initial_missing_values = int(
            dataframe
            .isna()
            .sum()
            .sum()
        )

        working_dataframe = (
            dataframe.copy(
                deep=True
            )
            if copy_input
            else dataframe
        )

        # =================================================
        # STEP 1 — ANALYSIS
        # =================================================

        context = ProfileContext(
            dataframe=working_dataframe
        )

        analysis_result = (
            self.analyzer.execute(
                context
            )
        )

        report = getattr(
            analysis_result,
            "result",
            None,
        )

        if not isinstance(
            report,
            dict,
        ):
            raise TypeError(
                "MissingAnalyzer.execute() must return "
                "an object containing a dictionary "
                "in its 'result' attribute."
            )

        # =================================================
        # STEP 2 — PLAN
        # =================================================

        plan = (
            self.plan_builder.build(
                report=report,
                dataframe=working_dataframe,
            )
        )

        # =================================================
        # STEP 3 — ANALYSIS ONLY
        # =================================================

        if not apply_imputation:

            return MissingPipelineResult(
                dataframe=
                    working_dataframe,

                report=
                    report,

                plan=
                    plan,

                execution=
                    None,

                analysis_result=
                    analysis_result,

                applied=
                    False,

                success=
                    True,

                initial_missing_values=
                    initial_missing_values,
            )

        # =================================================
        # STEP 4 — EXECUTION
        # =================================================

        execution = (
            self.plan_executor.execute(
                dataframe=
                    working_dataframe,

                plan=
                    plan,
            )
        )

        final_dataframe = getattr(
            execution,
            "dataframe",
            None,
        )

        if not isinstance(
            final_dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "ImputationPlanExecutor.execute() must "
                "return an object containing a pandas "
                "DataFrame in its 'dataframe' attribute."
            )

        execution_success = bool(
            getattr(
                execution,
                "success",
                True,
            )
        )

        return MissingPipelineResult(
            dataframe=
                final_dataframe,

            report=
                report,

            plan=
                plan,

            execution=
                execution,

            analysis_result=
                analysis_result,

            applied=
                True,

            success=
                execution_success,

            initial_missing_values=
                initial_missing_values,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    @staticmethod
    def _validate_inputs(
        dataframe: pd.DataFrame,
        apply_imputation: bool,
        copy_input: bool,
    ) -> None:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        if not isinstance(
            apply_imputation,
            bool,
        ):
            raise TypeError(
                "apply_imputation must be a boolean."
            )

        if not isinstance(
            copy_input,
            bool,
        ):
            raise TypeError(
                "copy_input must be a boolean."
            )
