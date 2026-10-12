import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression

from emidaf_core.eaie.evaluation import (
    ModelEvaluator,
)


def test_binary_positive_class_metrics():

    X_train = pd.DataFrame(
        {
            "x": [
                -3, -2, -1,
                1, 2, 3,
            ]
        }
    )

    y_train = pd.Series(
        [
            0, 0, 0,
            1, 1, 1,
        ]
    )

    X_test = pd.DataFrame(
        {
            "x": [
                -2.5,
                -0.5,
                0.5,
                2.5,
            ]
        }
    )

    y_test = pd.Series(
        [
            0,
            0,
            1,
            1,
        ]
    )

    estimator = LogisticRegression(
        random_state=42
    )

    estimator.fit(
        X_train,
        y_train,
    )

    result = (
        ModelEvaluator.classification(
            estimator=estimator,
            X_test=X_test,
            y_test=y_test,
            model_name="logistic",
            features=["x"],
            target="target",
            train_size=len(X_train),
            positive_label=1,
        )
    )

    assert result.positive_label == 1

    assert (
        result.precision_positive
        is not None
    )

    assert (
        result.recall_positive
        is not None
    )

    assert (
        result.f1_positive
        is not None
    )

    assert result.roc_auc is not None
    assert result.pr_auc is not None

    assert (
        0 <= result.precision_positive <= 1
    )

    assert (
        0 <= result.recall_positive <= 1
    )

    assert (
        0 <= result.f1_positive <= 1
    )

    assert 0 <= result.roc_auc <= 1
    assert 0 <= result.pr_auc <= 1


def test_positive_probability_column_is_resolved_by_label():

    class ReversedProbabilityEstimator:

        classes_ = np.array(
            [1, 0]
        )

        def predict(self, X):
            return np.array(
                [1, 0, 1, 0]
            )

        def predict_proba(self, X):

            # Colonne 0 = classe 1
            # Colonne 1 = classe 0
            return np.array(
                [
                    [0.90, 0.10],
                    [0.20, 0.80],
                    [0.80, 0.20],
                    [0.10, 0.90],
                ]
            )

    X_test = pd.DataFrame(
        {
            "x": [
                1, 2, 3, 4,
            ]
        }
    )

    y_test = pd.Series(
        [
            1, 0, 1, 0,
        ]
    )

    result = (
        ModelEvaluator.classification(
            estimator=(
                ReversedProbabilityEstimator()
            ),
            X_test=X_test,
            y_test=y_test,
            model_name="dummy",
            features=["x"],
            target="target",
            train_size=10,
            positive_label=1,
        )
    )

    assert np.isclose(
        result.roc_auc,
        1.0,
    )

    assert np.isclose(
        result.pr_auc,
        1.0,
    )
