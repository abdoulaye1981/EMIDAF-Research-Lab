"""
=========================================================
EMIDAF Framework v1.0
Quality Analyzer
=========================================================
"""

from __future__ import annotations

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class QualityAnalyzer(BaseAnalyzer):
    """
    Analyse la qualité globale d'un DataFrame.

    Le score est basé sur :
        - les valeurs manquantes
        - les doublons
    """

    name = "QualityAnalyzer"

    version = "1.0.0"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict:
        """
        Calcule les indicateurs de qualité.
        """

        dataframe = context.dataframe

        rows, columns = dataframe.shape

        total_cells = rows * columns

        missing_values = int(
            dataframe.isna().sum().sum()
        )

        duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        if total_cells == 0:

            missing_rate = 0.0

        else:

            missing_rate = missing_values / total_cells

        if rows == 0:

            duplicate_rate = 0.0

        else:

            duplicate_rate = duplicate_rows / rows

        # ==================================================
        # QUALITY SCORE
        # ==================================================

        quality_score = 100.0

        quality_score -= missing_rate * 60

        quality_score -= duplicate_rate * 40

        quality_score = max(

            0.0,

            min(100.0, quality_score)

        )

        return {

            "quality_score": round(
                quality_score,
                2
            ),

            "missing_values": missing_values,

            "missing_rate": round(
                missing_rate * 100,
                2
            ),

            "duplicate_rows": duplicate_rows,

            "duplicate_rate": round(
                duplicate_rate * 100,
                2
            ),

            "total_cells": total_cells,

            "rows": rows,

            "columns": columns

        }