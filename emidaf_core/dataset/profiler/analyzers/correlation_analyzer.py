"""
=========================================================
EMIDAF Framework v1.0

Correlation Analyzer

---------------------------------------------------------

Analyse des corrélations entre variables numériques.

=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class CorrelationAnalyzer(BaseAnalyzer):

    """
    Analyse les corrélations entre variables numériques.
    """

    name = "CorrelationAnalyzer"
    version = "1.0.0"
    description = "Analyse des corrélations numériques"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        datatype_result = context.results.get(
              "DatatypeAnalyzer"
        )

        if datatype_result is None:
              return {
                  "columns": [],
                  "count": 0,
                  "correlation_matrix": {},
                  "pairs": []
              }

        datatype = datatype_result.result

        numeric_columns = datatype.get(
             "numeric",
             []
        )

        numeric = dataframe[numeric_columns]

        if numeric.empty:
              return {
                 "columns": [],
                 "count": 0,
                 "correlation_matrix": {},
                 "pairs": []
              }
        numeric = numeric.replace(
            [np.inf, -np.inf],
            np.nan
        )


        correlation_matrix = (
            numeric
            .corr()
            .round(4)
        )

        pairs = []

        columns = correlation_matrix.columns.tolist()

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                column_1 = columns[i]
                column_2 = columns[j]

                correlation = correlation_matrix.loc[
                    column_1,
                    column_2
                ]

                if pd.isna(correlation):
                    continue

                pairs.append({
                    "variable_1": column_1,
                    "variable_2": column_2,
                    "correlation": float(correlation)
                })

        pairs.sort(
            key=lambda x: abs(
                x["correlation"]
            ),
            reverse=True
        )

        result = {
            "columns": columns,
            "count": len(columns),
            "correlation_matrix": (
                correlation_matrix
                .to_dict()
            ),
            "pairs": pairs
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
