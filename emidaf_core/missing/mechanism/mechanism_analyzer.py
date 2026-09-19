"""
=========================================================
EMIDAF Framework v1.0
Missing Mechanism Analyzer
---------------------------------------------------------
Orchestration des analyses MCAR / MAR / MNAR.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from emidaf_core.missing.mechanism.little_mcar_test import (
    LittleMCARTest,
)
from emidaf_core.missing.mechanism.mar_analyzer import (
    MARAnalyzer,
)
from emidaf_core.missing.mechanism.mnar_analyzer import (
    MNARAnalyzer,
)


class MechanismAnalyzer:
    """
    Orchestre l'évaluation du mécanisme des valeurs
    manquantes.

    Ordre de décision :

    1. Little MCAR Test
    2. Analyse MAR si MCAR est rejeté ou non évaluable
    3. Évaluation du risque MNAR si nécessaire

    Important :
        MAR et MNAR ne sont pas considérés comme
        "prouvés" à partir des seules données observées.
    """

    def __init__(self) -> None:

        self._mcar_test = LittleMCARTest()

        self._mar_analyzer = MARAnalyzer()

        self._mnar_analyzer = MNARAnalyzer()

    # =====================================================
    # PUBLIC
    # =====================================================

    def analyze(
        self,
        dataframe: pd.DataFrame,
        alpha: float = 0.05,
    ) -> dict[str, Any]:
        """
        Analyse le mécanisme potentiel des valeurs
        manquantes.
        """

        # =================================================
        # VALIDATION
        # =================================================

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha must be between 0 and 1."
            )

        # =================================================
        # EMPTY DATAFRAME
        # =================================================

        if dataframe.empty:

            return self._not_evaluated_result(
                status="Not evaluated",
                candidate="Unknown",
                explanation=(
                    "The dataframe is empty. "
                    "The missing-data mechanism cannot "
                    "be evaluated."
                ),
            )

        # =================================================
        # NO MISSING VALUES
        # =================================================

        if not dataframe.isna().any().any():

            return {
                "status": "Not required",
                "candidate": "None",
                "detected": False,
                "confidence": 1.0,
                "pvalue": None,
                "statistic": None,
                "test_name": "Not required",
                "explanation": (
                    "No missing values were detected. "
                    "Mechanism analysis is not required."
                ),
                "tests": {
                    "mcar": {
                        "name": "Little MCAR Test",
                        "available": True,
                        "executed": False,
                    },
                    "mar": {
                        "name": "MAR Statistical Analysis",
                        "available": True,
                        "executed": False,
                    },
                    "mnar": {
                        "name": "MNAR Risk Assessment",
                        "available": True,
                        "executed": False,
                    },
                },
            }

        # =================================================
        # MCAR
        # =================================================

        mcar_result = self._mcar_test.run(
            dataframe=dataframe,
            alpha=alpha,
        )

        mcar_details = {
            "name": "Little MCAR Test",
            "available": True,
            "executed": mcar_result.executed,
            "statistic": mcar_result.statistic,
            "pvalue": mcar_result.pvalue,
            "degrees_of_freedom": (
                mcar_result.degrees_of_freedom
            ),
            "compatible_with_mcar": (
                mcar_result.is_mcar
            ),
            "message": mcar_result.message,
        }

        # -------------------------------------------------
        # MCAR COMPATIBLE
        # -------------------------------------------------

        if (
            mcar_result.executed
            and mcar_result.is_mcar is True
        ):

            confidence = self._mcar_confidence(
                pvalue=mcar_result.pvalue,
                alpha=alpha,
            )

            return {
                "status": "Compatible",
                "candidate": "MCAR",
                "detected": False,
                "confidence": confidence,
                "pvalue": mcar_result.pvalue,
                "statistic": mcar_result.statistic,
                "test_name": "Little MCAR Test",
                "explanation": (
                     "Little's MCAR test did not reject the null "
                     "hypothesis. The observed data are compatible "
                     "with an MCAR mechanism. This result does not "
                     "prove MCAR, and MAR or MNAR mechanisms cannot "
                     "be excluded from observed data alone."
                ),
                "tests": {
                    "mcar": mcar_details,
                    "mar": {
                        "name": "MAR Statistical Analysis",
                        "available": True,
                        "executed": False,
                    },
                    "mnar": {
                        "name": "MNAR Risk Assessment",
                        "available": True,
                        "executed": False,
                    },
                },
            }

        # =================================================
        # MAR
        # =================================================

        mar_result = self._mar_analyzer.run(
            dataframe=dataframe,
            alpha=alpha,
        )

        mar_evidence = {
            item.variable: item.evidence_detected
            for item in mar_result.results
        }

        mar_details = {
            "name": "MAR Statistical Analysis",
            "available": True,
            "executed": mar_result.executed,
            "evidence_detected": (
                mar_result.evidence_detected
            ),
            "variables_tested": (
                mar_result.variables_tested
            ),
            "variables_with_evidence": (
                mar_result.variables_with_evidence
            ),
            "message": mar_result.message,
        }

        # -------------------------------------------------
        # MAR EVIDENCE
        # -------------------------------------------------

        if (
            mar_result.executed
            and mar_result.evidence_detected is True
        ):

            confidence = self._mar_confidence(
                variables_tested=(
                    mar_result.variables_tested
                ),
                variables_with_evidence=(
                    mar_result.variables_with_evidence
                ),
            )

            return {
                "status": "Evaluated",
                "candidate": "MAR",
                "detected": True,
                "confidence": confidence,
                "pvalue": mcar_result.pvalue,
                "statistic": mcar_result.statistic,
                "test_name": (
                    "Observed missingness association "
                    "analysis"
                ),
                "explanation": (
                    "Missingness is associated with one "
                    "or more observed variables. This "
                    "provides evidence compatible with "
                    "a MAR mechanism, but does not prove "
                    "that the mechanism is MAR."
                ),
                "tests": {
                    "mcar": mcar_details,
                    "mar": mar_details,
                    "mnar": {
                        "name": "MNAR Risk Assessment",
                        "available": True,
                        "executed": False,
                    },
                },
            }

        # =================================================
        # MNAR RISK
        # =================================================

        mnar_result = self._mnar_analyzer.run(
            dataframe=dataframe,
            mar_evidence=mar_evidence,
        )

        mnar_details = {
            "name": "MNAR Risk Assessment",
            "available": True,
            "executed": mnar_result.executed,
            "evidence_level": (
                mnar_result.evidence_level
            ),
            "sensitivity_required": (
                mnar_result.sensitivity_required
            ),
            "variables_analyzed": (
                mnar_result.variables_analyzed
            ),
            "variables_at_risk": (
                mnar_result.variables_at_risk
            ),
            "message": mnar_result.message,
        }

        # -------------------------------------------------
        # POSSIBLE MNAR
        # -------------------------------------------------

        if (
            mnar_result.executed
            and mnar_result.sensitivity_required
        ):

            confidence = self._mnar_risk_score(
                mnar_result.results
            )

            return {
                "status": "Requires review",
                "candidate": "MNAR possible",
                "detected": False,
                "confidence": confidence,
                "pvalue": mcar_result.pvalue,
                "statistic": mcar_result.statistic,
                "test_name": (
                    "MNAR Risk Assessment"
                ),
                "explanation": (
                    "MCAR was not supported and no "
                    "sufficient observed-variable MAR "
                    "evidence was detected. MNAR is "
                    "possible, but cannot be confirmed "
                    "from observed data alone. "
                    "Sensitivity analysis and domain "
                    "expertise are required."
                ),
                "tests": {
                    "mcar": mcar_details,
                    "mar": mar_details,
                    "mnar": mnar_details,
                },
            }

        # =================================================
        # INCONCLUSIVE
        # =================================================

        return {
            "status": "Inconclusive",
            "candidate": "Unknown",
            "detected": False,
            "confidence": 0.0,
            "pvalue": mcar_result.pvalue,
            "statistic": mcar_result.statistic,
            "test_name": (
                "Missing Mechanism Analysis"
            ),
            "explanation": (
                "The available evidence is insufficient "
                "to identify a plausible missing-data "
                "mechanism."
            ),
            "tests": {
                "mcar": mcar_details,
                "mar": mar_details,
                "mnar": mnar_details,
            },
        }

    # =====================================================
    # CONFIDENCE HELPERS
    # =====================================================

    @staticmethod
    def _mcar_confidence(
        pvalue: float | None,
        alpha: float,
    ) -> float:
        """
        Heuristic support score for MCAR compatibility.

        This value is not a statistical probability
        that the mechanism is MCAR.
        """

        if pvalue is None:
            return 0.0

        if pvalue <= alpha:
            return 0.0

        score = (
            pvalue - alpha
        ) / (
            1.0 - alpha
        )

        return round(
            min(
                max(
                    score,
                    0.0,
                ),
                1.0,
            ),
            2,
        )

    @staticmethod
    def _mar_confidence(
        variables_tested: int,
        variables_with_evidence: int,
    ) -> float:
        """
        Heuristic proportion of missing variables
        showing observed-variable associations.
        """

        if variables_tested <= 0:
            return 0.0

        return round(
            variables_with_evidence
            / variables_tested,
            2,
        )

    @staticmethod
    def _mnar_risk_score(
        results,
    ) -> float:
        """
        Returns the highest heuristic MNAR suspicion
        score across analyzed variables.
        """

        if not results:
            return 0.0

        return round(
            max(
                item.suspicion_score
                for item in results
            ),
            2,
        )

    # =====================================================
    # DEFAULT RESULT
    # =====================================================

    @staticmethod
    def _not_evaluated_result(
        status: str,
        candidate: str,
        explanation: str,
    ) -> dict[str, Any]:

        return {
            "status": status,
            "candidate": candidate,
            "detected": False,
            "confidence": 0.0,
            "pvalue": None,
            "statistic": None,
            "test_name": "Not evaluated",
            "explanation": explanation,
            "tests": {
                "mcar": {
                    "name": "Little MCAR Test",
                    "available": True,
                    "executed": False,
                },
                "mar": {
                    "name": "MAR Statistical Analysis",
                    "available": True,
                    "executed": False,
                },
                "mnar": {
                    "name": "MNAR Risk Assessment",
                    "available": True,
                    "executed": False,
                },
            },
        }
