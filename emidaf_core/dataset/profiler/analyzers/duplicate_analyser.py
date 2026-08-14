"""
=========================================================
EMIDAF Framework v1.0
Duplicate Analyzer
---------------------------------------------------------
Analyse des doublons.
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext
from ...common.enums.data_quality import DataQuality


class DuplicateAnalyzer(BaseAnalyzer):
    """
    Analyse les doublons du DataFrame.
    """

    name = "DuplicateAnalyzer"

    version = "1.0.0"

    description = "Duplicate Row Analysis"

    WARNING_RATE = 5.0

    CRITICAL_RATE = 15.0

    # =====================================================
    # PUBLIC
    # =====================================================

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        rows = context.rows

        duplicated_mask = dataframe.duplicated()

        duplicate_rows = int(

            duplicated_mask.sum()

        )

        duplicate_rate = (

            round(

                100 * duplicate_rows / rows,

                2

            )

            if rows > 0

            else 0.0

        )

        unique_rows = rows - duplicate_rows

        uniqueness_score = round(

            100 - duplicate_rate,

            2

        )

        report = {

            "rows": rows,

            "duplicate_rows": duplicate_rows,

            "duplicate_rate": duplicate_rate,

            "unique_rows": unique_rows,

            "unique_rate": round(

                100 - duplicate_rate,

                2

            ),

            "duplicate_index": dataframe.index[
                duplicated_mask
            ].tolist(),

            "duplicate_records": dataframe[
                duplicated_mask
            ].to_dict(
                orient="records"
            ),

            "quality_score": uniqueness_score,

            "summary": {},

            "warnings": [],

            "recommendations": []

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

        rate = report["duplicate_rate"]

        if rate == 0:

            level = DataQuality.EXCELLENT.value

        elif rate < self.WARNING_RATE:

            level = DataQuality.VERY_GOOD.value

        elif rate < self.CRITICAL_RATE:

            level = DataQuality.GOOD.value

        elif rate < 30:

            level = DataQuality.POOR.value

        else:

            level = DataQuality.CRITICAL.value

        report["summary"]["quality_level"] = level

        report["summary"]["uniqueness_score"] = report[
            "quality_score"
        ]

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    def _build_recommendations(

        self,

        report: dict[str, Any]

    ) -> None:

        rate = report["duplicate_rate"]

        recommendations = report["recommendations"]

        warnings = report["warnings"]

        if rate == 0:

            recommendations.append(

                "Aucun doublon détecté."

            )

            return

        recommendations.append(

            "Identifier la cause des doublons."

        )

        recommendations.append(

            "Supprimer les doublons avant la modélisation."

        )

        recommendations.append(

            "Contrôler les clés primaires ou identifiants."

        )

        if rate > self.WARNING_RATE:

            warnings.append(

                f"{rate:.2f}% de lignes sont dupliquées."

            )

        if rate > self.CRITICAL_RATE:

            warnings.append(

                "Le taux de doublons est critique."

            )