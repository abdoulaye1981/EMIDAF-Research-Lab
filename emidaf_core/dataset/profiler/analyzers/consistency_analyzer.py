"""
=========================================================
EMIDAF Framework v1.0
Consistency Analyzer
---------------------------------------------------------
Analyse de la cohérence des données.
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class ConsistencyAnalyzer(BaseAnalyzer):

    name = "ConsistencyAnalyzer"
    version = "1.0.0"
    description = "Data Consistency Analysis"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        report = {
            "rows": context.rows,
            "columns": {},
            "inconsistent_columns": [],
            "summary": {},
            "warnings": [],
            "recommendations": []
        }

        inconsistent_columns = []

        total_missing = 0
        total_duplicated = 0
        total_infinite = 0

        for column in dataframe.columns:

            series = dataframe[column]

            missing = int(
                series.isna().sum()
            )

            duplicated = int(
                series.duplicated().sum()
            )

            infinite = 0

            if pd.api.types.is_numeric_dtype(series):

                infinite = int(
                    np.isinf(
                        series.dropna().to_numpy()
                    ).sum()
                )

            issues = []

            if missing > 0:
                issues.append(
                    "missing_values"
                )

            if infinite > 0:
                issues.append(
                    "infinite_values"
                )

            if issues:
                inconsistent_columns.append(
                    column
                )

            report["columns"][column] = {

                "dtype": str(
                    series.dtype
                ),

                "missing": missing,

                "duplicated": duplicated,

                "infinite": infinite,

                "consistent": len(
                    issues
                ) == 0,

                "issues": issues
            }

            total_missing += missing
            total_duplicated += duplicated
            total_infinite += infinite

        report["inconsistent_columns"] = (
            inconsistent_columns
        )

        report["summary"] = {

            "total_columns": len(
                dataframe.columns
            ),

            "inconsistent_columns": len(
                inconsistent_columns
            ),

            "total_missing_values": (
                total_missing
            ),

            "total_duplicated_values": (
                total_duplicated
            ),

            "total_infinite_values": (
                total_infinite
            )
        }

        if total_missing > 0:

            report["warnings"].append(
                f"{total_missing} valeur(s) "
                "manquante(s) détectée(s)."
            )

            report["recommendations"].append(
                "Analyser les valeurs manquantes "
                "avant toute imputation."
            )

        if total_infinite > 0:

            report["warnings"].append(
                f"{total_infinite} valeur(s) "
                "infinie(s) détectée(s)."
            )

            report["recommendations"].append(
                "Traiter les valeurs infinies "
                "avant les analyses statistiques."
            )

        if not report["warnings"]:

            report["recommendations"].append(
                "Aucun problème majeur de "
                "cohérence détecté."
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
