"""
EMIDAF Framework
EAIE - Problem Detection
"""

from __future__ import annotations

import pandas as pd


class ProblemDetector:
    """
    Détection prudente du type de problème supervisé.

    La détection automatique reste heuristique.
    L'utilisateur peut toujours imposer explicitement
    classification ou regression.
    """

    @staticmethod
    def detect(
        y: pd.Series,
        task: str | None = None,
    ) -> str:

        if task is not None:
            normalized = task.strip().lower()

            aliases = {
                "classification": "classification",
                "classifier": "classification",
                "class": "classification",
                "regression": "regression",
                "regressor": "regression",
                "reg": "regression",
            }

            if normalized not in aliases:
                raise ValueError(
                    "task doit être 'classification' "
                    "ou 'regression'."
                )

            return aliases[normalized]

        y = pd.Series(y).dropna()

        if y.empty:
            raise ValueError(
                "La variable cible ne contient "
                "aucune observation exploitable."
            )

        if (
            pd.api.types.is_bool_dtype(y)
            or isinstance(y.dtype, pd.CategoricalDtype)
            or pd.api.types.is_object_dtype(y)
            or pd.api.types.is_string_dtype(y)
        ):
            return "classification"

        if pd.api.types.is_numeric_dtype(y):

            n = len(y)
            unique = y.nunique(dropna=True)
            ratio = unique / max(n, 1)

            # Cible numérique discrète à faible cardinalité.
            # Il s'agit d'une heuristique, non d'une preuve.
            if unique <= 20 and ratio <= 0.20:
                return "classification"

            return "regression"

        return "classification"


def detect_problem(
    y: pd.Series,
    task: str | None = None,
) -> str:
    return ProblemDetector.detect(y, task=task)
