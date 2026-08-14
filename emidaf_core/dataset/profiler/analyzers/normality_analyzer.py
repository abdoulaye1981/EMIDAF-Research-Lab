"""
=========================================================
EMIDAF Framework v1.0
Normality Analyzer
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson

from .base_analyzer import BaseAnalyzer


class NormalityAnalyzer(BaseAnalyzer):
    """
    Tests de normalité.
    """

    MAX_SHAPIRO = 5000

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        numeric = dataframe.select_dtypes(
            include=np.number
        )

        report = {}

        for column in numeric.columns:

            values = numeric[column].dropna()

            if len(values) < 8:
                continue

            sample = values

            if len(values) > self.MAX_SHAPIRO:

                sample = values.sample(
                    self.MAX_SHAPIRO,
                    random_state=42
                )

            shapiro_stat, shapiro_p = shapiro(sample)

            dagostino_stat, dagostino_p = normaltest(values)

            anderson_result = anderson(values)

            report[column] = {

                "shapiro": {

                    "statistic": float(shapiro_stat),

                    "pvalue": float(shapiro_p),

                    "normal": bool(shapiro_p > 0.05)

                },

                "dagostino": {

                    "statistic": float(dagostino_stat),

                    "pvalue": float(dagostino_p),

                    "normal": bool(dagostino_p > 0.05)

                },

                "anderson": {

                    "statistic": float(anderson_result.statistic),

                    "critical_values": anderson_result.critical_values.tolist(),

                    "significance": anderson_result.significance_level.tolist()

                }

            }

        return report