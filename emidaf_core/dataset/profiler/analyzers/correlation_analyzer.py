"""
=========================================================
EMIDAF Framework v1.0
Correlation Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base_analyzer import BaseAnalyzer


class CorrelationAnalyzer(BaseAnalyzer):
    """
    Corrélations numériques.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        numeric = dataframe.select_dtypes(
            include="number"
        )

        if numeric.empty:

            return {}

        return {

            "pearson":
                numeric.corr(
                    method="pearson"
                ).round(4).to_dict(),

            "spearman":
                numeric.corr(
                    method="spearman"
                ).round(4).to_dict(),

            "kendall":
                numeric.corr(
                    method="kendall"
                ).round(4).to_dict()

        }