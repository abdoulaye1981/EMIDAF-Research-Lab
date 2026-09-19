"""
=========================================================
EMIDAF Framework v1.0
Uniqueness Analyzer
---------------------------------------------------------
Analyse de l'unicité des variables.
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class UniquenessAnalyzer(BaseAnalyzer):

    name = "UniquenessAnalyzer"
    version = "1.0.0"
    description = "Column Uniqueness Analysis"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe
        rows = context.rows

        report = {
            "rows": rows,
            "columns": {},
            "unique_columns": [],
            "constant_columns": [],
            "summary": {},
            "warnings": [],
            "recommendations": []
        }

        for column in dataframe.columns:

            series = dataframe[column]

            unique_count = int(
                series.nunique(
                    dropna=False
                )
            )

            duplicate_count = (
                rows - unique_count
                if rows > 0
                else 0
            )

            unique_rate = (
                round(
                    100 * unique_count / rows,
                    2
                )
                if rows > 0
                else 0.0
            )

            is_unique = (
                unique_count == rows
                if rows > 0
                else False
            )

            is_constant = (
                unique_count <= 1
            )

            report["columns"][column] = {
                "unique_count": unique_count,
                "unique_rate": unique_rate,
                "duplicate_count": duplicate_count,
                "is_unique": is_unique,
                "is_constant": is_constant
            }

            if is_unique:
                report["unique_columns"].append(
                    column
                )

            if is_constant:
                report["constant_columns"].append(
                    column
                )

        report["summary"] = {
            "total_columns": len(
                dataframe.columns
            ),
            "unique_columns": len(
                report["unique_columns"]
            ),
            "constant_columns": len(
                report["constant_columns"]
            )
        }

        if report["unique_columns"]:

            report["warnings"].append(
                f"{len(report['unique_columns'])} "
                "variable(s) possède(nt) une valeur "
                "unique pour chaque observation."
            )

            report["recommendations"].append(
                "Vérifier si les variables totalement "
                "uniques correspondent à des identifiants."
            )

        if report["constant_columns"]:

            report["warnings"].append(
                f"{len(report['constant_columns'])} "
                "variable(s) constante(s) détectée(s)."
            )

            report["recommendations"].append(
                "Examiner et éventuellement supprimer "
                "les variables constantes avant la modélisation."
            )

        if (
            not report["unique_columns"]
            and not report["constant_columns"]
        ):

            report["recommendations"].append(
                "Aucun problème majeur d'unicité détecté."
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
