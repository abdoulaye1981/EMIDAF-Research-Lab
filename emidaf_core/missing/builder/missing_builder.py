"""
=========================================================
EMIDAF Framework v1.0
Missing Builder
---------------------------------------------------------
Construction du MissingResult à partir du report produit
par MissingAnalyzer.
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_builder import BaseBuilder

from emidaf_core.missing.models.missing_result import MissingResult
from emidaf_core.missing.models.missing_summary import MissingSummary
from emidaf_core.missing.models.missing_statistics import MissingStatistics
from emidaf_core.missing.models.missing_mechanism import MissingMechanism
from emidaf_core.missing.models.missing_strategy import MissingStrategy
from emidaf_core.missing.models.missing_pattern import MissingPattern
from emidaf_core.missing.models.missing_recommendation import (
    MissingRecommendation,
)


class MissingBuilder(BaseBuilder):
    """
    Construit un MissingResult à partir du report produit
    par MissingAnalyzer.

    Cette classe ne réalise aucune analyse statistique.
    Elle transforme et assemble uniquement les résultats.
    """

    def __init__(self) -> None:
        super().__init__()

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        report: dict[str, Any],
    ) -> MissingResult:
        """
        Construit un MissingResult à partir du report.
        """

        if not isinstance(report, dict):
            raise TypeError(
                "report must be a dictionary."
            )

        self.reset()

        summary = self._build_summary(report)
        statistics = self._build_statistics(report)
        mechanism = self._build_mechanism(report)
        strategy = self._build_strategy(report)

        patterns = self._build_patterns(report)
        recommendations = self._build_recommendations(report)

        warnings = list(
            report.get("warnings", [])
        )

        errors = list(
            report.get("errors", [])
        )

        execution_time = float(
            report.get("execution_time", 0.0)
        )

        score = float(
            report.get(
                "quality_score",
                0.0,
            )
        )

        self._result = MissingResult(
            summary=summary,
            statistics=statistics,
            mechanism=mechanism,
            strategy=strategy,
            patterns=patterns,
            recommendations=recommendations,
            warnings=warnings,
            errors=errors,
            execution_time=execution_time,
            score=score,
        )

        return self.finalize()

    # =====================================================
    # SUMMARY
    # =====================================================

    def _build_summary(
        self,
        report: dict[str, Any],
    ) -> MissingSummary:
        """
        Construit MissingSummary.
        """

        summary = report.get(
            "summary",
            {},
        )

        rows = int(
            report.get("rows", 0)
        )

        columns = int(
            report.get("columns", 0)
        )

        cells = int(
            report.get(
                "cells",
                rows * columns,
            )
        )

        total_missing = int(
            report.get(
                "total_missing",
                0,
            )
        )

        missing_rate = float(
            report.get(
                "missing_rate",
                0.0,
            )
        )

        completeness_score = float(
            summary.get(
                "completeness_score",
                max(
                    0.0,
                    100.0 - missing_rate,
                ),
            )
        )

        quality_score = float(
            report.get(
                "quality_score",
                0.0,
            )
        )

        quality_level = str(
            summary.get(
                "quality_level",
                "Unknown",
            )
        )

        return MissingSummary(
            rows=rows,
            columns=columns,
            cells=cells,
            total_missing=total_missing,
            missing_rate=missing_rate,
            completeness_score=completeness_score,
            quality_score=quality_score,
            quality_level=quality_level,
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def _build_statistics(
        self,
        report: dict[str, Any],
    ) -> MissingStatistics:
        """
        Construit MissingStatistics.
        """

        summary = report.get(
            "summary",
            {},
        )

        row_statistics = report.get(
            "row_statistics",
            {},
        )

        return MissingStatistics(
            complete_rows=int(
                row_statistics.get(
                    "complete_rows",
                    0,
                )
            ),
            rows_with_missing=int(
                row_statistics.get(
                    "rows_with_missing",
                    0,
                )
            ),
            empty_rows=int(
                row_statistics.get(
                    "empty_rows",
                    0,
                )
            ),
            complete_columns=int(
                summary.get(
                    "complete_columns",
                    0,
                )
            ),
            partial_columns=int(
                summary.get(
                    "partial_columns",
                    0,
                )
            ),
            empty_columns=int(
                summary.get(
                    "empty_columns",
                    0,
                )
            ),
            missing_density=float(
                summary.get(
                    "missing_density",
                    0.0,
                )
            ),
            pattern_count=int(
                summary.get(
                    "pattern_count",
                    0,
                )
            ),
        )

    # =====================================================
    # MECHANISM
    # =====================================================

    def _build_mechanism(
        self,
        report: dict[str, Any],
    ) -> MissingMechanism:
        """
        Construit MissingMechanism.

        Le Builder ne réalise pas les tests MCAR/MAR/MNAR.
        Il reprend uniquement les informations disponibles.
        """

        mechanism = report.get(
            "missing_mechanism",
            {},
        )

        return MissingMechanism(
            name=str(
                mechanism.get(
                    "candidate",
                    "Unknown",
                )
            ),
            detected=(
                mechanism.get(
                    "status",
                    "Not evaluated",
                )
                != "Not evaluated"
            ),
            confidence=float(
                mechanism.get(
                    "confidence",
                    0.0,
                )
            ),
            pvalue=mechanism.get(
                "pvalue"
            ),
            statistic=mechanism.get(
                "statistic"
            ),
            test_name=str(
                mechanism.get(
                    "test_name",
                    "Not evaluated",
                )
            ),
            explanation=str(
                mechanism.get(
                    "explanation",
                    "Missing mechanism not evaluated.",
                )
            ),
        )

    # =====================================================
    # STRATEGY
    # =====================================================

    def _build_strategy(
        self,
        report: dict[str, Any],
    ) -> MissingStrategy:
        """
        Construit une stratégie globale à partir
        des stratégies recommandées par variable.
        """

        candidates = report.get(
            "imputation_candidates",
            [],
        )

        if not candidates:
            return MissingStrategy(
                strategy="NONE",
                confidence=1.0,
                applicable=True,
                reason="No imputation candidate available.",
            )

        hierarchy = {
            "NONE": 0,
            "MEAN": 1,
            "MODE": 1,
            "KNN": 2,
            "MICE": 3,
            "REVIEW": 4,
        }

        selected = max(
            candidates,
            key=lambda item: hierarchy.get(
                self._normalize_strategy(
                    item.get(
                        "recommended_strategy",
                        "REVIEW",
                    )
                ),
                4,
            ),
        )

        strategy = self._normalize_strategy(
            selected.get(
                "recommended_strategy",
                "REVIEW",
            )
        )

        column = selected.get(
            "column",
            "unknown",
        )

        applicable = strategy not in {
            "REVIEW",
        }

        if strategy == "NONE":
            reason = (
                "No imputation is required."
            )
        elif strategy == "REVIEW":
            reason = (
                f"Expert review required for variable "
                f"'{column}'."
            )
        else:
            reason = (
                f"Global strategy selected from the "
                f"most demanding variable: '{column}'."
            )

        confidence = self._strategy_confidence(
            candidates,
            strategy,
        )

        return MissingStrategy(
            strategy=strategy,
            confidence=confidence,
            applicable=applicable,
            reason=reason,
        )

    # =====================================================
    # PATTERNS
    # =====================================================

    def _build_patterns(
        self,
        report: dict[str, Any],
    ) -> list[MissingPattern]:
        """
        Construit les MissingPattern.
        """

        patterns = report.get(
            "patterns",
            [],
        )

        return [
            MissingPattern(
                pattern=list(
                    item.get(
                        "pattern",
                        [],
                    )
                ),
                count=int(
                    item.get(
                        "count",
                        0,
                    )
                ),
                percentage=float(
                    item.get(
                        "percentage",
                        0.0,
                    )
                ),
            )
            for item in patterns
            if isinstance(item, dict)
        ]

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _build_recommendations(
        self,
        report: dict[str, Any],
    ) -> list[MissingRecommendation]:
        """
        Convertit les recommandations textuelles
        en MissingRecommendation.
        """

        recommendations = report.get(
            "recommendations",
            [],
        )

        return [
            self._recommendation_from_message(
                str(message)
            )
            for message in recommendations
        ]

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def _normalize_strategy(
        strategy: str,
    ) -> str:
        """
        Normalise le nom d'une stratégie.
        """

        value = str(
            strategy
        ).strip()

        mapping = {
            "None": "NONE",
            "Mean": "MEAN",
            "Mode": "MODE",
            "KNN": "KNN",
            "MICE": "MICE",
            "Review Variable": "REVIEW",
        }

        return mapping.get(
            value,
            value.upper(),
        )

    @staticmethod
    def _strategy_confidence(
        candidates: list[dict[str, Any]],
        strategy: str,
    ) -> float:
        """
        Calcule une confiance simple basée
        sur la proportion de variables utilisant
        la stratégie sélectionnée.
        """

        if not candidates:
            return 1.0

        matching = sum(
            1
            for item in candidates
            if MissingBuilder._normalize_strategy(
                item.get(
                    "recommended_strategy",
                    "",
                )
            ) == strategy
        )

        return round(
            matching / len(candidates),
            2,
        )

    @staticmethod
    def _recommendation_from_message(
        message: str,
    ) -> MissingRecommendation:
        """
        Détermine la criticité d'une recommandation
        sans modifier son message.
        """

        text = message.lower()

        if (
            "entièrement vide" in text
            or "nettoyage approfondi" in text
        ):
            severity = "critical"
            priority = 0

        elif (
            "identifier le mécanisme" in text
            or "imputation adaptée" in text
            or "plus de 20%" in text
        ):
            severity = "high"
            priority = 1

        elif (
            "aucune valeur manquante" in text
        ):
            severity = "info"
            priority = 3

        else:
            severity = "medium"
            priority = 2

        return MissingRecommendation(
            severity=severity,
            message=message,
            priority=priority,
        )
