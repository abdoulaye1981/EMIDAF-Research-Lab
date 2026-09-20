"""
=========================================================
EMIDAF Framework
EDSE - Decision Profiles
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class DecisionProfiles:

    @staticmethod
    def regression(
        X: pd.DataFrame,
        predictions,
    ) -> pd.DataFrame:

        table = X.copy()

        table.insert(
            0,
            "observation",
            range(len(table)),
        )

        table["prediction"] = np.asarray(
            predictions,
            dtype=float,
        )

        return table.sort_values(
            "prediction",
            ascending=False,
        ).reset_index(
            drop=True
        )

    @staticmethod
    def classification(
        X: pd.DataFrame,
        probabilities,
        predictions=None,
    ) -> pd.DataFrame:

        table = X.copy()

        table.insert(
            0,
            "observation",
            range(len(table)),
        )

        table["probability"] = np.asarray(
            probabilities,
            dtype=float,
        )

        if predictions is not None:
            table["prediction"] = (
                predictions
            )

        return table.sort_values(
            "probability",
            ascending=False,
        ).reset_index(
            drop=True
        )
