"""
=========================================================
EMIDAF Framework
EXAIE - Global Feature Importance
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline


def _final_estimator(estimator: Any) -> Any:
    """
    Retourne l'estimateur final d'un Pipeline sklearn.
    """

    if isinstance(estimator, Pipeline):
        return estimator.steps[-1][1]

    return estimator


def _feature_names(
    estimator: Any,
    X: pd.DataFrame,
) -> list[str]:
    """
    Récupère les noms des variables après preprocessing.
    """

    if not isinstance(estimator, Pipeline):
        return list(X.columns)

    if len(estimator.steps) < 2:
        return list(X.columns)

    transformer = estimator.steps[0][1]

    if hasattr(
        transformer,
        "get_feature_names_out",
    ):
        try:
            names = transformer.get_feature_names_out()
            return [str(name) for name in names]
        except Exception:
            pass

    return list(X.columns)


class GlobalImportance:
    """
    Analyse globale de l'importance des variables.
    """

    @staticmethod
    def native(
        estimator: Any,
        X: pd.DataFrame,
    ) -> pd.DataFrame | None:
        """
        Importance native du modèle.

        Compatible avec :
        - feature_importances_
        - coef_
        """

        model = _final_estimator(estimator)

        names = _feature_names(
            estimator,
            X,
        )

        values = None
        method = None

        # -------------------------------------------------
        # Arbres
        # -------------------------------------------------

        if hasattr(
            model,
            "feature_importances_",
        ):
            values = np.asarray(
                model.feature_importances_,
                dtype=float,
            )

            method = "feature_importances"

        # -------------------------------------------------
        # Modèles linéaires
        # -------------------------------------------------

        elif hasattr(
            model,
            "coef_",
        ):
            coef = np.asarray(
                model.coef_,
                dtype=float,
            )

            if coef.ndim == 1:
                values = np.abs(coef)

            else:
                values = np.mean(
                    np.abs(coef),
                    axis=0,
                )

            method = "coefficients"

        if values is None:
            return None

        if len(names) != len(values):
            names = [
                f"variable_{index + 1}"
                for index in range(
                    len(values)
                )
            ]

        result = pd.DataFrame(
            {
                "feature": names,
                "importance": values,
                "method": method,
            }
        )

        return (
            result
            .sort_values(
                "importance",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    @staticmethod
    def permutation(
        estimator: Any,
        X: pd.DataFrame,
        y,
        *,
        n_repeats: int = 10,
        random_state: int = 42,
        scoring: str | None = None,
    ) -> pd.DataFrame:
        """
        Importance par permutation.

        Cette méthode travaille sur les variables originales,
        avant transformation du Pipeline.
        """

        result = permutation_importance(
            estimator,
            X,
            y,
            n_repeats=n_repeats,
            random_state=random_state,
            scoring=scoring,
        )

        table = pd.DataFrame(
            {
                "feature": list(X.columns),
                "importance": result.importances_mean,
                "std": result.importances_std,
                "method": "permutation",
            }
        )

        return (
            table
            .sort_values(
                "importance",
                ascending=False,
            )
            .reset_index(drop=True)
        )
