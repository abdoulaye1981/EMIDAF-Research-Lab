"""
=========================================================
EMIDAF Framework v1.0
Datatype Analyzer
=========================================================
"""

from __future__ import annotations

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class DatatypeAnalyzer(BaseAnalyzer):
    """
    Analyse les types de données du DataFrame.
    """

    name = "DatatypeAnalyzer"

    version = "1.0.0"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict:
        """
        Analyse les types de données.
        """

        dataframe = context.dataframe

        numeric = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical = dataframe.select_dtypes(
            include="category"
        ).columns.tolist()

        boolean = dataframe.select_dtypes(
            include="bool"
        ).columns.tolist()

        datetime = dataframe.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns.tolist()

        text = dataframe.select_dtypes(
            include=["object", "string"]
        ).columns.tolist()

        unknown = [

            column

            for column in dataframe.columns

            if column not in (

                numeric +

                categorical +

                boolean +

                datetime +

                text

            )

        ]

        return {

            "numeric": numeric,

            "categorical": categorical,

            "boolean": boolean,

            "datetime": datetime,

            "text": text,

            "unknown": unknown,

            "dtypes": dataframe.dtypes.astype(str).to_dict(),

            "count": {

                "numeric": len(numeric),

                "categorical": len(categorical),

                "boolean": len(boolean),

                "datetime": len(datetime),

                "text": len(text),

                "unknown": len(unknown)

            }

        }