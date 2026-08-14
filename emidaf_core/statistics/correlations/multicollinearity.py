"""
=========================================================
EMIDAF Framework
Multicollinearity Analysis
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Analyse de la multicolinéarité.

Contient

- Variance Inflation Factor (VIF)
- Tolérance
- Détection automatique
- Variables problématiques
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from statsmodels.stats.outliers_influence import (
    variance_inflation_factor,
)


class VarianceInflationFactor:
    """
    Calcul du Variance Inflation Factor.
    """

    @staticmethod
    def compute(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe = dataframe.select_dtypes(

            include="number"

        ).dropna()

        vif = pd.DataFrame()

        vif["Variable"] = dataframe.columns

        vif["VIF"] = [

            variance_inflation_factor(

                dataframe.values,

                i

            )

            for i in range(

                dataframe.shape[1]

            )

        ]

        vif["Tolerance"] = 1 / vif["VIF"]

        return vif


class MulticollinearityAnalyzer:
    """
    Analyse complète de la multicolinéarité.
    """

    @staticmethod
    def compute(
        dataframe: pd.DataFrame,
        threshold: float = 5.0,
    ) -> dict:

        vif = VarianceInflationFactor.compute(

            dataframe

        )

        problematic = vif.loc[

            vif["VIF"] >= threshold

        ]

        return {

            "vif": vif,

            "threshold": threshold,

            "problematic_variables":

                problematic["Variable"].tolist(),

            "problematic_count":

                len(problematic),

            "has_multicollinearity":

                len(problematic) > 0

        }

    @staticmethod
    def summary(
        dataframe: pd.DataFrame,
    ) -> dict:

        return MulticollinearityAnalyzer.compute(

            dataframe

        )