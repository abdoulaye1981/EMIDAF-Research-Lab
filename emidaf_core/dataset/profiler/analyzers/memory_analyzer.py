"""
=========================================================
EMIDAF Framework v1.0

Memory Analyzer
=========================================================
"""

from __future__ import annotations

from emidaf_core.core.base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class MemoryAnalyzer(BaseAnalyzer):
    """
    Analyse la consommation mémoire du DataFrame.
    """

    name = "MemoryAnalyzer"
    version = "1.0.0"

    def analyze(
        self,
        context: ProfileContext
    ) -> dict:

        dataframe = context.dataframe

        column_memory = (
            dataframe.memory_usage(
                deep=True
            )
            .to_dict()
        )

        total = int(
            dataframe.memory_usage(
                deep=True
            ).sum()
        )

        average = (
            total / dataframe.shape[1]
            if dataframe.shape[1]
            else 0
        )

        result = {
            "total_bytes": total,
            "average_column_bytes": average,
            "column_memory": column_memory
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
