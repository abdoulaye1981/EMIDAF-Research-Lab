"""
EMIDAF Framework
EAIE - Model Evaluation
"""

from __future__ import annotations

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
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

from emidaf_core.common.results import ModelResult


class ModelEvaluator:

    @staticmethod
    def classification(
        *,
        estimator,
        X_test,
        y_test,
        model_name: str,
        features: list[str],
        target: str,
        train_size: int,
        positive_label=1,
    ) -> ModelResult:

        predictions = estimator.predict(
            X_test
        )

        result = ModelResult(
            name=model_name,
            model_name=model_name,
            algorithm=type(
                estimator
            ).__name__,
            model_type="classifier",
            task="classification",
            library="scikit-learn",
            fitted=True,
            train_size=train_size,
            test_size=len(y_test),
            features=list(features),
            target=target,
            estimator=estimator,
        )

        result.accuracy = float(
            accuracy_score(
                y_test,
                predictions,
            )
        )

        result.precision = float(
            precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        result.recall = float(
            recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        result.f1_score = float(
            f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
        )

        # Score principal EAIE v1 :
        # F1 pondéré, plus robuste que l'accuracy
        # seule en cas de classes déséquilibrées.
        result.score = result.f1_score


        # -------------------------------------------------
        # Métriques de la classe positive
        # -------------------------------------------------

        observed_classes = np.unique(
            y_test
        )

        if (
            len(observed_classes) == 2
            and positive_label in observed_classes
        ):

            result.positive_label = (
                positive_label
            )

            result.precision_positive = float(
                precision_score(
                    y_test,
                    predictions,
                    pos_label=positive_label,
                    average="binary",
                    zero_division=0,
                )
            )

            result.recall_positive = float(
                recall_score(
                    y_test,
                    predictions,
                    pos_label=positive_label,
                    average="binary",
                    zero_division=0,
                )
            )

            result.f1_positive = float(
                f1_score(
                    y_test,
                    predictions,
                    pos_label=positive_label,
                    average="binary",
                    zero_division=0,
                )
            )

        result.predictions = (
            np.asarray(predictions)
            .tolist()
        )

        result.confusion_matrix = (
            confusion_matrix(
                y_test,
                predictions,
            )
            .tolist()
        )

        result.classification_report = (
            classification_report(
                y_test,
                predictions,
                output_dict=True,
                zero_division=0,
            )
        )

        if hasattr(
            estimator,
            "predict_proba",
        ):

            try:
                probabilities = (
                    estimator.predict_proba(
                        X_test
                    )
                )

                result.probabilities = (
                    np.asarray(
                        probabilities
                    ).tolist()
                )

                classes = np.unique(
                    y_test
                )

                if len(classes) == 2:

                    estimator_classes = list(
                        getattr(
                            estimator,
                            "classes_",
                            classes,
                        )
                    )

                    if (
                        positive_label
                        in estimator_classes
                    ):

                        positive_index = (
                            estimator_classes.index(
                                positive_label
                            )
                        )

                        positive_probabilities = (
                            probabilities[
                                :,
                                positive_index
                            ]
                        )

                        binary_target = (
                            np.asarray(y_test)
                            == positive_label
                        ).astype(int)

                        result.roc_auc = float(
                            roc_auc_score(
                                binary_target,
                                positive_probabilities,
                            )
                        )

                        result.pr_auc = float(
                            average_precision_score(
                                binary_target,
                                positive_probabilities,
                            )
                        )

                elif len(classes) > 2:

                    result.roc_auc = float(
                        roc_auc_score(
                            y_test,
                            probabilities,
                            multi_class="ovr",
                            average="weighted",
                        )
                    )

                try:
                    estimator_classes = list(
                        getattr(
                            estimator,
                            "classes_",
                            np.unique(y_test),
                        )
                    )

                    ordered_classes = sorted(
                        estimator_classes
                    )

                    if (
                        estimator_classes
                        != ordered_classes
                    ):

                        column_order = [
                            estimator_classes.index(
                                label
                            )
                            for label
                            in ordered_classes
                        ]

                        log_loss_probabilities = (
                            probabilities[
                                :,
                                column_order
                            ]
                        )

                    else:

                        log_loss_probabilities = (
                            probabilities
                        )

                    result.log_loss = float(
                        log_loss(
                            y_test,
                            log_loss_probabilities,
                            labels=ordered_classes,
                        )
                    )
                except Exception:
                    pass

            except Exception:
                pass

        return result

    @staticmethod
    def regression(
        *,
        estimator,
        X_test,
        y_test,
        model_name: str,
        features: list[str],
        target: str,
        train_size: int,
    ) -> ModelResult:

        predictions = estimator.predict(
            X_test
        )

        residuals = (
            np.asarray(y_test)
            - np.asarray(predictions)
        )

        mse = mean_squared_error(
            y_test,
            predictions,
        )

        result = ModelResult(
            name=model_name,
            model_name=model_name,
            algorithm=type(
                estimator
            ).__name__,
            model_type="regressor",
            task="regression",
            library="scikit-learn",
            fitted=True,
            train_size=train_size,
            test_size=len(y_test),
            features=list(features),
            target=target,
            estimator=estimator,
        )

        result.mae = float(
            mean_absolute_error(
                y_test,
                predictions,
            )
        )

        result.mse = float(mse)

        result.rmse = float(
            np.sqrt(mse)
        )

        result.r2 = float(
            r2_score(
                y_test,
                predictions,
            )
        )

        result.score = result.r2

        result.predictions = (
            np.asarray(predictions)
            .tolist()
        )

        result.residuals = (
            residuals.tolist()
        )

        return result
