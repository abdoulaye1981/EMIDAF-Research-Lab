"""
=========================================================
EMIDAF Framework v1.0
Text Analyzer
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class TextAnalyzer(BaseAnalyzer):

    name = "TextAnalyzer"
    version = "1.0.0"
    description = "Analyse des variables textuelles"

    def analyze(
        self,
        context: ProfileContext
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        datatype_result = context.results.get("DatatypeAnalyzer")

        if datatype_result is None:
            result = {
                "count": 0,
                "columns": {}
            }

            context.add_result(self.name, result)
            context.put_cache(self.name, result)

            return result

        datatype = datatype_result.result

        text_columns = datatype.get(
            "text",
            []
        )

        results = {}

        for column in text_columns:

            series = dataframe[column]

            non_null = series.dropna()

            if len(non_null) > 0:

                lengths = (
                    non_null
                    .astype(str)
                    .str.len()
                )

                average_length = float(
                    lengths.mean()
                )

                minimum_length = int(
                    lengths.min()
                )

                maximum_length = int(
                    lengths.max()
                )

            else:

                average_length = 0.0
                minimum_length = 0
                maximum_length = 0

            results[column] = {

                "dtype": str(
                    series.dtype
                ),

                "count": int(
                    series.count()
                ),

                "missing": int(
                    series.isna().sum()
                ),

                "unique": int(
                    series.nunique()
                ),

                "average_length": round(
                    average_length,
                    2
                ),

                "minimum_length": (
                    minimum_length
                ),

                "maximum_length": (
                    maximum_length
                )
            }

        result = {
            "count": len(results),
            "columns": results
        }

        context.add_result(self.name, result)
        context.put_cache(self.name, result)

        return result
