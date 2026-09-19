import numpy as np
import pandas as pd

from sklearn.datasets import (
    make_classification,
    make_regression,
)

from emidaf_core.common.results import ModelResult
from emidaf_core.eaie import (
    EAIEEngine,
    ProblemDetector,
)


def test_problem_detector_classification():

    y = pd.Series(
        ["A", "B", "A", "B"]
    )

    assert (
        ProblemDetector.detect(y)
        == "classification"
    )


def test_problem_detector_regression():

    y = pd.Series(
        np.linspace(0, 100, 100)
    )

    assert (
        ProblemDetector.detect(y)
        == "regression"
    )


def test_regression_engine():

    X, y = make_regression(
        n_samples=120,
        n_features=4,
        noise=5,
        random_state=42,
    )

    df = pd.DataFrame(
        X,
        columns=[
            "x1",
            "x2",
            "x3",
            "x4",
        ],
    )

    df["target"] = y

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    results = engine.run(
        df,
        target="target",
        task="regression",
        models=[
            "linear_regression",
            "random_forest",
        ],
    )

    assert len(results) == 2

    assert all(
        isinstance(
            result,
            ModelResult,
        )
        for result in results
    )

    best = engine.best()

    assert best.task == "regression"
    assert best.estimator is not None

    summary = engine.summary()

    assert (
        summary["selection_metric"]
        == "r2"
    )

    assert (
        summary["baseline_cv_mean"]
        is not None
    )


def test_classification_engine():

    X, y = make_classification(
        n_samples=150,
        n_features=5,
        n_informative=4,
        n_redundant=0,
        random_state=42,
    )

    df = pd.DataFrame(
        X,
        columns=[
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
        ],
    )

    df["target"] = y

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    results = engine.run(
        df,
        target="target",
        task="classification",
        models=[
            "logistic_regression",
            "random_forest",
        ],
    )

    assert len(results) == 2

    best = engine.best()

    assert (
        best.task
        == "classification"
    )

    assert (
        best.confusion_matrix
    )

    assert (
        best.classification_report
    )

    summary = engine.summary()

    assert (
        summary["selection_metric"]
        == "f1_weighted"
    )

    assert (
        summary["baseline_cv_mean"]
        is not None
    )


def test_mixed_data_and_missing_values():

    df = pd.DataFrame(
        {
            "age": [
                20,
                21,
                None,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
            ],
            "income": [
                "100",
                "120",
                "130",
                None,
                "150",
                "160",
                "170",
                "180",
                "190",
                "200",
                "210",
                "220",
            ],
            "gender": [
                "F",
                "M",
                "F",
                "M",
                None,
                "M",
                "F",
                "M",
                "F",
                "M",
                "F",
                "M",
            ],
            "target": [
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
        }
    )

    engine = EAIEEngine(
        test_size=0.25,
        random_state=42,
        cv=2,
    )

    engine.run(
        df,
        target="target",
        task="classification",
        models=[
            "logistic_regression"
        ],
    )

    result = engine.best()

    assert result.fitted is True
    assert result.estimator is not None
