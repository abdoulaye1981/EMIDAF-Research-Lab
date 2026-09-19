"""
=========================================================
EMIDAF Framework v1.0
MNAR Analyzer
---------------------------------------------------------
Évaluation prudente du risque de mécanisme MNAR.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass(slots=True)
class MNARVariableResult:
    """
    Résultat MNAR pour une variable.
    """

    variable: str

    missing_rate: float

    risk_level: str

    suspicion_score: float

    sensitivity_required: bool

    reasons: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class MNARResult:
    """
    Résultat global de l'analyse MNAR.

    Important :
        MNAR n'est pas directement identifiable
        à partir des seules données observées.
    """

    executed: bool

    evidence_level: str

    sensitivity_required: bool

    variables_analyzed: int

    variables_at_risk: int

    results: list[MNARVariableResult]

    message: str


class MNARAnalyzer:
    """
    Analyse exploratoire du risque MNAR.

    Cette classe ne prétend pas prouver qu'un mécanisme
    est MNAR.

    Elle identifie des situations dans lesquelles
    une analyse de sensibilité ou une expertise métier
    est nécessaire.
    """

    def run(
        self,
        dataframe: pd.DataFrame,
        mar_evidence: dict[str, bool] | None = None,
        high_missing_rate: float = 40.0,
    ) -> MNARResult:
        """
        Évalue le risque potentiel de MNAR.
        """

        # =====================================================
        # VALIDATION
        # =====================================================

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        if not 0 < high_missing_rate <= 100:
            raise ValueError(
                "high_missing_rate must be between "
                "0 and 100."
            )

        if (
            mar_evidence is not None
            and not isinstance(
                mar_evidence,
                dict,
            )
        ):
            raise TypeError(
                "mar_evidence must be a dictionary "
                "or None."
            )

        # =====================================================
        # EMPTY DATAFRAME
        # =====================================================

        if dataframe.empty:
            return MNARResult(
                executed=False,
                evidence_level="not_evaluated",
                sensitivity_required=False,
                variables_analyzed=0,
                variables_at_risk=0,
                results=[],
                message="The dataframe is empty.",
            )

        # =====================================================
        # MISSING VARIABLES
        # =====================================================

        missing_columns = [
            column
            for column in dataframe.columns
            if dataframe[column].isna().any()
        ]

        if not missing_columns:
            return MNARResult(
                executed=False,
                evidence_level="not_required",
                sensitivity_required=False,
                variables_analyzed=0,
                variables_at_risk=0,
                results=[],
                message=(
                    "No missing values detected. "
                    "MNAR assessment is not required."
                ),
            )

        variable_results = []

        # =====================================================
        # VARIABLE ANALYSIS
        # =====================================================

        for column in missing_columns:

            missing_rate = round(
                100.0
                * dataframe[column].isna().mean(),
                2,
            )

            reasons = []

            score = 0.0

            # -------------------------------------------------
            # SIGNAL 1
            # High missingness
            # -------------------------------------------------

            if missing_rate >= high_missing_rate:

                score += 0.4

                reasons.append(
                    "High missing-data rate."
                )

            elif missing_rate >= 20:

                score += 0.2

                reasons.append(
                    "Moderate missing-data rate."
                )

            # -------------------------------------------------
            # SIGNAL 2
            # Absence of observed MAR evidence
            # -------------------------------------------------

            if mar_evidence is not None:

                evidence = mar_evidence.get(
                    column
                )

                if evidence is False:

                    score += 0.4

                    reasons.append(
                        "No observed-variable MAR "
                        "association was detected."
                    )

                elif evidence is True:

                    reasons.append(
                        "Observed-variable associations "
                        "support a possible MAR mechanism."
                    )

            else:

                score += 0.1

                reasons.append(
                    "MAR evidence was not supplied."
                )

            # -------------------------------------------------
            # SIGNAL 3
            # Entirely missing variable
            # -------------------------------------------------

            if dataframe[column].isna().all():

                score = max(
                    score,
                    0.8,
                )

                reasons.append(
                    "The variable is entirely missing."
                )

            # =================================================
            # SCORE
            # =================================================

            score = round(
                min(
                    score,
                    1.0,
                ),
                2,
            )

            if score >= 0.7:

                risk_level = "high"

            elif score >= 0.4:

                risk_level = "moderate"

            else:

                risk_level = "low"

            sensitivity_required = (
                risk_level
                in {
                    "moderate",
                    "high",
                }
            )

            variable_results.append(
                MNARVariableResult(
                    variable=column,
                    missing_rate=missing_rate,
                    risk_level=risk_level,
                    suspicion_score=score,
                    sensitivity_required=(
                        sensitivity_required
                    ),
                    reasons=reasons,
                )
            )

        # =====================================================
        # GLOBAL RESULT
        # =====================================================

        variables_at_risk = sum(
            1
            for result in variable_results
            if result.risk_level
            in {
                "moderate",
                "high",
            }
        )

        if any(
            result.risk_level == "high"
            for result in variable_results
        ):

            evidence_level = "high_risk"

        elif variables_at_risk > 0:

            evidence_level = "possible"

        else:

            evidence_level = "low_risk"

        sensitivity_required = (
            variables_at_risk > 0
        )

        if sensitivity_required:

            message = (
                "Potential MNAR risk detected. "
                "MNAR cannot be confirmed from observed "
                "data alone. Sensitivity analysis and "
                "domain expertise are recommended."
            )

        else:

            message = (
                "No strong MNAR risk signal was detected. "
                "However, MNAR cannot be ruled out using "
                "observed data alone."
            )

        return MNARResult(
            executed=True,
            evidence_level=evidence_level,
            sensitivity_required=(
                sensitivity_required
            ),
            variables_analyzed=len(
                variable_results
            ),
            variables_at_risk=variables_at_risk,
            results=variable_results,
            message=message,
        )
