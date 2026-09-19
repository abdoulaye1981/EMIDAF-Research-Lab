"""
=========================================================
EMIDAF Framework v1.0

Datetime Analyzer

=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class DatetimeAnalyzer(BaseAnalyzer):

    """
    Analyse des variables de type date/heure.
    """

    name = "DatetimeAnalyzer"

    version = "1.0.0"

    description = "Analyse des variables temporelles"

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

        datetime_columns = datatype.get(
            "datetime",
            []
        )

        results = {}

        for column in datetime_columns:

            series = dataframe[column]

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

                "min": (
                    str(series.min())
                    if series.notna().any()
                    else None
                ),

                "max": (
                    str(series.max())
                    if series.notna().any()
                    else None
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
