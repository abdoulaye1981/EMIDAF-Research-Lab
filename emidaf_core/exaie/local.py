"""
=========================================================
EMIDAF Framework
EXAIE - Local Explanation
=========================================================
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline


class LocalExplanation:
    """
    Explication locale d'une observation.
    """

    @staticmethod
    def _transform(
        estimator: Any,
        X: pd.DataFrame,
    ):
        """
        Transformation des données avec le preprocessing
        du pipeline.
        """

        if not isinstance(
            estimator,
            Pipeline,
        ):
            return (
                X.to_numpy(),
                list(X.columns),
                estimator,
            )

        if len(estimator.steps) < 2:
            return (
                X.to_numpy(),
                list(X.columns),
                estimator,
            )

        transformer = estimator.steps[0][1]
        model = estimator.steps[-1][1]

        transformed = transformer.transform(X)

        if hasattr(
            transformed,
            "toarray",
        ):
            transformed = transformed.toarray()

        try:
            names = list(
                transformer.get_feature_names_out()
            )
        except Exception:
            names = [
                f"variable_{i + 1}"
                for i in range(
                    transformed.shape[1]
                )
            ]

        return (
            np.asarray(transformed),
            [str(name) for name in names],
            model,
        )

    @classmethod
    def linear(
        cls,
        estimator: Any,
        X: pd.DataFrame,
        *,
        row: int = 0,
    ) -> dict:
        """
        Contribution locale pour modèle linéaire.

        contribution_j = x_j * beta_j
        """

        transformed, names, model = (
            cls._transform(
                estimator,
                X,
            )
        )

        if not hasattr(
            model,
            "coef_",
        ):
            return {
                "available": False,
                "reason": (
                    "Le modèle ne possède pas "
                    "de coefficients linéaires."
                ),
            }

        if row < 0 or row >= len(transformed):
            raise IndexError(
                "Indice d'observation invalide."
            )

        coef = np.asarray(
            model.coef_,
            dtype=float,
        )

        # Classification binaire / régression
        if coef.ndim == 1:
            coef_vector = coef

        elif coef.shape[0] == 1:
            coef_vector = coef[0]

        else:
            # Multiclasse :
            # classe prédite pour l'observation
            predicted = model.predict(
                transformed[[row]]
            )[0]

            classes = list(
                getattr(
                    model,
                    "classes_",
                    range(coef.shape[0]),
                )
            )

            class_index = classes.index(
                predicted
            )

            coef_vector = coef[
                class_index
            ]

        values = transformed[row]

        contributions = (
            values
            * coef_vector
        )

        table = pd.DataFrame(
            {
                "feature": names,
                "value": values,
                "coefficient": coef_vector,
                "contribution": contributions,
            }
        )

        table["abs_contribution"] = (
            table["contribution"]
            .abs()
        )

        table = (
            table
            .sort_values(
                "abs_contribution",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        prediction = estimator.predict(
            X.iloc[[row]]
        )[0]

        return {
            "available": True,
            "row": row,
            "prediction": prediction,
            "contributions": table,
        }
