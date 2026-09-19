"""
EMIDAF Framework
EAIE - Model Evaluation
"""

from __future__ import annotations

import numpy as np

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

                    result.roc_auc = float(
                        roc_auc_score(
                            y_test,
                            probabilities[:, 1],
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
                    result.log_loss = float(
                        log_loss(
                            y_test,
                            probabilities,
                            labels=getattr(
                                estimator,
                                "classes_",
                                None,
                            ),
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
