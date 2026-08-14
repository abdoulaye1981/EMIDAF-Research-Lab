"""
=========================================================
EMIDAF Framework v1.0
Text Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base_analyzer import BaseAnalyzer


class TextAnalyzer(BaseAnalyzer):

    """
    Analyse textuelle.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        objects = dataframe.select_dtypes(

            include=[

                "object",

                "string"

            ]

        )

        report = {}

        for column in objects.columns:

            values = (

                objects[column]

                .dropna()

                .astype(str)

            )

            if values.empty:
                continue

            report[column] = {

                "min_length":

                    int(

                        values.str.len().min()

                    ),

                "max_length":

                    int(

                        values.str.len().max()

                    ),

                "mean_length":

                    float(

                        values.str.len().mean()

                    ),

                "empty_strings":

                    int(

                        (

                            values == ""

                        ).sum()

                    ),

                "whitespace":

                    int(

                        values.str.contains(

                            r"^\s+$",

                            regex=True

                        ).sum()

                    )

            }

        return report