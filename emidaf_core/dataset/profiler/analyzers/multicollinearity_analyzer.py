"""
=========================================================
EMIDAF Framework v1.0
Multicollinearity Analyzer
---------------------------------------------------------
Analyse de la multicolinéarité entre variables numériques.
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .base_analyzer import BaseAnalyzer
from ..profile_context import ProfileContext


class MulticollinearityAnalyzer(BaseAnalyzer):
    """
    Analyse la multicolinéarité entre variables numériques.
    """

    name = "MulticollinearityAnalyzer"
    version = "1.0.0"
    description = "Analyse de la multicolinéarité"

    def analyze(
        self,
        context: ProfileContext
    ) -> dict[str, Any]:

        dataframe = context.dataframe

        numeric = dataframe.select_dtypes(
            include="number"
        )

        columns = numeric.columns.tolist()

        if len(columns) < 2:
            result = {
                "columns": columns,
                "count": len(columns),
                "correlation_matrix": {},
                "vif": {},
                "vif_interpretation": {},
                "high_correlations": [],
                "multicollinearity_detected": False,
                "warnings": [],
                "recommendations": [],
                "status": "insufficient_variables"
            }

            context.add_result(self.name, result)
            context.put_cache(self.name, result)

            return result
        # -------------------------------------------------
        # Nettoyage des valeurs infinies
        # -------------------------------------------------

        numeric = numeric.replace(
            [np.inf, -np.inf],
            np.nan
        )

        # -------------------------------------------------
        # Matrice de corrélation
        # -------------------------------------------------

        correlation_matrix = (
            numeric
            .corr()
            .round(4)
        )

        # -------------------------------------------------
        # Détection des fortes corrélations
        # -------------------------------------------------

        high_correlations = []

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                variable_1 = columns[i]
                variable_2 = columns[j]

                correlation = correlation_matrix.loc[
                    variable_1,
                    variable_2
                ]

                if pd.isna(correlation):
                    continue

                if abs(correlation) >= 0.8:
                    high_correlations.append({
                        "variable_1": variable_1,
                        "variable_2": variable_2,
                        "correlation": float(
                            correlation
                        )
                    })

        # -------------------------------------------------
        # Calcul du VIF
        # -------------------------------------------------

        vif = {}

        try:

            matrix = numeric.dropna()

            if len(matrix) > len(columns):

                values = matrix.to_numpy(
                    dtype=float
                )

                for i, column in enumerate(columns):

                    y = values[:, i]

                    x = np.delete(
                        values,
                        i,
                        axis=1
                    )

                    x = np.column_stack([
                        np.ones(len(x)),
                        x
                    ])

                    coefficients = np.linalg.lstsq(
                        x,
                        y,
                        rcond=None
                    )[0]

                    prediction = x @ coefficients

                    ss_residual = np.sum(
                        (y - prediction) ** 2
                    )

                    ss_total = np.sum(
                        (y - np.mean(y)) ** 2
                    )

                    if ss_total == 0:
                        vif[column] = None
                        continue

                    r_squared = (
                        1
                        - ss_residual / ss_total
                    )

                    if np.isclose(
                        r_squared,
                        1.0,
                        atol=1e-10
                    ):
                        vif[column] = float("inf")

                    elif r_squared < 1:

                        vif[column] = round(
                            float(
                                1 /
                                (1 - r_squared)
                            ),
                            4
                        )

                    else:
                        vif[column] = None

        except (
            ValueError,
            np.linalg.LinAlgError
        ):
            vif = {}

        # -------------------------------------------------
        # Interprétation du VIF
        # -------------------------------------------------

        vif_interpretation = {}

        for column, value in vif.items():

            if value is None:
                vif_interpretation[column] = (
                    "Non interprétable"
                )

            elif np.isinf(value):
                vif_interpretation[column] = (
                    "Multicolinéarité parfaite"
                )

            elif value < 5:
                vif_interpretation[column] = (
                    "Multicolinéarité faible"
                )

            elif value < 10:
                vif_interpretation[column] = (
                    "Multicolinéarité modérée"
                )

            else:
                vif_interpretation[column] = (
                    "Multicolinéarité forte"
                )

        # -------------------------------------------------
        # Détection globale
        # -------------------------------------------------

        multicollinearity_detected = (
            len(high_correlations) > 0
            or any(
                value is not None
                and (
                    np.isinf(value)
                    or value >= 5
                )
                for value in vif.values()
            )
        )

        # -------------------------------------------------
        # Warnings
        # -------------------------------------------------

        warnings = []

        if high_correlations:
            warnings.append(
                (
                    f"{len(high_correlations)} paire(s) "
                    "de variables présentent une "
                    "forte corrélation "
                    "(|r| >= 0.8)."
                )
            )

        perfect_vif = [
            column
            for column, value in vif.items()
            if value is not None
            and np.isinf(value)
        ]

        if perfect_vif:
            warnings.append(
                (
                    "Multicolinéarité parfaite détectée "
                    "pour : "
                    + ", ".join(perfect_vif)
                    + "."
                )
            )

        strong_vif = [
            column
            for column, value in vif.items()
            if value is not None
            and not np.isinf(value)
            and value >= 10
        ]

        if strong_vif:
            warnings.append(
                (
                    "VIF >= 10 détecté pour : "
                    + ", ".join(strong_vif)
                    + "."
                )
            )

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        recommendations = []

        if multicollinearity_detected:
            recommendations.append(
                (
                    "Examiner les variables fortement "
                    "corrélées avant leur utilisation "
                    "dans un modèle statistique ou "
                    "de Machine Learning."
                )
            )

            recommendations.append(
                (
                    "Envisager la suppression d'une "
                    "des variables redondantes, une "
                    "transformation des variables ou "
                    "une réduction dimensionnelle "
                    "(par exemple ACP) selon le contexte."
                )
            )

        if perfect_vif:
            recommendations.append(
                (
                    "Vérifier les variables présentant "
                    "un VIF infini : elles peuvent "
                    "contenir une information redondante "
                    "ou être des combinaisons linéaires "
                    "d'autres variables."
                )
            )

        result = {
            "columns": columns,
            "count": len(columns),
            "correlation_matrix": (
                correlation_matrix
                .to_dict()
            ),
            "vif": vif,
            "vif_interpretation": vif_interpretation,
            "high_correlations": high_correlations,
            "multicollinearity_detected": (
                multicollinearity_detected
            ),
            "warnings": warnings,
            "recommendations": recommendations,
            "status": "success"
        }

        context.add_result(self.name, result)
        context.put_cache(self.name, result)

        return result
