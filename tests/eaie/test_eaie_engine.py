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


def test_cross_validation_uses_training_set_only(
    monkeypatch,
):

    from emidaf_core.eaie.comparison import (
        ModelComparison,
    )

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

    observed_sizes = []

    original_cross_validate = (
        ModelComparison.cross_validate
    )

    def spy_cross_validate(
        estimator,
        X,
        y,
        task,
        cv=5,
        scoring=None,
    ):
        observed_sizes.append(
            (
                len(X),
                len(y),
            )
        )

        return original_cross_validate(
            estimator,
            X,
            y,
            task=task,
            cv=cv,
            scoring=scoring,
        )

    monkeypatch.setattr(
        ModelComparison,
        "cross_validate",
        staticmethod(
            spy_cross_validate
        ),
    )

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    engine.run(
        df,
        target="target",
        task="regression",
        models=[
            "linear_regression",
            "random_forest",
        ],
    )

    # 120 observations avec 20 % réservées au test :
    # 96 train / 24 test.
    assert len(
        engine.X_train_
    ) == 96

    assert len(
        engine.X_test_
    ) == 24

    # Une CV baseline + une CV par modèle.
    assert len(
        observed_sizes
    ) == 3

    # Toutes les validations croisées doivent être
    # réalisées exclusivement sur le train.
    assert all(
        x_size == 96
        and y_size == 96
        for x_size, y_size
        in observed_sizes
    )

    # Protection explicite contre une régression future :
    # aucune CV ne doit revoir les 120 observations.
    assert all(
        x_size != 120
        for x_size, _
        in observed_sizes
    )


def test_only_selected_model_uses_final_test_set(
    monkeypatch,
):

    from emidaf_core.eaie.evaluation import (
        ModelEvaluator,
    )

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

    evaluation_calls = []

    original_regression = (
        ModelEvaluator.regression
    )

    def spy_regression(**kwargs):

        evaluation_calls.append(
            {
                "model_name":
                    kwargs["model_name"],
                "test_size":
                    len(kwargs["y_test"]),
            }
        )

        return original_regression(
            **kwargs
        )

    monkeypatch.setattr(
        ModelEvaluator,
        "regression",
        staticmethod(
            spy_regression
        ),
    )

    engine = EAIEEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    candidates = engine.run(
        df,
        target="target",
        task="regression",
        models=[
            "linear_regression",
            "random_forest",
        ],
    )

    # Deux candidats sont comparés.
    assert len(candidates) == 2

    # Aucun candidat non sélectionné ne possède
    # une métrique provenant du test.
    assert all(
        result.score is None
        for result in candidates
    )

    assert all(
        result.r2 is None
        for result in candidates
    )

    # Le jeu de test ne doit être évalué
    # qu'une seule fois.
    assert len(
        evaluation_calls
    ) == 1

    assert (
        evaluation_calls[0][
            "test_size"
        ]
        == 24
    )

    best = engine.best()

    # Le résultat final possède bien
    # les métriques hold-out.
    assert best.fitted is True
    assert best.score is not None
    assert best.r2 is not None

    # Et conserve les informations
    # utilisées lors de la sélection CV.
    assert (
        best.metadata.get(
            "cv_mean"
        )
        is not None
    )


def test_model_comparison_is_ranked_by_cv():

    X, y = make_regression(
        n_samples=140,
        n_features=5,
        noise=10,
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

    engine.run(
        df,
        target="target",
        task="regression",
        models=[
            "linear_regression",
            "random_forest",
            "decision_tree",
        ],
    )

    comparison = engine.compare()

    cv_values = (
        comparison[
            "cv_mean"
        ]
        .dropna()
        .tolist()
    )

    assert cv_values == sorted(
        cv_values,
        reverse=True,
    )

    # Le meilleur modèle affiché dans
    # le classement est celui sélectionné.
    assert (
        comparison.iloc[0][
            "model"
        ]
        == engine.best().model_name
    )
