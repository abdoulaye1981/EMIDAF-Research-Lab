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
    """
    Construction des profils décisionnels EDSE.

    Les identifiants d'observation et d'élève sont des
    métadonnées de traçabilité.

    Ils ne sont jamais utilisés ici comme variables
    prédictives.
    """

    @staticmethod
    def _validate_identifiers(
        X: pd.DataFrame,
        observation_ids=None,
        student_ids=None,
    ) -> tuple[list, list | None]:

        observations = (
            list(observation_ids)
            if observation_ids is not None
            else list(X.index)
        )

        if len(observations) != len(X):
            raise ValueError(
                "Le nombre d'observation_ids doit "
                "correspondre au nombre de lignes de X."
            )

        students = None

        if student_ids is not None:
            students = list(student_ids)

            if len(students) != len(X):
                raise ValueError(
                    "Le nombre de student_ids doit "
                    "correspondre au nombre de lignes de X."
                )

        return observations, students

    @staticmethod
    def regression(
        X: pd.DataFrame,
        predictions,
        *,
        observation_ids=None,
        student_ids=None,
    ) -> pd.DataFrame:

        table = X.copy()

        (
            observations,
            students,
        ) = DecisionProfiles._validate_identifiers(
            X,
            observation_ids=observation_ids,
            student_ids=student_ids,
        )

        table.insert(
            0,
            "observation",
            observations,
        )

        if students is not None:
            table.insert(
                1,
                "id_eleve",
                students,
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
        *,
        observation_ids=None,
        student_ids=None,
    ) -> pd.DataFrame:

        table = X.copy()

        (
            observations,
            students,
        ) = DecisionProfiles._validate_identifiers(
            X,
            observation_ids=observation_ids,
            student_ids=student_ids,
        )

        table.insert(
            0,
            "observation",
            observations,
        )

        if students is not None:
            table.insert(
                1,
                "id_eleve",
                students,
            )

        table["probability"] = np.asarray(
            probabilities,
            dtype=float,
        )

        if predictions is not None:
            table["prediction"] = (
                np.asarray(predictions)
            )

        return table.sort_values(
            "probability",
            ascending=False,
        ).reset_index(
            drop=True
        )
