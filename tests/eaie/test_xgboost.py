"""
=========================================================
Tests EMIDAF - XGBoost
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from emidaf_core.common.results import ModelResult
from emidaf_core.eaie import XGBoostModel


def make_classification_dataframe():

    rng = np.random.default_rng(42)

    n = 240

    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)

    score = (
        1.6 * x1
        - 0.9 * x2
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
        4.5
        + 2.4 * x1
        - 1.5 * x2
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
        + 0.6 * x2
    )

    target = np.where(
        score < -0.5,
        0,
        np.where(
            score > 0.5,
            2,
            1,
        ),
    )

    return pd.DataFrame({
        "x1": x1,
        "x2": x2,
        "target": target,
    })


def test_xgboost_classification_result():

    df = make_classification_dataframe()

    result = XGBoostModel.fit(
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
        "XGBClassifier"
    )

    assert result.task == (
        "classification"
    )

    assert result.model_type == (
        "classifier"
    )

    assert result.library == (
        "xgboost"
    )


def test_xgboost_regression_result():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
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
        "XGBRegressor"
    )

    assert result.task == (
        "regression"
    )

    assert result.model_type == (
        "regressor"
    )


def test_xgboost_classification_metrics():

    df = make_classification_dataframe()

    result = XGBoostModel.fit(
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
    assert 0 <= result.precision <= 1
    assert 0 <= result.recall <= 1
    assert 0 <= result.f1_score <= 1
    assert 0 <= result.roc_auc <= 1

    assert result.log_loss >= 0

    assert result.score == (
        result.f1_score
    )


def test_xgboost_regression_metrics():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
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


def test_xgboost_feature_importance():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
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

    for value in (
        result.feature_importance.values()
    ):
        assert value >= 0


def test_xgboost_predictions_regression():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
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


def test_xgboost_probabilities():

    df = make_classification_dataframe()

    result = XGBoostModel.fit(
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
        atol=1e-6,
    )


def test_xgboost_confusion_matrix():

    df = make_classification_dataframe()

    result = XGBoostModel.fit(
        df,
        target="target",
        task="classification",
    )

    matrix = np.asarray(
        result.confusion_matrix
    )

    assert matrix.shape == (
        2,
        2,
    )

    assert matrix.sum() == len(
        df
    )


def test_xgboost_classification_report():

    df = make_classification_dataframe()

    result = XGBoostModel.fit(
        df,
        target="target",
        task="classification",
    )

    assert isinstance(
        result.classification_report,
        dict,
    )

    assert "accuracy" in (
        result.classification_report
    )


def test_xgboost_multiclass():

    df = make_multiclass_dataframe()

    result = XGBoostModel.fit(
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

    assert len(
        result.confusion_matrix
    ) == 3

    assert result.roc_auc is not None


def test_xgboost_explicit_features():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
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


def test_xgboost_test_dataframe_classification():

    df = make_classification_dataframe()

    train = df.iloc[:180].copy()
    test = df.iloc[180:].copy()

    result = XGBoostModel.fit(
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

    assert len(
        result.probabilities
    ) == 60


def test_xgboost_test_dataframe_regression():

    df = make_regression_dataframe()

    train = df.iloc[:180].copy()
    test = df.iloc[180:].copy()

    result = XGBoostModel.fit(
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


def test_xgboost_parameters():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
        df,
        target="target",
        task="regression",
        n_estimators=50,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.9,
        random_state=7,
    )

    assert result.parameters[
        "n_estimators"
    ] == 50

    assert result.parameters[
        "max_depth"
    ] == 4

    assert result.parameters[
        "learning_rate"
    ] == 0.05

    assert result.parameters[
        "subsample"
    ] == 0.8

    assert result.parameters[
        "colsample_bytree"
    ] == 0.9

    assert result.parameters[
        "random_state"
    ] == 7


def test_xgboost_metadata():

    df = make_regression_dataframe()

    result = XGBoostModel.fit(
        df,
        target="target",
        task="regression",
    )

    assert result.metadata[
        "boosting"
    ] is True

    assert result.metadata[
        "tree_based"
    ] is True

    assert result.metadata[
        "task"
    ] == "regression"


def test_xgboost_run_alias():

    df = make_regression_dataframe()

    result = XGBoostModel.run(
        df,
        target="target",
        task="regression",
    )

    assert isinstance(
        result,
        ModelResult,
    )

    assert result.fitted is True


def test_xgboost_requires_dataframe():

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        XGBoostModel.fit(
            [],
            target="target",
            task="regression",
        )


def test_xgboost_empty_dataframe():

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        XGBoostModel.fit(
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
def test_xgboost_invalid_task(
    task,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="task",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task=task,
        )


def test_xgboost_missing_target():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        XGBoostModel.fit(
            df,
            target="unknown",
            task="regression",
        )


def test_xgboost_missing_feature():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="absentes",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "unknown",
            ],
        )


def test_xgboost_target_as_feature():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="cible",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "target",
            ],
        )


def test_xgboost_duplicate_features():

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="doublons",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            features=[
                "x1",
                "x1",
            ],
        )


def test_xgboost_missing_values():

    df = make_regression_dataframe()

    df.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_xgboost_non_numeric_feature():

    df = make_regression_dataframe()

    df[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_xgboost_non_numeric_regression_target():

    df = make_regression_dataframe()

    df[
        "target"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numérique",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
        )


def test_xgboost_single_class():

    df = make_classification_dataframe()

    df[
        "target"
    ] = 1

    with pytest.raises(
        ValueError,
        match="deux classes",
    ):

        XGBoostModel.fit(
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
def test_xgboost_invalid_estimators(
    value,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="n_estimators",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            n_estimators=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        "invalid",
    ],
)
def test_xgboost_invalid_max_depth(
    value,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="max_depth",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            max_depth=value,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -0.1,
        "invalid",
    ],
)
def test_xgboost_invalid_learning_rate(
    value,
):

    df = make_regression_dataframe()

    with pytest.raises(
        ValueError,
        match="learning_rate",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            learning_rate=value,
        )


@pytest.mark.parametrize(
    "name,value",
    [
        (
            "subsample",
            0,
        ),
        (
            "subsample",
            1.1,
        ),
        (
            "colsample_bytree",
            0,
        ),
        (
            "colsample_bytree",
            1.1,
        ),
    ],
)
def test_xgboost_invalid_sampling(
    name,
    value,
):

    df = make_regression_dataframe()

    parameters = {
        name: value,
    }

    with pytest.raises(
        ValueError,
        match=name,
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            **parameters,
        )


def test_xgboost_invalid_test_dataframe():

    df = make_regression_dataframe()

    with pytest.raises(
        TypeError,
        match="test_dataframe",
    ):

        XGBoostModel.fit(
            df,
            target="target",
            task="regression",
            test_dataframe=[],
        )
