"""
=========================================================
Tests EMIDAF - SHAP Explainer
=========================================================
"""

import numpy as np
import pandas as pd
import pytest

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

from xgboost import XGBClassifier

from emidaf_core.common.results import (
    ShapResult,
)
from emidaf_core.exaie import (
    ShapExplainer,
)


def make_regression_data():

    rng = np.random.default_rng(42)

    n = 120

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

    y = (
        3
        + 2.5 * x1
        - 1.2 * x2
        + rng.normal(
            0,
            0.4,
            n,
        )
    )

    X = pd.DataFrame({
        "x1": x1,
        "x2": x2,
    })

    return X, y


def make_classification_data():

    rng = np.random.default_rng(123)

    n = 140

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

    y = (
        x1
        - 0.7 * x2
        + rng.normal(
            0,
            0.5,
            n,
        )
        > 0
    ).astype(int)

    X = pd.DataFrame({
        "x1": x1,
        "x2": x2,
    })

    return X, y


def test_shap_random_forest_regression():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=30,
        random_state=42,
        n_jobs=1,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        task="regression",
        max_samples=40,
    )

    assert isinstance(
        result,
        ShapResult,
    )

    assert result.success is True

    assert result.model_name == (
        "RandomForestRegressor"
    )

    assert result.explainer_type == (
        "TreeExplainer"
    )

    assert result.task == (
        "regression"
    )

    assert result.n_observations == 40


def test_shap_random_forest_classification():

    X, y = make_classification_data()

    model = RandomForestClassifier(
        n_estimators=30,
        random_state=42,
        n_jobs=1,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        task="classification",
        max_samples=30,
    )

    assert isinstance(
        result,
        ShapResult,
    )

    assert result.task == (
        "classification"
    )

    assert result.n_observations == 30


def test_shap_xgboost_classification():

    X, y = make_classification_data()

    model = XGBClassifier(
        n_estimators=30,
        max_depth=3,
        random_state=42,
        n_jobs=1,
        eval_metric="logloss",
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        task="classification",
        max_samples=35,
    )

    assert isinstance(
        result,
        ShapResult,
    )

    assert result.model_name == (
        "XGBClassifier"
    )

    assert result.explainer_type == (
        "TreeExplainer"
    )

    assert result.n_observations == 35


def test_shap_feature_names():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=25,
    )

    assert result.features == [
        "x1",
        "x2",
    ]


def test_shap_global_importance():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=30,
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


def test_shap_values_dimensions():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=20,
    )

    values = np.asarray(
        result.shap_values
    )

    assert values.shape[0] == 20

    assert values.shape[1] == 2


def test_shap_local_explanations():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=15,
    )

    assert len(
        result.local_explanations
    ) == 15

    first = (
        result.local_explanations[
            0
        ]
    )

    assert first[
        "row"
    ] == 0

    assert "contributions" in first

    assert set(
        first[
            "contributions"
        ]
    ) == {
        "x1",
        "x2",
    }


def test_shap_base_values():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=10,
    )

    assert result.base_values is not None

    assert len(
        result.base_values
    ) > 0


def test_shap_metadata():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=10,
    )

    assert result.metadata[
        "method"
    ] == "SHAP"

    assert result.metadata[
        "global_explanation"
    ] is True

    assert result.metadata[
        "local_explanation"
    ] is True

    assert result.metadata[
        "max_samples"
    ] == 10


def test_shap_summary():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        task="regression",
        max_samples=10,
    )

    summary = result.summary()

    assert summary[
        "Model"
    ] == (
        "RandomForestRegressor"
    )

    assert summary[
        "Explainer"
    ] == (
        "TreeExplainer"
    )

    assert summary[
        "Observations"
    ] == 10


def test_shap_run_alias():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=20,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.run(
        model,
        X,
        max_samples=10,
    )

    assert isinstance(
        result,
        ShapResult,
    )


