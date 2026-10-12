import pandas as pd

from emidaf_core.eaie.comparison import (
    ModelComparison,
)
from emidaf_core.eaie.engine import (
    EAIEEngine,
)


def _classification_dataframe():

    return pd.DataFrame(
        {
            "x1": [
                -3.0,
                -2.5,
                -2.0,
                -1.5,
                -1.0,
                -0.5,
                0.5,
                1.0,
                1.5,
                2.0,
                2.5,
                3.0,
                -2.8,
                -1.8,
                -0.8,
                0.8,
                1.8,
                2.8,
                -2.2,
                2.2,
            ],
            "x2": [
                0, 1, 0, 1, 0,
                1, 0, 1, 0, 1,
                0, 1, 1, 0, 1,
                0, 1, 0, 0, 1,
            ],
            "target": [
                0, 0, 0, 0, 0,
                0, 1, 1, 1, 1,
                1, 1, 0, 0, 0,
                1, 1, 1, 0, 1,
            ],
        }
    )


def test_cross_validation_default_classification_metric():

    from sklearn.linear_model import (
        LogisticRegression,
    )

    df = _classification_dataframe()

    result = ModelComparison.cross_validate(
        LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),
        df[["x1", "x2"]],
        df["target"],
        task="classification",
        cv=2,
    )

    assert (
        result["cv_metric"]
        == "f1_weighted"
    )


def test_cross_validation_accepts_f1_metric():

    from sklearn.linear_model import (
        LogisticRegression,
    )

    df = _classification_dataframe()

    result = ModelComparison.cross_validate(
        LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),
        df[["x1", "x2"]],
        df["target"],
        task="classification",
        cv=2,
        scoring="f1",
    )

    assert result["cv_metric"] == "f1"

    assert 0 <= result["cv_mean"] <= 1


def test_eaie_engine_uses_requested_selection_metric():

    df = _classification_dataframe()

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=2,
        selection_metric="f1",
        positive_label=1,
    )

    engine.run(
        df,
        target="target",
        task="classification",
        models=[
            "logistic_regression",
        ],
    )

    assert engine.selection_metric_ == "f1"

    best = engine.best()

    assert (
        best.metadata[
            "selection_metric"
        ]
        == "f1"
    )

    assert (
        best.metadata[
            "positive_label"
        ]
        == 1
    )

    assert (
        best.positive_label
        == 1
    )

    assert (
        best.f1_positive
        is not None
    )


def test_eaie_engine_keeps_historical_default():

    df = _classification_dataframe()

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=2,
    )

    engine.run(
        df,
        target="target",
        task="classification",
        models=[
            "logistic_regression",
        ],
    )

    assert (
        engine.selection_metric_
        == "f1_weighted"
    )

    assert (
        engine.best()
        .metadata[
            "selection_metric"
        ]
        == "f1_weighted"
    )
