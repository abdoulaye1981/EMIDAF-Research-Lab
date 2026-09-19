"""
=========================================================
EMIDAF Framework v1.0
Imputation Plan
---------------------------------------------------------
Structures représentant un plan d'imputation par colonne.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class ColumnImputationDecision:
    """
    Décision d'imputation pour une colonne donnée.
    """

    column: str
    strategy: str
    reason: str
    missing_rate: float

    applicable: bool = True
    confidence: float | None = None

    predictors: list[str] = field(
        default_factory=list
    )

    parameters: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(
        self,
    ) -> None:

        # =================================================
        # COLUMN
        # =================================================

        if not isinstance(
            self.column,
            str,
        ):
            raise TypeError(
                "column must be a string."
            )

        self.column = (
            self.column
            .strip()
        )

        if not self.column:
            raise ValueError(
                "column must be a non-empty string."
            )

        # =================================================
        # STRATEGY
        # =================================================

        if not isinstance(
            self.strategy,
            str,
        ):
            raise TypeError(
                "strategy must be a string."
            )

        self.strategy = (
            self.strategy
            .strip()
            .upper()
        )

        allowed_strategies = {
            "NONE",
            "MEAN",
            "MODE",
            "KNN",
            "MICE",
            "REVIEW",
        }

        if (
            self.strategy
            not in allowed_strategies
        ):
            raise ValueError(
                f"Unsupported strategy: "
                f"'{self.strategy}'."
            )

        # =================================================
        # REASON
        # =================================================

        if not isinstance(
            self.reason,
            str,
        ):
            raise TypeError(
                "reason must be a string."
            )

        # =================================================
        # MISSING RATE
        # =================================================

        if not isinstance(
            self.missing_rate,
            (int, float),
        ):
            raise TypeError(
                "missing_rate must be numeric."
            )

        self.missing_rate = float(
            self.missing_rate
        )

        if not (
            0.0
            <= self.missing_rate
            <= 100.0
        ):
            raise ValueError(
                "missing_rate must be between "
                "0 and 100."
            )

        # =================================================
        # APPLICABLE
        # =================================================

        if not isinstance(
            self.applicable,
            bool,
        ):
            raise TypeError(
                "applicable must be a boolean."
            )

        # =================================================
        # CONFIDENCE
        # =================================================

        if self.confidence is not None:

            if not isinstance(
                self.confidence,
                (int, float),
            ):
                raise TypeError(
                    "confidence must be numeric "
                    "or None."
                )

            self.confidence = float(
                self.confidence
            )

            if not (
                0.0
                <= self.confidence
                <= 1.0
            ):
                raise ValueError(
                    "confidence must be between "
                    "0 and 1."
                )

        # =================================================
        # PREDICTORS
        # =================================================

        if not isinstance(
            self.predictors,
            list,
        ):
            raise TypeError(
                "predictors must be a list."
            )

        normalized_predictors: list[str] = []

        for predictor in self.predictors:

            if not isinstance(
                predictor,
                str,
            ):
                raise TypeError(
                    "Each predictor must be a string."
                )

            predictor = (
                predictor
                .strip()
            )

            if not predictor:
                raise ValueError(
                    "Predictor names must not be empty."
                )

            if predictor == self.column:
                raise ValueError(
                    "Target column cannot also be listed "
                    "as a predictor."
                )

            if (
                predictor
                not in normalized_predictors
            ):
                normalized_predictors.append(
                    predictor
                )

        self.predictors = (
            normalized_predictors
        )

        # =================================================
        # PARAMETERS
        # =================================================

        if not isinstance(
            self.parameters,
            dict,
        ):
            raise TypeError(
                "parameters must be a dictionary."
            )


@dataclass(slots=True)
class ImputationPlan:
    """
    Plan d'imputation complet d'un dataset.
    """

    decisions: list[
        ColumnImputationDecision
    ] = field(
        default_factory=list
    )

    source: str = "EMIDAF"
    generated_automatically: bool = True

    # =====================================================
    # ADD
    # =====================================================

    def add(
        self,
        decision: ColumnImputationDecision,
    ) -> None:

        if not isinstance(
            decision,
            ColumnImputationDecision,
        ):
            raise TypeError(
                "decision must be a "
                "ColumnImputationDecision."
            )

        existing_columns = {
            item.column
            for item in self.decisions
        }

        if (
            decision.column
            in existing_columns
        ):
            raise ValueError(
                f"Column '{decision.column}' "
                "already exists in the plan."
            )

        self.decisions.append(
            decision
        )

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        column: str,
    ) -> ColumnImputationDecision | None:

        for decision in self.decisions:

            if (
                decision.column
                == column
            ):
                return decision

        return None

    # =====================================================
    # STRATEGIES
    # =====================================================

    def strategies(
        self,
    ) -> dict[str, str]:

        return {
            decision.column:
            decision.strategy
            for decision
            in self.decisions
        }

    # =====================================================
    # ACTIONABLE
    # =====================================================

    def actionable(
        self,
    ) -> list[
        ColumnImputationDecision
    ]:

        return [
            decision
            for decision
            in self.decisions
            if (
                decision.applicable
                and decision.strategy
                not in {
                    "NONE",
                    "REVIEW",
                }
            )
        ]

    # =====================================================
    # REVIEW REQUIRED
    # =====================================================

    def review_required(
        self,
    ) -> list[
        ColumnImputationDecision
    ]:

        return [
            decision
            for decision
            in self.decisions
            if (
                decision.strategy
                == "REVIEW"
                or not decision.applicable
            )
        ]

    # =====================================================
    # TO DICT
    # =====================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "source":
                self.source,

            "generated_automatically":
                self.generated_automatically,

            "decisions": [
                {
                    "column":
                        decision.column,

                    "strategy":
                        decision.strategy,

                    "reason":
                        decision.reason,

                    "missing_rate":
                        decision.missing_rate,

                    "applicable":
                        decision.applicable,

                    "confidence":
                        decision.confidence,

                    "predictors":
                        list(
                            decision.predictors
                        ),

                    "parameters":
                        dict(
                            decision.parameters
                        ),
                }

                for decision
                in self.decisions
            ],
        }
