"""
=========================================================
EMIDAF Framework v1.0
Structure Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from emidaf_core.core.base_analyzer import BaseAnalyzer

from ..profile_context import ProfileContext


class StructureAnalyzer(BaseAnalyzer):
    """
    Analyse la structure générale du DataFrame.
    """

    name = "StructureAnalyzer"

    version = "1.0.0"

    def analyze(
        self,
        context: ProfileContext,
    ) -> dict:
        """
        Analyse la structure du DataFrame.
        """

        dataframe = context.dataframe

        rows, columns = dataframe.shape

        memory_usage = int(

            dataframe.memory_usage(

                deep=True

            ).sum()

        )

        return {

            "rows": rows,

            "columns": columns,

            "shape": dataframe.shape,

            "column_names": dataframe.columns.tolist(),

            "index_type": type(

                dataframe.index

            ).__name__,

            "memory_usage": memory_usage,

        }