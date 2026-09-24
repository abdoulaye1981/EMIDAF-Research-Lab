"""
=========================================================
EMIDAF Framework
EAIE - Logistic Regression
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
=========================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

from emidaf_core.common.results import (
    LogisticResult,
)


class LogisticRegressionModel:
    """
    Régression logistique EMIDAF.

    Supporte la classification binaire
    et multiclasses.
    """

    name = "Logistic Regression"
    task = "classification"
    library = "scikit-learn"

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        *,
        target: str,
        features: list[str] | None = None,
        test_dataframe: pd.DataFrame | None = None,
        threshold: float = 0.5,
        max_iter: int = 2000,
        random_state: int = 42,
        C: float = 1.0,
    ) -> LogisticResult:

        start = time.perf_counter()

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "LogisticRegressionModel attend "
                "un pandas.DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                "Le dataframe est vide."
            )

        if target not in dataframe.columns:
            raise ValueError(
                f"La variable cible '{target}' "
                "n'existe pas dans le dataframe."
            )

        if features is None:

            features = [
                column
                for column in dataframe.columns
                if column != target
            ]

        else:

            features = list(features)

        if not features:
            raise ValueError(
                "Au moins une variable explicative "
                "est nécessaire."
            )

        if len(features) != len(
            set(features)
        ):
            raise ValueError(
                "La liste des variables explicatives "
                "contient des doublons."
            )

        if target in features:
            raise ValueError(
                "La variable cible ne peut pas être "
                "une variable explicative."
            )

        missing_features = [
            column
            for column in features
            if column not in dataframe.columns
        ]

        if missing_features:
            raise ValueError(
                "Variables explicatives absentes : "
                f"{missing_features}"
            )

        selected = dataframe[
            features + [target]
        ].copy()

        if selected.isna().any().any():
            raise ValueError(
                "La régression logistique ne peut pas "
                "être exécutée avec des valeurs "
                "manquantes."
            )

        non_numeric = [
            column
            for column in features
            if not pd.api.types.is_numeric_dtype(
                selected[column]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Les variables explicatives doivent "
                "être numériques. Variables non "
                f"numériques : {non_numeric}"
            )

        X_train = (
            selected[
                features
            ]
            .astype(float)
        )

        y_train = (
            selected[
                target
            ]
        )

        if not np.isfinite(
            X_train.to_numpy()
        ).all():
            raise ValueError(
                "Les variables explicatives doivent "
                "contenir uniquement des valeurs finies."
            )

        classes = np.unique(
            y_train
        )

        if len(classes) < 2:
            raise ValueError(
                "La variable cible doit contenir "
                "au moins deux classes."
            )

        try:
            threshold = float(
                threshold
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "threshold doit être numérique."
            ) from exc

        if not 0 < threshold < 1:
            raise ValueError(
                "threshold doit être strictement "
                "compris entre 0 et 1."
            )

        try:
            C = float(C)
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "C doit être numérique."
            ) from exc

        if C <= 0:
            raise ValueError(
                "C doit être strictement positif."
            )

        model = LogisticRegression(
            max_iter=max_iter,
            random_state=random_state,
            C=C,
        )

        model.fit(
            X_train,
            y_train,
        )

        # =================================================
        # Données d'évaluation
        # =================================================

        if test_dataframe is None:

            X_eval = X_train
            y_eval = y_train

        else:

            if not isinstance(
                test_dataframe,
                pd.DataFrame,
            ):
                raise TypeError(
                    "test_dataframe doit être un "
                    "pandas.DataFrame."
                )

            required = (
                features + [target]
            )

            missing_test = [
                column
                for column in required
                if column
                not in test_dataframe.columns
            ]

            if missing_test:
                raise ValueError(
                    "Colonnes absentes dans "
                    "test_dataframe : "
                    f"{missing_test}"
                )

            test_selected = (
                test_dataframe[
                    required
                ].copy()
            )

            if (
                test_selected
                .isna()
                .any()
                .any()
            ):
                raise ValueError(
                    "test_dataframe contient des "
                    "valeurs manquantes."
                )

            X_eval = (
                test_selected[
                    features
                ]
                .astype(float)
            )

            y_eval = (
                test_selected[
                    target
                ]
            )

            if not np.isfinite(
                X_eval.to_numpy()
            ).all():
                raise ValueError(
                    "test_dataframe contient des "
                    "valeurs non finies."
                )

        # =================================================
        # Prédictions
        # =================================================

        probabilities = (
            model.predict_proba(
                X_eval
            )
        )

        model_classes = list(
            model.classes_
        )

        is_binary = (
            len(model_classes) == 2
        )

        if is_binary:

            positive_class = (
                model_classes[1]
            )

            negative_class = (
                model_classes[0]
            )

            predictions = np.where(
                probabilities[:, 1]
                >= threshold,
                positive_class,
                negative_class,
            )

        else:

            predictions = (
                model.predict(
                    X_eval
                )
            )

        # =================================================
        # Métriques
        # =================================================

        accuracy = float(
            accuracy_score(
                y_eval,
                predictions,
            )
        )

        precision = float(
            precision_score(
                y_eval,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        recall = float(
            recall_score(
                y_eval,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        f1 = float(
            f1_score(
                y_eval,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        roc_auc = None

        try:

            if is_binary:

                roc_auc = float(
                    roc_auc_score(
                        y_eval,
                        probabilities[:, 1],
                    )
                )

            else:

                roc_auc = float(
                    roc_auc_score(
                        y_eval,
                        probabilities,
                        multi_class="ovr",
                        average="weighted",
                        labels=model.classes_,
                    )
                )

        except ValueError:
            roc_auc = None

        try:

            model_log_loss = float(
                log_loss(
                    y_eval,
                    probabilities,
                    labels=model.classes_,
                )
            )

        except ValueError:
            model_log_loss = None

        # =================================================
        # Coefficients et odds ratios
        # =================================================

        coefficients = {}
        odds_ratios = {}

        coef_array = np.asarray(
            model.coef_
        )

        if is_binary:

            coefficients = {
                feature: float(value)
                for feature, value
                in zip(
                    features,
                    coef_array[0],
                )
            }

            odds_ratios = {
                feature: float(
                    np.exp(value)
                )
                for feature, value
                in coefficients.items()
            }

            intercept = float(
                model.intercept_[0]
            )

        else:

            for class_index, class_name in enumerate(
                model.classes_
            ):

                coefficients[
                    str(class_name)
                ] = {
                    feature: float(value)
                    for feature, value
                    in zip(
                        features,
                        coef_array[
                            class_index
                        ],
                    )
                }

                odds_ratios[
                    str(class_name)
                ] = {
                    feature: float(
                        np.exp(value)
                    )
                    for feature, value
                    in coefficients[
                        str(class_name)
                    ].items()
                }

            intercept = None

        # =================================================
        # Résultat
        # =================================================

        result = LogisticResult(
            name=cls.name,

            description=(
                "Régression logistique "
                "pour classification."
            ),

            model_name=cls.name,
            algorithm="LogisticRegression",
            model_type="classifier",
            task="classification",
            library=cls.library,
            fitted=True,

            train_size=len(
                y_train
            ),

            test_size=(
                0
                if test_dataframe is None
                else len(y_eval)
            ),

            features=list(
                features
            ),

            target=target,

            estimator=model,

            parameters={
                "max_iter": max_iter,
                "random_state": random_state,
                "C": C,
                "threshold": threshold,
            },

            score=f1,

            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            roc_auc=roc_auc,
            log_loss=model_log_loss,

            coefficients=coefficients,
            intercept=intercept,

            odds_ratios=odds_ratios,

            predictions=(
                np.asarray(
                    predictions
                ).tolist()
            ),

            probabilities=(
                np.asarray(
                    probabilities
                ).tolist()
            ),

            confusion_matrix=(
                confusion_matrix(
                    y_eval,
                    predictions,
                    labels=model.classes_,
                ).tolist()
            ),

            classification_report=(
                classification_report(
                    y_eval,
                    predictions,
                    labels=model.classes_,
                    output_dict=True,
                    zero_division=0,
                )
            ),

            classes=[
                value.item()
                if hasattr(
                    value,
                    "item",
                )
                else value
                for value in model.classes_
            ],

            n_classes=len(
                model.classes_
            ),

            is_binary=is_binary,

            threshold=(
                threshold
                if is_binary
                else None
            ),

            execution_time=float(
                time.perf_counter()
                - start
            ),

            metadata={
                "classification": True,
                "probabilistic_model": True,
                "binary": is_binary,
                "multiclass": (
                    not is_binary
                ),
            },
        )

        return result

    run = fit
