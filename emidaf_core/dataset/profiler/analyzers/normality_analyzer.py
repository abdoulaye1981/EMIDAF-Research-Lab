"""
=========================================================
EMIDAF Framework v1.0

Normality Analyzer
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import shapiro

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class NormalityAnalyzer(BaseAnalyzer):
    """
    Analyse de la normalité des variables numériques.
    """

    name = "NormalityAnalyzer"
    version = "1.0.0"
    description = "Analyse de la normalité des variables numériques"

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
                "count": 0,
                "columns": {},
                "test": "Shapiro-Wilk",
                "alpha": 0.05
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

            n = len(series)

            if n < 3:

                results[column] = {
                    "n": int(n),
                    "statistic": None,
                    "p_value": None,
                    "normal": None,
                    "interpretation": (
                        "Test impossible : "
                        "au moins 3 observations sont nécessaires."
                    )
                }

                continue


            if series.nunique() <= 1:

                results[column] = {
                     "n": int(n),
                     "statistic": None,
                     "p_value": None,
                     "normal": None,
                     "interpretation": (
                          "Test impossible : "
                          "la variable est constante."
                     )
                }
                continue

            try:

                statistic, p_value = shapiro(
                    series
                )

                statistic = float(statistic)
                p_value = float(p_value)

                normal = p_value > 0.05

                if normal:
                    interpretation = (
                        "La normalité n'est pas rejetée "
                        "(p > 0.05)."
                    )
                else:
                    interpretation = (
                        "La normalité est rejetée "
                        "(p ≤ 0.05)."
                    )

                results[column] = {
                    "n": int(n),
                    "statistic": statistic,
                    "p_value": p_value,
                    "normal": normal,
                    "interpretation": interpretation
                }

            except Exception as error:

                results[column] = {
                    "n": int(n),
                    "statistic": None,
                    "p_value": None,
                    "normal": None,
                    "interpretation": (
                        "Erreur lors du test de normalité."
                    ),
                    "error": str(error)
                }

        result = {
            "count": len(results),
            "columns": results,
            "test": "Shapiro-Wilk",
            "alpha": 0.05
        }

        context.add_result(self.name, result)
        context.put_cache(self.name, result)

        return result
