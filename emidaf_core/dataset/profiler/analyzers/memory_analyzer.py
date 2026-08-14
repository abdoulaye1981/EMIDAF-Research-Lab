"""
=========================================================
EMIDAF Framework v1.0
Memory Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base_analyzer import BaseAnalyzer


class MemoryAnalyzer(BaseAnalyzer):

    """
    Analyse mémoire.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

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

            total /

            dataframe.shape[1]

            if dataframe.shape[1]

            else 0

        )

        return {

            "total_bytes": total,

            "average_column_bytes": average,

            "column_memory": column_memory

        }