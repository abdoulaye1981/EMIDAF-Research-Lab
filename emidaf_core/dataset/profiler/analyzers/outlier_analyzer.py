"""
=========================================================
EMIDAF Framework v1.0
Outlier Analyzer
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class OutlierAnalyzer(BaseAnalyzer):
    """
    Analyse des valeurs aberrantes avec la méthode IQR.
    """
    name = "OutlierAnalyzer"
    version = "1.0.0"
    def analyze(
            self,
            context: ProfileContext
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        datatype_result = context.results.get(
           "DatatypeAnalyzer"
        )

        if datatype_result is None:
            result = {
                "columns": {},
                "count": 0,
                "method": "IQR",
                "warnings": [],
                "recommendations": []
            }

            context.add_result(self.name, result)
            context.put_cache(self.name, result)

            return result

        datatype = datatype_result.result

        numeric_columns = datatype.get(
           "numeric",
           []
        )

        results = {}

        for column in numeric_columns:
            series = dataframe[column].dropna()

            series = series[
                 np.isfinite(series)
            ]

            if series.empty:

                results[column] = {
                    "count": 0,
                    "outliers": 0,
                    "outlier_rate": 0.0,
                    "lower_bound": None,
                    "upper_bound": None,
                    "method": "IQR"
                }

                continue

            q1 = series.quantile(0.25)

            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr

            upper_bound = q3 + 1.5 * iqr

            outliers = (
                (series < lower_bound)
                |
                (series > upper_bound)
            )

            outlier_count = int(
                outliers.sum()
            )

            results[column] = {
                "count": int(len(series)),
                "outliers": outlier_count,
                "outlier_rate": round(
                    100 * outlier_count / len(series),
                    2
                ),
                "lower_bound": float(
                    lower_bound
                ),
                "upper_bound": float(
                    upper_bound
                ),
                "method": "IQR"
            }

        result = {
            "columns": results,
            "count": len(results),
            "method": "IQR",
            "warnings": [],
            "recommendations": []
        }

        outlier_columns = [
            column
            for column, stats in results.items()
            if stats["outliers"] > 0
        ]

        if outlier_columns:
            result["warnings"].append(
                f"Valeurs aberrantes détectées dans "
                f"{len(outlier_columns)} variable(s)."
            )

            result["recommendations"].append(
                "Examiner les valeurs aberrantes avant "
                "la modélisation et déterminer si elles "
                "doivent être conservées, transformées "
                "ou traitées."
            )

        context.add_result(self.name, result)
        context.put_cache(self.name, result)

        return result
