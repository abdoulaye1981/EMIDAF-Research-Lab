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


def test_invalid_task_is_rejected():
    X_array, y = make_regression(
        n_samples=40,
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

    try:
        EDSEEngine(
            model,
            X,
            task="unknown",
        )
    except ValueError as exc:
        assert "classification" in str(exc)
        assert "regression" in str(exc)
    else:
        raise AssertionError(
            "Une task invalide doit être rejetée."
        )


def test_classification_rejects_invalid_threshold():
    X_array, y = make_classification(
        n_samples=80,
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
    )

    try:
        engine.scenario(
            threshold=1.20,
        )
    except ValueError as exc:
        assert "entre 0 et 1" in str(exc)
    else:
        raise AssertionError(
            "Un seuil > 1 doit être rejeté."
        )


def test_regression_rejects_invalid_direction():
    X_array, y = make_regression(
        n_samples=50,
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

    try:
        engine.scenario(
            threshold=0.0,
            direction="invalid",
        )
    except ValueError as exc:
        assert "above" in str(exc)
        assert "below" in str(exc)
    else:
        raise AssertionError(
            "Une direction invalide doit être rejetée."
        )


def test_missing_scores_are_not_declared_acceptable():
    X_array, y = make_regression(
        n_samples=50,
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
        cv_mean=None,
        test_score=None,
    )

    assessment = (
        engine.summary()["assessment"]
    )

    assert assessment["evaluable"] is False
    assert assessment["reliable"] is False
    assert assessment["level"] == "non évaluable"


def test_baseline_failure_requires_prudence():
    X_array, y = make_regression(
        n_samples=60,
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
        cv_mean=0.80,
        test_score=0.75,
        better_than_baseline=False,
    )

    assessment = (
        engine.summary()["assessment"]
    )

    assert assessment["evaluable"] is True
    assert assessment["reliable"] is False
    assert assessment["level"] == "prudence"

    assert any(
        "référence naïve" in warning
        for warning in assessment["warnings"]
    )


def test_profiles_preserve_original_index():

    X_array, y = make_regression(
        n_samples=30,
        n_features=3,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=["x1", "x2", "x3"],
        index=range(100, 130),
    )

    model = LinearRegression()
    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="regression",
    )

    profiles = engine.profiles()

    assert set(
        profiles["observation"].tolist()
    ) == set(
        X.index.tolist()
    )


def test_binary_classification_exposes_positive_class():

    X_array, y = make_classification(
        n_samples=100,
        n_features=5,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=["a", "b", "c", "d", "e"],
    )

    model = LogisticRegression(
        max_iter=1000
    )
    model.fit(X, y)

    engine = EDSEEngine(
        model,
        X,
        task="classification",
    )

    engine.scenario(
        threshold=0.50
    )

    assert (
        engine.positive_class_
        == model.classes_[1]
    )


def test_scenario_preserves_original_index():

    X_array, y = make_regression(
        n_samples=30,
        n_features=3,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=["x1", "x2", "x3"],
        index=range(200, 230),
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

    assert (
        result["table"]["observation"]
        .tolist()
        == X.index.tolist()
    )


def test_multiclass_classification_is_rejected():

    X_array, y = make_classification(
        n_samples=120,
        n_features=6,
        n_classes=3,
        n_informative=4,
        n_redundant=0,
        random_state=42,
    )

    X = pd.DataFrame(
        X_array,
        columns=[
            "a", "b", "c",
            "d", "e", "f",
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
    )

    try:
        engine.scenario(
            threshold=0.50
        )
    except RuntimeError as exc:
        assert "binaire" in str(exc)
    else:
        raise AssertionError(
            "EDSE doit rejeter explicitement "
            "la classification multiclasse."
        )
