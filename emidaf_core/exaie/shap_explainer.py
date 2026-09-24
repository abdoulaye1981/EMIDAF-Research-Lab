"""
=========================================================
EMIDAF Framework
EXAIE - SHAP Explainer
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Explications globales et locales avec SHAP.
=========================================================
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline

from emidaf_core.common.results import (
    ShapResult,
)


class ShapExplainer:
    """
    Composant SHAP générique pour EMIDAF.
    """

    name = "SHAP Explainer"

    @staticmethod
    def _prepare_estimator(
        estimator: Any,
        X: pd.DataFrame,
    ):
        """
        Prépare un modèle simple ou un Pipeline sklearn.
        """

        if not isinstance(
            estimator,
            Pipeline,
        ):
            return (
                estimator,
                X.copy(),
                list(X.columns),
            )

        if len(estimator.steps) < 2:

            return (
                estimator,
                X.copy(),
                list(X.columns),
            )

        transformer = estimator.steps[0][1]

        model = estimator.steps[-1][1]

        transformed = transformer.transform(
            X
        )

        if hasattr(
            transformed,
            "toarray",
        ):
            transformed = (
                transformed.toarray()
            )

        transformed = np.asarray(
            transformed
        )

        try:

            feature_names = list(
                transformer
                .get_feature_names_out()
            )

        except Exception:

            feature_names = [
                f"variable_{index + 1}"
                for index in range(
                    transformed.shape[1]
                )
            ]

        transformed_df = pd.DataFrame(
            transformed,
            columns=[
                str(name)
                for name in feature_names
            ],
            index=X.index,
        )

        return (
            model,
            transformed_df,
            [
                str(name)
                for name in feature_names
            ],
        )

    @classmethod
    def explain(
        cls,
        estimator: Any,
        X: pd.DataFrame,
        *,
        task: str = "",
        max_samples: int | None = None,
    ) -> ShapResult:

        start = time.perf_counter()

        if not isinstance(
            X,
            pd.DataFrame,
        ):
            raise TypeError(
                "ShapExplainer attend X sous forme "
                "de pandas.DataFrame."
            )

        if X.empty:
            raise ValueError(
                "X est vide."
            )

        if X.isna().any().any():
            raise ValueError(
                "SHAP ne peut pas être exécuté "
                "avec des valeurs manquantes."
            )

        non_numeric = [
            column
            for column in X.columns
            if not pd.api.types.is_numeric_dtype(
                X[column]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Toutes les variables doivent être "
                "numériques avant SHAP. "
                f"Variables non numériques : "
                f"{non_numeric}"
            )

        if not np.isfinite(
            X.astype(float).to_numpy()
        ).all():
            raise ValueError(
                "SHAP exige des valeurs "
                "numériques finies."
            )

        if max_samples is not None:

            try:
                max_samples = int(
                    max_samples
                )

            except (
                TypeError,
                ValueError,
            ) as exc:

                raise ValueError(
                    "max_samples doit être un entier "
                    "ou None."
                ) from exc

            if max_samples < 1:
                raise ValueError(
                    "max_samples doit être "
                    "au moins égal à 1."
                )

        # =================================================
        # Dépendance optionnelle : chargement paresseux
        # =================================================

        try:
            import shap
        except ImportError as exc:
            raise RuntimeError(
                "SHAP n'est pas installé. "
                "Installez la dépendance 'shap' "
                "pour utiliser ShapExplainer."
            ) from exc

        model, prepared_X, feature_names = (
            cls._prepare_estimator(
                estimator,
                X,
            )
        )

        if max_samples is not None:

            prepared_X = prepared_X.iloc[
                :max_samples
            ].copy()

        # =================================================
        # Construction de l'explainer
        # =================================================

        try:

            model_module = type(
                model
            ).__module__.lower()

            model_name = type(
                model
            ).__name__.lower()

            is_xgboost = (
                "xgboost" in model_module
                or model_name.startswith(
                    "xgb"
                )
            )

            if is_xgboost:

                explainer = shap.TreeExplainer(
                    model,
                    feature_perturbation=(
                        "tree_path_dependent"
                    ),
                )

                explanation = explainer(
                    prepared_X,
                    check_additivity=False,
                )

            else:

                explainer = shap.Explainer(
                    model,
                    prepared_X,
                )

                explanation = explainer(
                    prepared_X
                )

        except Exception as exc:

            raise RuntimeError(
                "Impossible de construire "
                "l'explication SHAP pour ce modèle."
            ) from exc

        values = np.asarray(
            explanation.values
        )

        base_values = np.asarray(
            explanation.base_values
        )

        # =================================================
        # Importance globale
        # =================================================

        if values.ndim == 2:

            global_values = np.mean(
                np.abs(values),
                axis=0,
            )

        elif values.ndim == 3:

            global_values = np.mean(
                np.abs(values),
                axis=(
                    0,
                    2,
                ),
            )

        else:

            raise RuntimeError(
                "Format de valeurs SHAP "
                "non pris en charge."
            )

        feature_importance = {
            feature: float(value)
            for feature, value
            in zip(
                feature_names,
                global_values,
            )
        }

        feature_importance = dict(
            sorted(
                feature_importance.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        # =================================================
        # Explications locales compactes
        # =================================================

        local_explanations = []

        if values.ndim == 2:

            for row_index in range(
                values.shape[0]
            ):

                contributions = {
                    feature: float(value)
                    for feature, value
                    in zip(
                        feature_names,
                        values[
                            row_index
                        ],
                    )
                }

                local_explanations.append({
                    "row": int(row_index),
                    "contributions": contributions,
                })

        elif values.ndim == 3:

            for row_index in range(
                values.shape[0]
            ):

                contributions = {
                    feature: [
                        float(value)
                        for value in values[
                            row_index,
                            feature_index,
                            :
                        ]
                    ]
                    for feature_index, feature
                    in enumerate(
                        feature_names
                    )
                }

                local_explanations.append({
                    "row": int(row_index),
                    "contributions": contributions,
                })

        output_names = []

        if getattr(
            explanation,
            "output_names",
            None,
        ) is not None:

            try:
                output_names = [
                    str(value)
                    for value in (
                        explanation.output_names
                    )
                ]

            except TypeError:

                output_names = [
                    str(
                        explanation.output_names
                    )
                ]

        return ShapResult(
            name=cls.name,

            description=(
                "Explication globale et locale "
                "du modèle avec SHAP."
            ),

            success=True,

            model_name=type(
                model
            ).__name__,

            explainer_type=type(
                explainer
            ).__name__,

            task=str(
                task
            ),

            features=list(
                feature_names
            ),

            n_observations=len(
                prepared_X
            ),

            shap_values=(
                values.tolist()
            ),

            base_values=(
                base_values.tolist()
            ),

            feature_importance=(
                feature_importance
            ),

            local_explanations=(
                local_explanations
            ),

            output_names=(
                output_names
            ),

            execution_time=float(
                time.perf_counter()
                - start
            ),

            metadata={
                "method": "SHAP",
                "global_explanation": True,
                "local_explanation": True,
                "max_samples": max_samples,
            },
        )

    run = explain
