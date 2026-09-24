"""
=========================================================
Tests EMIDAF - Logistic Regression
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import (
    LogisticResult,
)
from emidaf_core.eaie import (
    LogisticRegressionModel,
)


def make_binary_dataframe():

    rng = np.random.default_rng(42)

    n = 200

    x1 = rng.normal(
        0,
        1,
        n,
    )

    x2 = rng.normal(
        0,
        1,
        n,
    )

    linear = (
        1.7 * x1
        - 1.1 * x2
        + rng.normal(
            0,
            0.7,
            n,
        )
    )

    y = (
        linear > 0
    ).astype(int)

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "target": y,
    })


def make_string_target_dataframe():

    dataframe = (
        make_binary_dataframe()
    )

    dataframe[
        "target"
    ] = dataframe[
        "target"
    ].map({
        0: "Echec",
        1: "Reussite",
    })

    return dataframe


def make_multiclass_dataframe():

    rng = np.random.default_rng(123)

    n = 240

    x1 = rng.normal(
        0,
        1,
        n,
    )

    x2 = rng.normal(
        0,
        1,
        n,
    )

    score = (
        x1
        + 0.6 * x2
    )

    target = np.where(
        score < -0.5,
        "A",
        np.where(
            score > 0.5,
            "C",
            "B",
        ),
    )

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "target": target,
    })


def test_logistic_returns_result():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert isinstance(
        result,
        LogisticResult,
    )

    assert result.fitted is True
    assert result.success is True

    assert result.task == (
        "classification"
    )

    assert result.algorithm == (
        "LogisticRegression"
    )

    assert result.library == (
        "scikit-learn"
    )


def test_logistic_model_information():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.model_name == (
        "Logistic Regression"
    )

    assert result.model_type == (
        "classifier"
    )

    assert result.target == (
        "target"
    )

    assert result.features == [
        "x1",
        "x2",
    ]

    assert result.train_size == 200

    assert result.test_size == 0


def test_logistic_binary_classes():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.is_binary is True

    assert result.n_classes == 2

    assert result.classes == [
        0,
        1,
    ]

    assert result.threshold == 0.5


def test_logistic_binary_metrics():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.accuracy is not None
    assert result.precision is not None
    assert result.recall is not None
    assert result.f1_score is not None
    assert result.roc_auc is not None
    assert result.log_loss is not None

    assert 0 <= result.accuracy <= 1
    assert 0 <= result.precision <= 1
    assert 0 <= result.recall <= 1
    assert 0 <= result.f1_score <= 1
    assert 0 <= result.roc_auc <= 1

    assert result.log_loss >= 0

    assert result.score == (
        result.f1_score
    )


def test_logistic_coefficients():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert "x1" in (
        result.coefficients
    )

    assert "x2" in (
        result.coefficients
    )

    assert result.intercept is not None


def test_logistic_odds_ratios():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert "x1" in (
        result.odds_ratios
    )

    assert "x2" in (
        result.odds_ratios
    )

    assert (
        result.odds_ratios[
            "x1"
        ]
        > 0
    )

    assert (
        result.odds_ratios[
            "x2"
        ]
        > 0
    )


def test_logistic_predictions():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert len(
        result.predictions
    ) == len(
        dataframe
    )

    assert set(
        result.predictions
    ).issubset({
        0,
        1,
    })


def test_logistic_probabilities():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    probabilities = np.asarray(
        result.probabilities
    )

    assert probabilities.shape == (
        len(dataframe),
        2,
    )

    assert np.all(
        probabilities >= 0
    )

    assert np.all(
        probabilities <= 1
    )

    assert np.allclose(
        probabilities.sum(
            axis=1
        ),
        1.0,
    )


def test_logistic_confusion_matrix():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    matrix = np.asarray(
        result.confusion_matrix
    )

    assert matrix.shape == (
        2,
        2,
    )

    assert matrix.sum() == len(
        dataframe
    )


def test_logistic_classification_report():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert isinstance(
        result.classification_report,
        dict,
    )

    assert "accuracy" in (
        result.classification_report
    )


def test_logistic_string_target():

    dataframe = (
        make_string_target_dataframe()
    )

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.n_classes == 2

    assert set(
        result.classes
    ) == {
        "Echec",
        "Reussite",
    }

    assert set(
        result.predictions
    ).issubset({
        "Echec",
        "Reussite",
    })


def test_logistic_multiclass():

    dataframe = (
        make_multiclass_dataframe()
    )

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.is_binary is False

    assert result.n_classes == 3

    assert set(
        result.classes
    ) == {
        "A",
        "B",
        "C",
    }

    assert result.threshold is None

    assert isinstance(
        result.coefficients,
        dict,
    )

    assert set(
        result.coefficients.keys()
    ) == {
        "A",
        "B",
        "C",
    }


def test_logistic_multiclass_probabilities():

    dataframe = (
        make_multiclass_dataframe()
    )

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    probabilities = np.asarray(
        result.probabilities
    )

    assert probabilities.shape == (
        len(dataframe),
        3,
    )

    assert np.allclose(
        probabilities.sum(
            axis=1
        ),
        1.0,
    )


def test_logistic_explicit_features():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            features=[
                "x1",
            ],
        )
    )

    assert result.features == [
        "x1",
    ]

    assert "x1" in (
        result.coefficients
    )

    assert "x2" not in (
        result.coefficients
    )


def test_logistic_custom_threshold():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            threshold=0.7,
        )
    )

    assert result.threshold == 0.7

    probabilities = np.asarray(
        result.probabilities
    )

    expected = np.where(
        probabilities[:, 1] >= 0.7,
        result.classes[1],
        result.classes[0],
    )

    assert result.predictions == (
        expected.tolist()
    )


def test_logistic_test_dataframe():

    dataframe = make_binary_dataframe()

    train = dataframe.iloc[
        :150
    ].copy()

    test = dataframe.iloc[
        150:
    ].copy()

    result = (
        LogisticRegressionModel.fit(
            train,
            target="target",
            test_dataframe=test,
        )
    )

    assert result.train_size == 150

    assert result.test_size == 50

    assert len(
        result.predictions
    ) == 50

    assert len(
        result.probabilities
    ) == 50


def test_logistic_parameters():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            C=0.5,
            max_iter=1000,
            random_state=7,
        )
    )

    assert result.parameters[
        "C"
    ] == 0.5

    assert result.parameters[
        "max_iter"
    ] == 1000

    assert result.parameters[
        "random_state"
    ] == 7


def test_logistic_metadata():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    assert result.metadata[
        "classification"
    ] is True

    assert result.metadata[
        "probabilistic_model"
    ] is True

    assert result.metadata[
        "binary"
    ] is True

    assert result.metadata[
        "multiclass"
    ] is False


def test_logistic_summary():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )
    )

    summary = result.summary()

    assert summary[
        "Model"
    ] == "Logistic Regression"

    assert "Accuracy" in summary
    assert "Precision" in summary
    assert "Recall" in summary
    assert "F1" in summary
    assert "ROC-AUC" in summary
    assert "Log-loss" in summary


def test_logistic_run_alias():

    dataframe = make_binary_dataframe()

    result = (
        LogisticRegressionModel.run(
            dataframe,
            target="target",
        )
    )

    assert isinstance(
        result,
        LogisticResult,
    )

    assert result.fitted is True


def test_logistic_requires_dataframe():

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        LogisticRegressionModel.fit(
            [
                [1, 2],
                [3, 4],
            ],
            target="target",
        )


def test_logistic_empty_dataframe():

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        LogisticRegressionModel.fit(
            pd.DataFrame(),
            target="target",
        )


def test_logistic_missing_target():

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="unknown",
        )


def test_logistic_missing_feature():

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="absentes",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            features=[
                "x1",
                "unknown",
            ],
        )


def test_logistic_target_cannot_be_feature():

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            features=[
                "x1",
                "target",
            ],
        )


def test_logistic_duplicate_features():

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="doublons",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            features=[
                "x1",
                "x1",
            ],
        )


def test_logistic_rejects_missing_values():

    dataframe = make_binary_dataframe()

    dataframe.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )


def test_logistic_rejects_non_numeric_features():

    dataframe = make_binary_dataframe()

    dataframe[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )


def test_logistic_rejects_infinite_values():

    dataframe = make_binary_dataframe()

    dataframe.loc[
        0,
        "x1",
    ] = np.inf

    with pytest.raises(
        ValueError,
        match="finies",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )


def test_logistic_requires_two_classes():

    dataframe = make_binary_dataframe()

    dataframe[
        "target"
    ] = 1

    with pytest.raises(
        ValueError,
        match="deux classes",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
        )


@pytest.mark.parametrize(
    "threshold",
    [
        0,
        1,
        -0.1,
        1.1,
        "invalid",
    ],
)
def test_logistic_invalid_threshold(
    threshold,
):

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="threshold",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            threshold=threshold,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        "invalid",
    ],
)
def test_logistic_invalid_c(
    value,
):

    dataframe = make_binary_dataframe()

    with pytest.raises(
        ValueError,
        match="C",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            C=value,
        )


def test_logistic_invalid_test_dataframe_type():

    dataframe = make_binary_dataframe()

    with pytest.raises(
        TypeError,
        match="test_dataframe",
    ):

        LogisticRegressionModel.fit(
            dataframe,
            target="target",
            test_dataframe=[],
        )


def test_logistic_test_dataframe_missing_column():

    dataframe = make_binary_dataframe()

    train = dataframe.iloc[
        :150
    ].copy()

    test = dataframe.iloc[
        150:
    ].copy()

    test = test.drop(
        columns=[
            "x2",
        ]
    )

    with pytest.raises(
        ValueError,
        match="test_dataframe",
    ):

        LogisticRegressionModel.fit(
            train,
            target="target",
            test_dataframe=test,
        )
