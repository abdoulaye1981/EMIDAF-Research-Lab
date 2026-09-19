"""
=========================================================
EMIDAF Framework v1.0
Cardinality Analyzer
---------------------------------------------------------
Analyse de la cardinalité des variables.
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext
from ....common.enums.data_quality import DataQuality


class CardinalityAnalyzer(BaseAnalyzer):

    name = "CardinalityAnalyzer"
    version = "1.0.0"
    description = "Cardinality Analysis"

    LOW_CARDINALITY = 10
    HIGH_CARDINALITY = 100

    ID_THRESHOLD = 0.95

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe
        rows = context.rows

        report = {
            "column_statistics": {},
            "summary": {},
            "quality_score": 100.0,
            "warnings": [],
            "recommendations": []
        }

        constant_columns = []
        quasi_constant_columns = []
        low_cardinality_columns = []
        high_cardinality_columns = []
        id_columns = []

        for column in dataframe.columns:

            series = dataframe[column]

            unique = int(
                dataframe[column].nunique(
                    dropna=True
                )
            )

            unique_percentage = (
                round(
                    100 * unique / rows,
                    2
                )
                if rows > 0
                else 0.0
            )

            constant = unique <= 1

            quasi_constant = (
                unique <= 2
                and unique > 1
            )

            low_cardinality = (
                unique <= self.LOW_CARDINALITY
                and not constant
            )

            high_cardinality = (
                unique >= self.HIGH_CARDINALITY
            )

            id_like = (
                rows >= 20
                and unique_percentage >= self.ID_THRESHOLD * 100
                and unique >= 20
            )

            report["column_statistics"][column] = {
                "unique": unique,
                "unique_percentage": unique_percentage,
                "constant": constant,
                "quasi_constant": quasi_constant,
                "low_cardinality": low_cardinality,
                "high_cardinality": high_cardinality,
                "id_like": id_like
            }

            if constant:
                constant_columns.append(column)

            if quasi_constant:
                quasi_constant_columns.append(column)

            if low_cardinality:
                low_cardinality_columns.append(column)

            if high_cardinality:
                high_cardinality_columns.append(column)

            if id_like:
                id_columns.append(column)

        # =====================================================
        # RÉSUMÉ GLOBAL
        # =====================================================

        report["summary"] = {
            "columns": list(dataframe.columns),
            "column_count": len(dataframe.columns),

            "constant_columns": len(
                constant_columns
            ),
            "constant_column_names": constant_columns,

            "quasi_constant_columns": len(
                quasi_constant_columns
            ),
            "quasi_constant_column_names": quasi_constant_columns,

            "low_cardinality_columns": len(
                low_cardinality_columns
            ),
            "low_cardinality_column_names": low_cardinality_columns,

            "high_cardinality_columns": len(
                high_cardinality_columns
            ),
            "high_cardinality_column_names": high_cardinality_columns,

            "id_columns": len(
                id_columns
            ),
            "id_column_names": id_columns
        }

        self._compute_quality(report)

        self._build_recommendations(report)

        context.add_result(
            self.name,
            report
        )

        context.put_cache(
            self.name,
            report
        )

        return report
    def _compute_quality(
        self,
        report: dict[str, Any]
    ) -> None:

        summary = report["summary"]

        score = 100.0

        score -= (
            summary["constant_columns"] * 10
        )

        score -= (
            summary["quasi_constant_columns"] * 5
        )

        score = max(
            0.0,
            score
        )

        report["quality_score"] = round(
            score,
            2
        )

        if score >= 90:
            level = DataQuality.EXCELLENT.value

        elif score >= 75:
            level = DataQuality.VERY_GOOD.value

        elif score >= 60:
            level = DataQuality.GOOD.value

        elif score >= 40:
            level = DataQuality.POOR.value

        else:
            level = DataQuality.CRITICAL.value

        summary["quality_level"] = level

    def _build_recommendations(
        self,
        report: dict[str, Any]
    ) -> None:

        summary = report["summary"]

        recommendations = report["recommendations"]
        warnings = report["warnings"]

        if summary["constant_columns"] > 0:

            recommendations.append(
                "Supprimer les variables constantes."
            )

            warnings.append(
                f"{summary['constant_columns']} "
                "variable(s) constante(s) détectée(s)."
            )

        if summary["quasi_constant_columns"] > 0:

            recommendations.append(
                "Examiner les variables quasi constantes "
                "avant la modélisation."
            )

            warnings.append(
                f"{summary['quasi_constant_columns']} "
                "variable(s) quasi constante(s) détectée(s)."
            )

        if summary["high_cardinality_columns"] > 0:

            recommendations.append(
                "Examiner les variables à forte cardinalité "
                "et vérifier leur rôle dans l'analyse."
            )

            warnings.append(
                f"{summary['high_cardinality_columns']} "
                "variable(s) à forte cardinalité détectée(s)."
            )

        if summary["id_columns"] > 0:

            recommendations.append(
                "Vérifier les colonnes identifiées comme "
                "identifiants avant la modélisation."
            )

            warnings.append(
                f"{summary['id_columns']} "
                "colonne(s) potentiellement identifiantes détectée(s)."
            )

        if not recommendations:

            recommendations.append(
                "Aucun problème majeur de cardinalité détecté."
            )
