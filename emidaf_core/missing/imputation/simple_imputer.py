"""
=========================================================
EMIDAF Framework v1.0
Simple Imputer
---------------------------------------------------------
Imputation simple par moyenne ou mode.
=========================================================
"""

from __future__ import annotations

import pandas as pd

from emidaf_core.missing.imputation.base_imputer import (
    BaseImputer,
)


class SimpleImputer(BaseImputer):
    """
    Imputation simple des valeurs manquantes.

    Stratégies supportées :

    - MEAN :
        réservée aux variables numériques.

    - MODE :
        applicable aux variables numériques
        ou catégorielles.
    """

    def __init__(
        self,
        strategy: str = "MEAN",
    ) -> None:

        strategy = str(
            strategy
        ).strip().upper()

        if strategy not in {
            "MEAN",
            "MODE",
        }:
            raise ValueError(
                "strategy must be 'MEAN' or 'MODE'."
            )

        self.strategy = strategy

        self.name = strategy

    # =====================================================
    # IMPUTATION
    # =====================================================

    def impute(
        self,
        dataframe: pd.DataFrame,
        columns: list[str],
        **kwargs,
    ) -> pd.DataFrame:

        for column in columns:

            if not dataframe[column].isna().any():
                continue

            if self.strategy == "MEAN":

                self._impute_mean(
                    dataframe=dataframe,
                    column=column,
                )

            elif self.strategy == "MODE":

                self._impute_mode(
                    dataframe=dataframe,
                    column=column,
                )

        return dataframe

    # =====================================================
    # MEAN
    # =====================================================

    @staticmethod
    def _impute_mean(
       dataframe: pd.DataFrame,
       column: str,
    ) -> None:

       series = dataframe[
           column
       ]

       # Aucune valeur observée :
       # impossible de calculer une moyenne,
       # quel que soit le dtype inféré par pandas.
       if series.notna().sum() == 0:
          raise ValueError(
            f"Column '{column}' cannot be imputed "
            "with MEAN because no observed value "
            "is available."
         )

       if not pd.api.types.is_numeric_dtype(
         series
       ):
         raise TypeError(
            f"Column '{column}' must be numeric "
            "for MEAN imputation."
         )

       mean_value = series.mean()

       if pd.isna(
           mean_value
       ):
         raise ValueError(
            f"Column '{column}' cannot be imputed "
            "with MEAN because no valid numeric "
            "mean could be computed."
         )

       dataframe[column] = (
         series.fillna(
            mean_value
         )
       )
    # =====================================================
    # MODE
    # =====================================================

    @staticmethod
    def _impute_mode(
        dataframe: pd.DataFrame,
        column: str,
    ) -> None:

        series = dataframe[
            column
        ]

        modes = series.mode(
            dropna=True
        )

        if modes.empty:
            raise ValueError(
                f"Column '{column}' cannot be imputed "
                "with MODE because no observed value "
                "is available."
            )

        mode_value = modes.iloc[
            0
        ]

        dataframe[column] = (
            series.fillna(
                mode_value
            )
        )
