import pandas as pd

from sklearn.datasets import (
    make_classification,
    make_regression,
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
)

from sklearn.ensemble import (
    RandomForestClassifier,
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from emidaf_core.exaie import EXAIEEngine


def test_linear_regression_importance():

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

    model = Pipeline(
        [
            (
                "scale",
                StandardScaler(),
            ),
            (
                "model",
                LinearRegression(),
            ),
        ]
    )

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    importance = engine.global_importance()

    assert importance is not None
    assert len(importance) == 4
    assert "importance" in importance.columns


def test_classification_permutation():

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

    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    table = engine.permutation_importance(
        n_repeats=3,
    )

    assert len(table) == 5
    assert "importance" in table.columns


def test_local_linear_explanation():

    X_array, y = make_classification(
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

    model = Pipeline(
        [
            (
                "scale",
                StandardScaler(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000
                ),
            ),
        ]
    )

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    explanation = engine.local_explanation(
        row=0
    )

    assert explanation["available"] is True

    assert (
        "contributions"
        in explanation
    )


def test_summary():

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

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    summary = engine.summary()

    assert (
        summary["native_available"]
        is True
    )

    assert (
        "native_interpretation"
        in summary
    )


def test_summary_reuses_precomputed_importances(
    monkeypatch,
):
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

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    engine.global_importance()

    engine.permutation_importance(
        n_repeats=2,
    )

    def fail_native():
        raise AssertionError(
            "global_importance ne doit pas "
            "être recalculée."
        )

    def fail_permutation(**kwargs):
        raise AssertionError(
            "permutation_importance ne doit pas "
            "être recalculée."
        )

    monkeypatch.setattr(
        engine,
        "global_importance",
        fail_native,
    )

    monkeypatch.setattr(
        engine,
        "permutation_importance",
        fail_permutation,
    )

    summary = engine.summary()

    assert (
        summary["native_available"]
        is True
    )

    assert (
        summary["permutation_available"]
        is True
    )


def test_local_explanation_rejects_invalid_row():
    X_array, y = make_classification(
        n_samples=50,
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

    model = Pipeline(
        [
            (
                "scale",
                StandardScaler(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000
                ),
            ),
        ]
    )

    model.fit(
        X,
        y,
    )

    engine = EXAIEEngine(
        model,
        X,
        y,
    )

    try:
        engine.local_explanation(
            row=len(X),
        )
    except IndexError as exc:
        assert (
            "Indice d'observation invalide"
            in str(exc)
        )
    else:
        raise AssertionError(
            "IndexError attendu"
        )
