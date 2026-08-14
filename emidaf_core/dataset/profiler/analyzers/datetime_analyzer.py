"""
=========================================================
EMIDAF Framework v1.0
Datetime Analyzer
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .base_analyzer import BaseAnalyzer


class DatetimeAnalyzer(BaseAnalyzer):

    """
    Analyse des variables temporelles.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        dates = dataframe.select_dtypes(

            include="datetime"

        )

        results = {}

        for column in dates.columns:

            s = dates[column].dropna()

            if s.empty:
                continue

            results[column] = {

                "minimum":

                    s.min(),

                "maximum":

                    s.max(),

                "duration_days":

                    int(

                        (

                            s.max()

                            -

                            s.min()

                        ).days

                    ),

                "years":

                    sorted(

                        s.dt.year.unique()

                    ).tolist(),

                "months":

                    sorted(

                        s.dt.month.unique()

                    ).tolist(),

                "weekdays":

                    sorted(

                        s.dt.dayofweek.unique()

                    ).tolist()

            }

        return results