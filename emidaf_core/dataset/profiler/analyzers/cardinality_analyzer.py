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
from ...common.enums.data_quality import DataQuality


class CardinalityAnalyzer(BaseAnalyzer):
    """
    Analyse la cardinalité des variables.
    """

    name = "CardinalityAnalyzer"

    version = "1.0.0"

    description = "Cardinality Analysis"

    LOW_CARDINALITY = 10

    HIGH_CARDINALITY = 100

    ID_THRESHOLD = 0.95

    # =====================================================
    # PUBLIC
    # =====================================================

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

        low_cardinality = []

        high_cardinality = []

        id_columns = []

        quasi_constant = []

        for column in dataframe.columns:

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

            quasi = unique <= 2

            high = unique >= self.HIGH_CARDINALITY

            low = unique <= self.LOW_CARDINALITY

            id_like = (

                unique / rows

                >= self.ID_THRESHOLD

                if rows > 0

                else False

            )

            report["column_statistics"][column] = {

                "unique": unique,

                "unique_percentage": unique_percentage,

                "constant": constant,

                "quasi_constant": quasi,

                "low_cardinality": low,

                "high_cardinality": high,

                "id_like": id_like

            }

            if constant:

                constant_columns.append(column)

            if quasi:

                quasi_constant.append(column)

            if low:

                low_cardinality.append(column)

            if high:

                high_cardinality.append(column)

            if id_like:

                id_columns.append(column)

        report["summary"] = {

            "constant_columns": len(

                constant_columns

            ),

            "constant_column_names": constant_columns,

            "quasi_constant_columns": len(

                quasi_constant

            ),

            "quasi_constant_column_names": quasi_constant,

            "low_cardinality_columns": len(

                low_cardinality

            ),

            "low_cardinality_column_names": low_cardinality,

            "high_cardinality_columns": len(

                high_cardinality

            ),

            "high_cardinality_column_names": high_cardinality,

            "id_columns": len(

                id_columns

            ),

            "id_column_names": id_columns

        }

        self._compute_quality(

            report

        )

        self._build_recommendations(

            report

        )

        context.add_result(

            self.name,

            report

        )

        context.put_cache(

            self.name,

            report

        )

        return report

    # =====================================================
    # QUALITY
    # =====================================================

    def _compute_quality(

        self,

        report: dict[str, Any]

    ) -> None:

        summary = report["summary"]

        score = 100.0

        score -= summary["constant_columns"] * 10

        score -= summary["quasi_constant_columns"] * 5

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

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

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

                f"{summary['constant_columns']} variable(s) constante(s) détectée(s)."

            )

        if summary["quasi_constant_columns"] > 0:

            recommendations.append(

                "Examiner les variables quasi constantes."

            )

        if summary["high_cardinality_columns"] > 0:

            recommendations.append(

                "Évaluer une stratégie d'encodage adaptée aux variables à forte cardinalité."

            )

        if summary["id_columns"] > 0:

            recommendations.append(

                "Vérifier les colonnes identifiées comme identifiants avant la modélisation."

            )