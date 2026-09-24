"""
=========================================================
Tests EMIDAF - Random Forest
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import ModelResult
from emidaf_core.eaie import RandomForestModel


def make_classification_dataframe():

    rng = np.random.default_rng(42)

    n = 240

    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)

    score = (
        1.5 * x1
        - 0.8 * x2
        + rng.normal(
            0,
            0.8,
            n,
        )
    )

    target = (
        score > 0
    ).astype(int)

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "target": target,
    })


def make_regression_dataframe():

    rng = np.random.default_rng(123)

    n = 240

    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)

    target = (
        5
        + 2.3 * x1
        - 1.7 * x2
        + rng.normal(
            0,
            0.5,
            n,
        )
    )

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "target": target,
    })


def make_multiclass_dataframe():

    rng = np.random.default_rng(77)

    n = 240

    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)

    score = (
        x1
        + 0.5 * x2
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


def test_random_forest_classification_result():

    df = make_classification_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="classification",
    )

    assert isinstance(
        result,
        ModelResult,
    )

    assert result.fitted is True
    assert result.success is True

    assert result.algorithm == (
        "RandomForestClassifier"
    )

    assert result.task == (
        "classification"
    )

    assert result.model_type == (
        "classifier"
    )


def test_random_forest_regression_result():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert isinstance(
        result,
        ModelResult,
    )

    assert result.fitted is True

    assert result.algorithm == (
        "RandomForestRegressor"
    )

    assert result.task == (
        "regression"
    )

    assert result.model_type == (
        "regressor"
    )


def test_random_forest_classification_metrics():

    df = make_classification_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="classification",
    )

    assert result.accuracy is not None
    assert result.precision is not None
    assert result.recall is not None
    assert result.f1_score is not None
    assert result.roc_auc is not None
    assert result.log_loss is not None

    assert 0 <= result.accuracy <= 1
    assert 0 <= result.f1_score <= 1

    assert result.score == (
        result.f1_score
    )


def test_random_forest_regression_metrics():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert result.mae is not None
    assert result.mse is not None
    assert result.rmse is not None
    assert result.r2 is not None

    assert result.mae >= 0
    assert result.mse >= 0
    assert result.rmse >= 0

    assert result.score == (
        result.r2
    )


def test_random_forest_feature_importance():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert set(
        result.feature_importance
    ) == {
        "x1",
        "x2",
    }

    total = sum(
        result.feature_importance.values()
    )

    assert total == pytest.approx(
        1.0,
        abs=1e-8,
    )


def test_random_forest_predictions():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert len(
        result.predictions
    ) == len(df)

    assert len(
        result.residuals
    ) == len(df)


def test_random_forest_probabilities():

    df = make_classification_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="classification",
    )

    probabilities = np.asarray(
        result.probabilities
    )

    assert probabilities.shape == (
        len(df),
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


def test_random_forest_multiclass():

    df = make_multiclass_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="classification",
    )

    probabilities = np.asarray(
        result.probabilities
    )

    assert probabilities.shape == (
        len(df),
        3,
    )

    assert result.confusion_matrix

    assert result.classification_report


def test_random_forest_test_dataframe_classification():

    df = make_classification_dataframe()

    train = df.iloc[:180].copy()
    test = df.iloc[180:].copy()

    result = RandomForestModel.fit(
        train,
        target="target",
        task="classification",
        test_dataframe=test,
    )

    assert result.train_size == 180
    assert result.test_size == 60

    assert len(
        result.predictions
    ) == 60


def test_random_forest_test_dataframe_regression():

    df = make_regression_dataframe()

    train = df.iloc[:180].copy()
    test = df.iloc[180:].copy()

    result = RandomForestModel.fit(
        train,
        target="target",
        task="regression",
        test_dataframe=test,
    )

    assert result.train_size == 180
    assert result.test_size == 60

    assert len(
        result.predictions
    ) == 60

    assert len(
        result.residuals
    ) == 60


def test_random_forest_parameters():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
        n_estimators=50,
        max_depth=5,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=7,
    )

    assert result.parameters[
        "n_estimators"
    ] == 50

    assert result.parameters[
        "max_depth"
    ] == 5

    assert result.parameters[
        "min_samples_split"
    ] == 4

    assert result.parameters[
        "min_samples_leaf"
    ] == 2

    assert result.parameters[
        "random_state"
    ] == 7


def test_random_forest_explicit_features():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
        features=[
            "x1",
        ],
    )

    assert result.features == [
        "x1",
    ]

    assert set(
        result.feature_importance
    ) == {
        "x1",
    }


def test_random_forest_string_classes():

    df = make_classification_dataframe()

    df[
        "target"
    ] = df[
        "target"
    ].map({
        0: "No",
        1: "Yes",
    })

    result = RandomForestModel.fit(
        df,
        target="target",
        task="classification",
    )

    assert set(
        result.predictions
    ).issubset({
        "No",
        "Yes",
    })


def test_random_forest_metadata():

    df = make_regression_dataframe()

    result = RandomForestModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert result.metadata[
        "ensemble"
    ] is True

    assert result.metadata[
        "tree_based"
    ] is True

    assert result.metadata[
        "task"
    ] == "regression"


def test_random_forest_run_alias():

    df = make_regression_dataframe()

    result = RandomForestModel.run(
        df,
        target="target",
        task="regression",
    )

    assert isinstance(
        result,
        ModelResult,
    )

    assert result.fitted is True


def test_random_forest_requires_dataframe():

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        RandomForestModel.fit(
            [],
            target="target",
            task="regression",
        )


def test_random_forest_empty_dataframe():

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        RandomForestModel.fit(
            pd.DataFrame(),
            target="target",
            task="regression",
        )


@pytest.mark.parametrize(
    "task",
    [
        "unknown",
        "",
        "classificationx",
    ],
)
def test_random_forest_invalid_task(
    task,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="task",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task=task,
        )


def test_random_forest_missing_target():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        RandomForestModel.fit(
            df,
            target="unknown",
            task="regression",
        )


def test_random_forest_missing_feature():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="absentes",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "unknown",
            ],
        )


def test_random_forest_target_as_feature():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "target",
            ],
        )


def test_random_forest_duplicate_features():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="doublons",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "x1",
            ],
        )


def test_random_forest_missing_values():

    df = make_regression_dataframe()

    df.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_random_forest_non_numeric_feature():

    df = make_regression_dataframe()

    df[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_random_forest_non_numeric_regression_target():

    df = make_regression_dataframe()

    df[
        "target"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numérique",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_random_forest_single_class():

    df = make_classification_dataframe()

    df[
        "target"
    ] = 1

    with pytest.raises(
        ValueError,
        match="deux classes",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="classification",
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        "invalid",
    ],
)
def test_random_forest_invalid_estimators(
    value,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="n_estimators",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            n_estimators=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -2,
        "invalid",
    ],
)
def test_random_forest_invalid_max_depth(
    value,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="max_depth",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            max_depth=value,
        )


def test_random_forest_invalid_test_dataframe():

    df = make_regression_dataframe()

    with pytest.raises(
        TypeError,
        match="test_dataframe",
    ):

        RandomForestModel.fit(
            df,
            target="target",
            task="regression",
            test_dataframe=[],
        )
