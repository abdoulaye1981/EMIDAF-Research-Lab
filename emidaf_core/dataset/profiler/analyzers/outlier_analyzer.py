"""
=========================================================
EMIDAF Framework v1.0
Outlier Analyzer
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import zscore

from .base_analyzer import BaseAnalyzer


class OutlierAnalyzer(BaseAnalyzer):
    """
    Détection des valeurs aberrantes.
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

            if len(values) < 5:
                continue

            q1 = values.quantile(.25)

            q3 = values.quantile(.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            iqr_outliers = values[
                (values < lower)
                |
                (values > upper)
            ]

            z = np.abs(
                zscore(values)
            )

            z_outliers = values[
                z > 3
            ]

            report[column] = {

                "iqr": {

                    "count": int(len(iqr_outliers)),

                    "index": iqr_outliers.index.tolist()

                },

                "zscore": {

                    "count": int(len(z_outliers)),

                    "index": z_outliers.index.tolist()

                }

            }

        return report