def test_shap_pipeline():

    X, y = make_regression_data()

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "model",
            LinearRegression(),
        ),
    ])

    pipeline.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        pipeline,
        X,
        task="regression",
        max_samples=20,
    )

    assert isinstance(
        result,
        ShapResult,
    )

    assert result.model_name == (
        "LinearRegression"
    )

    assert len(
        result.features
    ) == 2


def test_shap_pipeline_with_categorical_features():

    rng = np.random.default_rng(2026)

    n = 80

    X = pd.DataFrame({
        "age": rng.integers(
            22,
            60,
            n,
        ),
        "experience": rng.normal(
            10,
            4,
            n,
        ),
        "service": rng.choice(
            [
                "IT",
                "Finance",
                "RH",
            ],
            size=n,
        ),
    })

    service_effect = (
        X["service"]
        .map({
            "IT": 120_000,
            "Finance": 80_000,
            "RH": 40_000,
        })
        .astype(float)
    )

    y = (
        500_000
        + 15_000 * X["age"]
        + 25_000 * X["experience"]
        + service_effect
        + rng.normal(
            0,
            20_000,
            n,
        )
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                [
                    "age",
                    "experience",
                ],
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
                [
                    "service",
                ],
            ),
        ],
    )

    pipeline = Pipeline([
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            Ridge(
                alpha=1.0,
            ),
        ),
    ])

    pipeline.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        pipeline,
        X,
        task="regression",
        max_samples=20,
    )

    assert isinstance(
        result,
        ShapResult,
    )

    assert result.model_name == "Ridge"

    assert result.n_observations == 20

    transformed = (
        pipeline[:-1]
        .transform(
            X.iloc[:20]
        )
    )

    assert len(
        result.features
    ) == transformed.shape[1]

    assert any(
        "service" in feature
        for feature in result.features
    )

    assert set(
        result.feature_importance
    ) == set(
        result.features
    )

    assert len(
        result.local_explanations
    ) == 20

    first_local = (
        result.local_explanations[0]
    )

    assert "contributions" in first_local

    assert set(
        first_local["contributions"]
    ) == set(
        result.features
    )


def test_shap_requires_dataframe():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    with pytest.raises(
        TypeError,
        match="DataFrame",
    ):

        ShapExplainer.explain(
            model,
            X.to_numpy(),
        )


def test_shap_empty_dataframe():

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    with pytest.raises(
        ValueError,
        match="vide",
    ):

        ShapExplainer.explain(
            model,
            pd.DataFrame(),
        )


def test_shap_missing_values():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    X_bad = X.copy()

    X_bad.loc[
        0,
        "x1",
    ] = np.nan

    with pytest.raises(
        ValueError,
        match="valeurs manquantes",
    ):

        ShapExplainer.explain(
            model,
            X_bad,
        )


def test_shap_non_numeric_feature():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    X_bad = X.copy()

    X_bad[
        "category"
    ] = "A"

    with pytest.raises(
        ValueError,
        match="numériques",
    ):

        ShapExplainer.explain(
            model,
            X_bad,
        )


def test_shap_infinite_values():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    X_bad = X.copy()

    X_bad.loc[
        0,
        "x1",
    ] = np.inf

    with pytest.raises(
        ValueError,
        match="finies",
    ):

        ShapExplainer.explain(
            model,
            X_bad,
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        "invalid",
    ],
)
def test_shap_invalid_max_samples(
    value,
):

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    with pytest.raises(
        ValueError,
        match="max_samples",
    ):

        ShapExplainer.explain(
            model,
            X,
            max_samples=value,
        )


def test_shap_max_samples_above_dataset():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=500,
    )

    assert result.n_observations == len(
        X
    )


def test_shap_result_execution_time():

    X, y = make_regression_data()

    model = RandomForestRegressor(
        n_estimators=10,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    result = ShapExplainer.explain(
        model,
        X,
        max_samples=10,
    )

    assert result.execution_time >= 0
