"""
=========================================================
EMIDAF Framework v1.0
Multicollinearity Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from statsmodels.stats.outliers_influence import (
    variance_inflation_factor,
)

from .base_analyzer import BaseAnalyzer


class MulticollinearityAnalyzer(BaseAnalyzer):
    """
    Analyse de la multicolinéarité (VIF).
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        numeric = dataframe.select_dtypes(
            include="number"
        ).dropna()

        if numeric.shape[1] < 2:

            return {}

        vif = {}

        for i, column in enumerate(numeric.columns):

            vif[column] = float(

                variance_inflation_factor(

                    numeric.values,

                    i

                )

            )

        return {

            "vif": vif

        }