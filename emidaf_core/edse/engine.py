"""
=========================================================
EMIDAF Framework
EDSE - Decision Support Engine
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .assessment import DecisionAssessment
from .profiles import DecisionProfiles
from .scenarios import DecisionScenarios
from .interpretation import DecisionInterpreter


class EDSEEngine:
    """
    Moteur d'aide à la décision.

    EDSE ne prend jamais automatiquement une décision.
    Il évalue des scénarios définis explicitement.
    """

    def __init__(
        self,
        estimator: Any,
        X: pd.DataFrame,
        *,
        task: str,
        cv_mean: float | None = None,
        test_score: float | None = None,
        better_than_baseline: bool | None = None,
    ):

        if task not in {
            "classification",
            "regression",
        }:
            raise ValueError(
                "task doit être 'classification' "
                "ou 'regression'."
            )

        self.estimator = estimator
        self.X = X.copy()
        self.task = task

        self.cv_mean = cv_mean
        self.test_score = test_score
        self.better_than_baseline = (
            better_than_baseline
        )

        self.predictions_ = None
        self.probabilities_ = None

    def predict(self):

        self.predictions_ = (
            self.estimator.predict(
                self.X
            )
        )

        if (
            self.task == "classification"
            and hasattr(
                self.estimator,
                "predict_proba",
            )
        ):

            probabilities = (
                self.estimator.predict_proba(
                    self.X
                )
            )

            if probabilities.ndim == 2:

                if probabilities.shape[1] == 2:
                    self.probabilities_ = (
                        probabilities[:, 1]
                    )

        return self.predictions_

    def assessment(self) -> dict:

        return DecisionAssessment.assess(
            task=self.task,
            cv_mean=self.cv_mean,
            test_score=self.test_score,
            better_than_baseline=(
                self.better_than_baseline
            ),
        )

    def profiles(self) -> pd.DataFrame:

        if self.predictions_ is None:
            self.predict()

        if (
            self.task == "classification"
            and self.probabilities_ is not None
        ):

            return (
                DecisionProfiles
                .classification(
                    self.X,
                    self.probabilities_,
                    self.predictions_,
                )
            )

        return DecisionProfiles.regression(
            self.X,
            self.predictions_,
        )

    def scenario(
        self,
        *,
        threshold: float,
        direction: str = "above",
    ) -> dict:

        if self.predictions_ is None:
            self.predict()

        if self.task == "classification":

            if self.probabilities_ is None:

                raise RuntimeError(
                    "Le modèle ne fournit pas "
                    "de probabilités exploitables "
                    "pour ce scénario."
                )

            table = (
                DecisionScenarios
                .classification(
                    self.probabilities_,
                    threshold=threshold,
                )
            )

            summary = (
                DecisionScenarios
                .summarize(
                    table
                )
            )

            interpretation = (
                DecisionInterpreter
                .scenario(
                    summary,
                    threshold=threshold,
                    task="classification",
                )
            )

        else:

            table = (
                DecisionScenarios
                .regression(
                    self.predictions_,
                    threshold=threshold,
                    direction=direction,
                )
            )

            summary = (
                DecisionScenarios
                .summarize(
                    table
                )
            )

            interpretation = (
                DecisionInterpreter
                .scenario(
                    summary,
                    threshold=threshold,
                    task="regression",
                    direction=direction,
                )
            )

        return {
            "table": table,
            "summary": summary,
            "interpretation": interpretation,
        }

    def summary(self) -> dict:

        assessment = self.assessment()

        return {
            "task": self.task,
            "observations": len(self.X),
            "cv_mean": self.cv_mean,
            "test_score": self.test_score,
            "assessment": assessment,
            "interpretation": (
                DecisionInterpreter
                .reliability(
                    assessment
                )
            ),
        }


class EDSE(EDSEEngine):
    pass
