"""
=========================================================
EMIDAF Framework v1.0
Categorical Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base_analyzer import BaseAnalyzer


class CategoricalAnalyzer(BaseAnalyzer):

    """
    Analyse des variables catégorielles.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        categorical = dataframe.select_dtypes(

            include=[

                "object",

                "category",

                "string"

            ]

        )

        results = {}

        for column in categorical.columns:

            counts = dataframe[column].value_counts(
                dropna=False
            )

            percentages = (

                counts /

                len(dataframe)

                * 100

            ).round(2)

            results[column] = {

                "unique": int(

                    dataframe[column].nunique()

                ),

                "mode":

                    dataframe[column]

                    .mode()

                    .tolist(),

                "frequencies":

                    counts.to_dict(),

                "percentages":

                    percentages.to_dict(),

                "cardinality":

                    int(

                        dataframe[column]

                        .nunique()

                    )

            }

        return results