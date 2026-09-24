"""
=========================================================
EMIDAF Framework
EAIE - XGBoost
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Composant XGBoost pour classification
et régression.
=========================================================
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)

from xgboost import (
    XGBClassifier,
    XGBRegressor,
)

from emidaf_core.common.results import (
    ModelResult,
)


class XGBoostModel:
    """
    XGBoost EMIDAF.

    Supporte :
    - classification binaire ;
    - classification multiclasses ;
    - régression.
    """

    name = "XGBoost"
    library = "xgboost"

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        *,
        target: str,
        task: str,
        features: list[str] | None = None,
        test_dataframe: pd.DataFrame | None = None,
        n_estimators: int = 100,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        subsample: float = 1.0,
        colsample_bytree: float = 1.0,
        random_state: int = 42,
        n_jobs: int = 1,
    ) -> ModelResult:

        start = time.perf_counter()

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "XGBoostModel attend un pandas.DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                "Le dataframe est vide."
            )

        task = str(
            task
        ).strip().lower()

        if task not in {
            "classification",
            "regression",
        }:
            raise ValueError(
                "task doit être 'classification' "
                "ou 'regression'."
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

            features = list(
                features
            )

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
            feature
            for feature in features
            if feature not in dataframe.columns
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
                "XGBoostModel ne peut pas être exécuté "
                "avec des valeurs manquantes."
            )

        non_numeric = [
            feature
            for feature in features
            if not pd.api.types.is_numeric_dtype(
                selected[feature]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Les variables explicatives doivent être "
                "numériques. Variables non numériques : "
                f"{non_numeric}"
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

        if task == "regression":

            if not pd.api.types.is_numeric_dtype(
                y_train
            ):
                raise ValueError(
                    "La cible d'un modèle XGBoost de "
                    "régression doit être numérique."
                )

            if not np.isfinite(
                y_train.astype(float).to_numpy()
            ).all():
                raise ValueError(
                    "La variable cible contient "
                    "des valeurs non finies."
                )

        else:

            if y_train.nunique() < 2:
                raise ValueError(
                    "La variable cible doit contenir "
                    "au moins deux classes."
                )

        try:
            n_estimators = int(
                n_estimators
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "n_estimators doit être un entier."
            ) from exc

        if n_estimators < 1:
            raise ValueError(
                "n_estimators doit être au moins égal à 1."
            )

        try:
            max_depth = int(
                max_depth
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "max_depth doit être un entier."
            ) from exc

        if max_depth < 1:
            raise ValueError(
                "max_depth doit être strictement positif."
            )

        try:
            learning_rate = float(
                learning_rate
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "learning_rate doit être numérique."
            ) from exc

        if learning_rate <= 0:
            raise ValueError(
                "learning_rate doit être strictement positif."
            )

        for name, value in {
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
        }.items():

            try:
                value = float(value)
            except (
                TypeError,
                ValueError,
            ) as exc:
                raise ValueError(
                    f"{name} doit être numérique."
                ) from exc

            if not 0 < value <= 1:
                raise ValueError(
                    f"{name} doit être compris "
                    "dans l'intervalle ]0, 1]."
                )

            if name == "subsample":
                subsample = value
            else:
                colsample_bytree = value

        common_parameters = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "random_state": random_state,
            "n_jobs": n_jobs,
        }

        if task == "classification":

            model = XGBClassifier(
                **common_parameters,
                eval_metric="logloss",
            )

        else:

            model = XGBRegressor(
                **common_parameters,
                objective="reg:squarederror",
            )

        model.fit(
            X_train,
            y_train,
        )

        if test_dataframe is None:

            X_eval = X_train
            y_eval = y_train

        else:

            if not isinstance(
                test_dataframe,
                pd.DataFrame,
            ):
                raise TypeError(
                    "test_dataframe doit être "
                    "un pandas.DataFrame."
                )

            required = (
                features + [target]
            )

            missing_test = [
                column
                for column in required
                if column not in test_dataframe.columns
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
                    "test_dataframe contient "
                    "des valeurs manquantes."
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
                    "test_dataframe contient "
                    "des valeurs non finies."
                )

        predictions = model.predict(
            X_eval
        )

        feature_importance = {
            feature: float(value)
            for feature, value
            in zip(
                features,
                model.feature_importances_,
            )
        }

        result = ModelResult(
            name=cls.name,
            description=(
                f"XGBoost pour {task}."
            ),
            model_name=cls.name,
            algorithm=type(
                model
            ).__name__,
            model_type=(
                "classifier"
                if task == "classification"
                else "regressor"
            ),
            task=task,
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
            parameters=dict(
                common_parameters
            ),
            predictions=(
                np.asarray(
                    predictions
                ).tolist()
            ),
            feature_importance=(
                feature_importance
            ),
            execution_time=float(
                time.perf_counter()
                - start
            ),
            metadata={
                "boosting": True,
                "tree_based": True,
                "task": task,
            },
        )

        if task == "classification":

            result.accuracy = float(
                accuracy_score(
                    y_eval,
                    predictions,
                )
            )

            result.precision = float(
                precision_score(
                    y_eval,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            )

            result.recall = float(
                recall_score(
                    y_eval,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            )

            result.f1_score = float(
                f1_score(
                    y_eval,
                    predictions,
                    average="weighted",
                    zero_division=0,
                )
            )

            result.score = (
                result.f1_score
            )

            result.confusion_matrix = (
                confusion_matrix(
                    y_eval,
                    predictions,
                ).tolist()
            )

            result.classification_report = (
                classification_report(
                    y_eval,
                    predictions,
                    output_dict=True,
                    zero_division=0,
                )
            )

            probabilities = (
                model.predict_proba(
                    X_eval
                )
            )

            result.probabilities = (
                np.asarray(
                    probabilities
                ).tolist()
            )

            classes = np.unique(
                y_eval
            )

            try:

                if len(classes) == 2:

                    result.roc_auc = float(
                        roc_auc_score(
                            y_eval,
                            probabilities[:, 1],
                        )
                    )

                else:

                    result.roc_auc = float(
                        roc_auc_score(
                            y_eval,
                            probabilities,
                            multi_class="ovr",
                            average="weighted",
                        )
                    )

            except ValueError:

                result.roc_auc = None

            try:

                result.log_loss = float(
                    log_loss(
                        y_eval,
                        probabilities,
                    )
                )

            except ValueError:

                result.log_loss = None

        else:

            residuals = (
                np.asarray(
                    y_eval,
                    dtype=float,
                )
                - np.asarray(
                    predictions,
                    dtype=float,
                )
            )

            mse = float(
                mean_squared_error(
                    y_eval,
                    predictions,
                )
            )

            result.mae = float(
                mean_absolute_error(
                    y_eval,
                    predictions,
                )
            )

            result.mse = mse

            result.rmse = float(
                np.sqrt(
                    mse
                )
            )

            result.r2 = float(
                r2_score(
                    y_eval,
                    predictions,
                )
            )

            result.score = (
                result.r2
            )

            result.residuals = (
                residuals.tolist()
            )

        return result

    run = fit
