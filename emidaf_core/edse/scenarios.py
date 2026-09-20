"""
=========================================================
EMIDAF Framework
EDSE - Decision Scenarios
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class DecisionScenarios:

    @staticmethod
    def regression(
        predictions,
        *,
        threshold: float,
        direction: str = "above",
    ) -> pd.DataFrame:
        """
        Analyse d'un scénario pour une cible continue.

        direction:
        - above : observations >= seuil
        - below : observations <= seuil
        """

        values = np.asarray(
            predictions,
            dtype=float,
        )

        if direction not in {
            "above",
            "below",
        }:
            raise ValueError(
                "direction doit être 'above' "
                "ou 'below'."
            )

        if direction == "above":

            selected = (
                values >= threshold
            )

        else:

            selected = (
                values <= threshold
            )

        return pd.DataFrame(
            {
                "prediction": values,
                "selected": selected,
            }
        )

    @staticmethod
    def classification(
        probabilities,
        *,
        threshold: float = 0.50,
    ) -> pd.DataFrame:
        """
        Scénario binaire basé sur une probabilité.

        Aucun seuil n'est présenté comme optimal.
        """

        if not 0 <= threshold <= 1:
            raise ValueError(
                "Le seuil doit être compris "
                "entre 0 et 1."
            )

        values = np.asarray(
            probabilities,
            dtype=float,
        )

        selected = (
            values >= threshold
        )

        return pd.DataFrame(
            {
                "probability": values,
                "selected": selected,
            }
        )

    @staticmethod
    def summarize(
        table: pd.DataFrame,
    ) -> dict:

        if table.empty:
            return {
                "observations": 0,
                "selected": 0,
                "not_selected": 0,
                "selected_rate": 0.0,
            }

        selected = int(
            table["selected"].sum()
        )

        total = len(table)

        return {
            "observations": total,
            "selected": selected,
            "not_selected": total - selected,
            "selected_rate": (
                selected / total
            ),
        }
