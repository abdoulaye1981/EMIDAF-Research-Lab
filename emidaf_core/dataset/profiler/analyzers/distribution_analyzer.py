"""
=========================================================
EMIDAF Framework v1.0

Distribution Analyzer
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class DistributionAnalyzer(BaseAnalyzer):
    """
    Analyse de la distribution des variables numériques.
    """

    name = "DistributionAnalyzer"
    version = "1.0.0"
    description = "Analyse des distributions numériques"

    def analyze(
        self,
        context: ProfileContext
    ) -> dict[str, Any]:


        dataframe = context.dataframe

        datatype_result = context.results.get(
            "DatatypeAnalyzer"
        )

        if datatype_result is None:
             return {
                "count": 0,
                "columns": {}
             }

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
                    "mean": None,
                    "median": None,
                    "std": None,
                    "variance": None,
                    "minimum": None,
                    "maximum": None,
                    "range": None,
                    "q1": None,
                    "q3": None,
                    "iqr": None,
                    "skewness": None,
                    "kurtosis": None
                }

                continue

            q1 = float(
                series.quantile(0.25)
            )

            q3 = float(
                series.quantile(0.75)
            )

            results[column] = {
                "count": int(series.count()),

                "mean": float(
                    series.mean()
                ),

                "median": float(
                    series.median()
                ),

                "std": float(
                    series.std()
                ),

                "variance": float(
                    series.var()
                ),

                "minimum": float(
                    series.min()
                ),

                "maximum": float(
                    series.max()
                ),

                "range": float(
                    series.max() - series.min()
                ),

                "q1": q1,

                "q3": q3,

                "iqr": float(
                    q3 - q1
                ),

                "skewness": float(
                    series.skew()
                ),

                "kurtosis": float(
                    series.kurtosis()
                )
            }

        result = {
            "count": len(results),
            "columns": results
        }

        context.add_result(
            self.name,
            result
        )

        context.put_cache(
            self.name,
            result
        )

        return result
