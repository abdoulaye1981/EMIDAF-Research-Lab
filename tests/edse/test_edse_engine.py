import pandas as pd

from sklearn.datasets import (
    make_classification,
    make_regression,
)

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
)

from emidaf_core.edse import EDSEEngine


def test_regression_profiles():

    X_array, y = make_regression(
        n_samples=100,
        n_features=4,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=[
            "x1",
            "x2",
            "x3",
            "x4",
        ],
    )

    model = LinearRegression()
    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="regression",
        cv_mean=0.90,
        test_score=0.90,
    )

    profiles = engine.profiles()

    assert len(profiles) == 100
    assert "prediction" in profiles.columns


def test_regression_scenario():

    X_array, y = make_regression(
        n_samples=100,
        n_features=3,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=[
            "x1",
            "x2",
            "x3",
        ],
    )

    model = LinearRegression()
    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="regression",
    )

    result = engine.scenario(
        threshold=0.0,
        direction="above",
    )

    assert "summary" in result
    assert "table" in result
    assert "interpretation" in result


def test_classification_scenario():

    X_array, y = make_classification(
        n_samples=120,
        n_features=5,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=[
            "a",
            "b",
            "c",
            "d",
            "e",
        ],
    )

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="classification",
        cv_mean=0.80,
        test_score=0.80,
    )

    result = engine.scenario(
        threshold=0.50,
    )

    assert (
        result["summary"]["observations"]
        == 120
    )

    assert (
        0
        <= result["summary"]["selected_rate"]
        <= 1
    )


def test_weak_regression_warning():

    X_array, y = make_regression(
        n_samples=80,
        n_features=3,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=[
            "x1",
            "x2",
            "x3",
        ],
    )

    model = LinearRegression()
    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="regression",
        cv_mean=-0.10,
        test_score=-0.05,
    )

    summary = engine.summary()

    assert (
        summary["assessment"]["reliable"]
        is False
    )

    assert (
        summary["assessment"]["level"]
        == "prudence"
    )
