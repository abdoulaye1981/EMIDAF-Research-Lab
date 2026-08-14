"""
=========================================================
EMIDAF Framework v1.0
Distribution Analyzer
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import skew
from scipy.stats import kurtosis

from .base_analyzer import BaseAnalyzer


class DistributionAnalyzer(BaseAnalyzer):
    """
    Analyse les distributions numériques.
    """

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

            if values.empty:
                continue

            report[column] = {

                "minimum": float(values.min()),

                "maximum": float(values.max()),

                "mean": float(values.mean()),

                "median": float(values.median()),

                "std": float(values.std()),

                "variance": float(values.var()),

                "q1": float(values.quantile(.25)),

                "q3": float(values.quantile(.75)),

                "iqr": float(
                    values.quantile(.75)
                    -
                    values.quantile(.25)
                ),

                "skewness": float(
                    skew(
                        values,
                        bias=False
                    )
                ),

                "kurtosis": float(
                    kurtosis(
                        values,
                        fisher=True,
                        bias=False
                    )
                )

            }

        return report