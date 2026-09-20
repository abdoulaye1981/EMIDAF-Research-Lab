"""
EMIDAF Framework
EAIE - Intelligent ML Engine
"""

from __future__ import annotations

import copy

import pandas as pd

from sklearn.base import clone
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .classification import ClassificationModels
from .comparison import ModelComparison
from .evaluation import ModelEvaluator
from .preparation import DataPreparation
from .problem import ProblemDetector
from .regression import RegressionModels


class EAIEEngine:
    """
    Moteur supervisé principal d'EMIDAF.

    Pipeline :
    inspection -> préparation -> split ->
    preprocessing dans pipeline -> entraînement ->
    validation -> évaluation -> comparaison.
    """

    def __init__(
        self,
        *,
        test_size: float = 0.20,
        random_state: int = 42,
        cv: int = 5,
    ):

        self.test_size = test_size
        self.random_state = random_state
        self.cv = cv

        self.task_ = None
        self.results_ = []
        self.comparison_ = None
        self.best_result_ = None
        self.baseline_cv_mean_ = None
        self.selection_metric_ = None

        # Contexte conservé pour EXAIE
        self.target_ = None
        self.feature_names_ = []

        self.X_train_ = None
        self.X_test_ = None
        self.y_train_ = None
        self.y_test_ = None

    def run(
        self,
        dataframe: pd.DataFrame,
        target: str,
        *,
        features: list[str] | None = None,
        task: str | None = None,
        models: list[str] | None = None,
    ):

        prepared = DataPreparation.prepare(
            dataframe,
            target,
            features=features,
        )

        detected_task = ProblemDetector.detect(
            prepared.y,
            task=task,
        )

        self.task_ = detected_task

        self.target_ = target
        self.feature_names_ = list(
            prepared.X.columns
        )

        stratify = None

        if detected_task == "classification":

            counts = prepared.y.value_counts()

            # Stratification seulement si chaque
            # classe possède au moins deux observations.
            if (
                len(counts) > 1
                and counts.min() >= 2
            ):
                stratify = prepared.y

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = train_test_split(
            prepared.X,
            prepared.y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=stratify,
        )

        # Conservation du split final pour EXAIE.
        self.X_train_ = X_train.copy()
        self.X_test_ = X_test.copy()
        self.y_train_ = y_train.copy()
        self.y_test_ = y_test.copy()

        preprocessor = (
            DataPreparation
            .build_preprocessor(
                prepared.numeric_features,
                prepared.categorical_features,
                scale_numeric=True,
            )
        )

        if detected_task == "classification":

            registry = (
                ClassificationModels.registry(
                    random_state=self.random_state
                )
            )

        else:

            registry = (
                RegressionModels.registry(
                    random_state=self.random_state
                )
            )

        if models is not None:

            unknown = [
                name
                for name in models
                if name not in registry
            ]

            if unknown:
                raise ValueError(
                    "Modèles inconnus : "
                    + ", ".join(unknown)
                )

            registry = {
                name: registry[name]
                for name in models
            }

        # ==================================================
        # BASELINE
        # ==================================================

        if detected_task == "classification":
            baseline_estimator = DummyClassifier(
                strategy="most_frequent"
            )
        else:
            baseline_estimator = DummyRegressor(
                strategy="mean"
            )

        baseline_pipeline = Pipeline(
            [
                (
                    "preprocessor",
                    clone(preprocessor),
                ),
                (
                    "model",
                    baseline_estimator,
                ),
            ]
        )

        try:
            baseline_validation = (
                ModelComparison.cross_validate(
                    baseline_pipeline,
                    prepared.X,
                    prepared.y,
                    task=detected_task,
                    cv=self.cv,
                )
            )

            self.baseline_cv_mean_ = (
                baseline_validation["cv_mean"]
            )

            self.selection_metric_ = (
                baseline_validation["cv_metric"]
            )

        except Exception:
            self.baseline_cv_mean_ = None

        results = []

        for name, estimator in registry.items():

            pipeline = Pipeline(
                [
                    (
                        "preprocessor",
                        clone(preprocessor),
                    ),
                    (
                        "model",
                        clone(estimator),
                    ),
                ]
            )

            pipeline.fit(
                X_train,
                y_train,
            )

            if detected_task == "classification":

                result = (
                    ModelEvaluator.classification(
                        estimator=pipeline,
                        X_test=X_test,
                        y_test=y_test,
                        model_name=name,
                        features=list(
                            prepared.X.columns
                        ),
                        target=target,
                        train_size=len(X_train),
                    )
                )

            else:

                result = (
                    ModelEvaluator.regression(
                        estimator=pipeline,
                        X_test=X_test,
                        y_test=y_test,
                        model_name=name,
                        features=list(
                            prepared.X.columns
                        ),
                        target=target,
                        train_size=len(X_train),
                    )
                )

            try:

                cv_result = (
                    ModelComparison.cross_validate(
                        pipeline,
                        prepared.X,
                        prepared.y,
                        task=detected_task,
                        cv=self.cv,
                    )
                )

                result.metadata.update(
                    cv_result
                )

            except Exception as exc:

                result.metadata[
                    "cv_error"
                ] = str(exc)

            results.append(result)

        self.results_ = results

        self.comparison_ = (
            ModelComparison.table(
                results
            )
        )

        if results:

            # Sélection du modèle uniquement sur la
            # validation croisée.
            valid_cv = [
                result
                for result in results
                if result.metadata.get(
                    "cv_mean"
                ) is not None
            ]

            if valid_cv:

                self.best_result_ = max(
                    valid_cv,
                    key=lambda item: (
                        item.metadata["cv_mean"]
                    ),
                )

            else:

                # Repli uniquement si la CV n'est
                # techniquement pas disponible.
                valid_score = [
                    result
                    for result in results
                    if result.score is not None
                ]

                if valid_score:

                    self.best_result_ = max(
                        valid_score,
                        key=lambda item: (
                            item.score
                        ),
                    )

        return self.results_

    def explainability_context(self):
        """
        Retourne le contexte scientifique nécessaire
        au module EXAIE.

        Le modèle retourné est celui sélectionné
        par EAIE sur la validation croisée.
        """

        if self.best_result_ is None:
            raise RuntimeError(
                "Aucun modèle EAIE sélectionné."
            )

        if self.X_test_ is None:
            raise RuntimeError(
                "Le jeu de test EAIE "
                "n'est pas disponible."
            )

        return {
            "estimator": self.best_result_.estimator,
            "model_name": self.best_result_.model_name,
            "task": self.task_,
            "target": self.target_,
            "features": list(
                self.feature_names_
            ),
            "X_train": self.X_train_.copy(),
            "X_test": self.X_test_.copy(),
            "y_train": self.y_train_.copy(),
            "y_test": self.y_test_.copy(),
            "cv_mean": (
                self.best_result_
                .metadata
                .get("cv_mean")
            ),
            "cv_std": (
                self.best_result_
                .metadata
                .get("cv_std")
            ),
            "test_score": self.best_result_.score,
        }

    def compare(self):

        if self.comparison_ is None:
            raise RuntimeError(
                "EAIE.run() doit être exécuté "
                "avant compare()."
            )

        return self.comparison_.copy()

    def best(self):

        if self.best_result_ is None:
            raise RuntimeError(
                "Aucun modèle évalué."
            )

        return self.best_result_

    def summary(self):

        best_model = None
        test_score = None
        cv_mean = None
        cv_std = None
        better_than_baseline = None
        interpretation = ""

        if self.best_result_ is not None:

            best_model = (
                self.best_result_.model_name
            )

            test_score = (
                self.best_result_.score
            )

            cv_mean = (
                self.best_result_
                .metadata
                .get("cv_mean")
            )

            cv_std = (
                self.best_result_
                .metadata
                .get("cv_std")
            )

            if (
                cv_mean is not None
                and self.baseline_cv_mean_
                is not None
            ):

                better_than_baseline = (
                    cv_mean
                    > self.baseline_cv_mean_
                )

            if self.task_ == "regression":

                if (
                    cv_mean is not None
                    and cv_mean <= 0
                ):
                    interpretation = (
                        "La performance moyenne en "
                        "validation croisée est nulle "
                        "ou négative. Le modèle ne "
                        "montre pas de capacité "
                        "prédictive convaincante par "
                        "rapport à une référence "
                        "simple."
                    )

                elif better_than_baseline:

                    interpretation = (
                        "Le modèle sélectionné dépasse "
                        "la baseline en validation "
                        "croisée. Sa performance doit "
                        "encore être interprétée avec "
                        "le score test et la stabilité "
                        "entre les folds."
                    )

                else:

                    interpretation = (
                        "Aucun avantage clair par "
                        "rapport à la baseline n'est "
                        "établi."
                    )

            elif self.task_ == "classification":

                if better_than_baseline is True:

                    interpretation = (
                        "Le modèle sélectionné dépasse "
                        "la baseline selon la moyenne "
                        "de validation croisée. Cette "
                        "supériorité ne suffit pas à "
                        "elle seule à établir une "
                        "performance satisfaisante : "
                        "il faut également examiner "
                        "la variabilité des folds, "
                        "les métriques par classe et "
                        "le jeu de test."
                    )

                elif better_than_baseline is False:

                    interpretation = (
                        "Le modèle sélectionné ne "
                        "dépasse pas la baseline en "
                        "validation croisée."
                    )

                else:

                    interpretation = (
                        "La comparaison à la baseline "
                        "n'a pas pu être établie."
                    )

        return {
            "task": self.task_,
            "models": len(self.results_),
            "selection_metric": (
                self.selection_metric_
            ),
            "best_model": best_model,
            "test_score": test_score,
            "cv_mean": cv_mean,
            "cv_std": cv_std,
            "baseline_cv_mean": (
                self.baseline_cv_mean_
            ),
            "better_than_baseline": (
                better_than_baseline
            ),
            "interpretation": interpretation,
        }



class EAIE:
    """
    Façade publique simplifiée.
    """

    @staticmethod
    def run(
        dataframe,
        target,
        **kwargs,
    ):

        engine_parameters = {}

        for key in (
            "test_size",
            "random_state",
            "cv",
        ):
            if key in kwargs:
                engine_parameters[key] = (
                    kwargs.pop(key)
                )

        engine = EAIEEngine(
            **engine_parameters
        )

        engine.run(
            dataframe,
            target,
            **kwargs,
        )

        return engine
