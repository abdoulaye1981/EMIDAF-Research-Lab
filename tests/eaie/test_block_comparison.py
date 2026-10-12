import numpy as np
import pandas as pd

from sklearn.datasets import (
    make_regression,
)

from emidaf_core.eaie.blocks import (
    FeatureBlocks,
)

from emidaf_core.eaie.block_comparison import (
    BlockComparisonEngine,
)


def _dataset():

    X, y = make_regression(
        n_samples=160,
        n_features=6,
        n_informative=6,
        noise=8,
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
            "x6",
        ],
    )

    df["target"] = y

    return df


def _blocks():

    return FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
            "x6",
        ],
        blocks={
            "A": [
                "x1",
                "x2",
            ],
            "B": [
                "x3",
            ],
            "C": [
                "x4",
                "x5",
            ],
            "D": [
                "x6",
            ],
        },
        target="target",
        require_all=True,
    )


def test_block_comparison_runs():

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    result = engine.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
            "ridge",
        ],
    )

    assert len(
        result.performances
    ) == 4

    assert (
        result.selected_block
        is not None
    )

    assert (
        result.selected_model
        is not None
    )

    assert (
        result.final_result
        is not None
    )

    assert (
        result.final_result.r2
        is not None
    )


def test_block_comparison_uses_one_common_split():

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=4,
    )

    result = engine.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
        ],
    )

    assert len(
        result.train_indices
    ) == 128

    assert len(
        result.test_indices
    ) == 32

    assert set(
        result.train_indices
    ).isdisjoint(
        result.test_indices
    )

    assert len(
        result.cv_splits
    ) == 4


def test_block_comparison_cumulative_sizes():

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    result = engine.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
        ],
    )

    sizes = [
        item.n_features
        for item
        in result.performances
    ]

    assert sizes == [
        2,
        3,
        5,
        6,
    ]


def test_block_comparison_delta_cv():

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    result = engine.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
        ],
    )

    performances = (
        result.performances
    )

    assert (
        performances[0].delta_cv
        is None
    )

    for index in range(
        1,
        len(performances),
    ):

        expected = (
            performances[index].cv_mean
            - performances[
                index - 1
            ].cv_mean
        )

        assert np.isclose(
            performances[
                index
            ].delta_cv,
            expected,
        )


def test_block_comparison_final_test_only_once(
    monkeypatch,
):

    from emidaf_core.eaie.evaluation import (
        ModelEvaluator,
    )

    calls = []

    original = (
        ModelEvaluator.regression
    )

    def spy(**kwargs):

        calls.append(
            {
                "model":
                    kwargs["model_name"],
                "test_size":
                    len(
                        kwargs["y_test"]
                    ),
            }
        )

        return original(
            **kwargs
        )

    monkeypatch.setattr(
        ModelEvaluator,
        "regression",
        staticmethod(
            spy
        ),
    )

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    engine.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
            "ridge",
        ],
    )

    # 4 blocs x 2 modèles sont comparés,
    # mais le TEST final n'est évalué
    # qu'une seule fois.
    assert len(calls) == 1

    assert (
        calls[0][
            "test_size"
        ]
        == 32
    )


def test_block_comparison_reproducible_folds():

    engine_1 = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    engine_2 = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    result_1 = engine_1.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
        ],
    )

    result_2 = engine_2.run(
        _dataset(),
        target="target",
        blocks=_blocks(),
        task="regression",
        models=[
            "linear_regression",
        ],
    )

    assert (
        result_1.train_indices
        == result_2.train_indices
    )

    assert (
        result_1.test_indices
        == result_2.test_indices
    )

    assert (
        result_1.cv_splits
        == result_2.cv_splits
    )


def test_block_comparison_classification_stratified_and_test_once(
    monkeypatch,
):

    from sklearn.datasets import (
        make_classification,
    )

    from emidaf_core.eaie.evaluation import (
        ModelEvaluator,
    )

    X, y = make_classification(
        n_samples=200,
        n_features=8,
        n_informative=6,
        n_redundant=0,
        weights=[
            0.60,
            0.40,
        ],
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
            "x6",
            "x7",
            "x8",
        ],
    )

    df["target"] = y

    blocks = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
            "x6",
            "x7",
            "x8",
        ],
        blocks={
            "A": [
                "x1",
                "x2",
            ],
            "B": [
                "x3",
                "x4",
            ],
            "C": [
                "x5",
                "x6",
            ],
            "D": [
                "x7",
                "x8",
            ],
        },
        target="target",
        require_all=True,
    )

    calls = []

    original = (
        ModelEvaluator.classification
    )

    def spy(**kwargs):

        calls.append(
            {
                "model":
                    kwargs["model_name"],
                "test_size":
                    len(
                        kwargs["y_test"]
                    ),
            }
        )

        return original(
            **kwargs
        )

    monkeypatch.setattr(
        ModelEvaluator,
        "classification",
        staticmethod(
            spy
        ),
    )

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=4,
    )

    result = engine.run(
        df,
        target="target",
        blocks=blocks,
        task="classification",
        models=[
            "logistic_regression",
            "random_forest",
        ],
    )

    # -----------------------------------------------------
    # Structure générale
    # -----------------------------------------------------

    assert result.task == "classification"

    assert len(
        result.performances
    ) == 4

    assert (
        result.selected_block
        is not None
    )

    assert (
        result.selected_model
        is not None
    )

    # -----------------------------------------------------
    # Split commun 80 / 20
    # -----------------------------------------------------

    assert len(
        result.train_indices
    ) == 160

    assert len(
        result.test_indices
    ) == 40

    assert set(
        result.train_indices
    ).isdisjoint(
        result.test_indices
    )

    # -----------------------------------------------------
    # Stratification des folds
    # -----------------------------------------------------

    y_train = (
        df["target"]
        .iloc[
            result.train_indices
        ]
        .reset_index(
            drop=True
        )
    )

    assert len(
        result.cv_splits
    ) == 4

    for (
        train_idx,
        valid_idx,
    ) in result.cv_splits:

        train_classes = set(
            y_train.iloc[
                train_idx
            ]
        )

        valid_classes = set(
            y_train.iloc[
                valid_idx
            ]
        )

        assert train_classes == {
            0,
            1,
        }

        assert valid_classes == {
            0,
            1,
        }

    # -----------------------------------------------------
    # TEST FINAL UTILISE UNE SEULE FOIS
    # -----------------------------------------------------

    # 4 blocs x 2 modèles =
    # 8 configurations CV,
    # mais une seule évaluation hold-out.
    assert len(calls) == 1

    assert (
        calls[0][
            "test_size"
        ]
        == 40
    )

    final = (
        result.final_result
    )

    assert final is not None
    assert final.fitted is True

    assert (
        final.f1_score
        is not None
    )

    assert (
        final.confusion_matrix
    )

    assert (
        final.classification_report
    )

    # -----------------------------------------------------
    # Sélection strictement fondée sur la CV
    # -----------------------------------------------------

    best_cv = max(
        item.cv_mean
        for item
        in result.performances
    )

    selected_performance = next(
        item
        for item
        in result.performances
        if item.block
        == result.selected_block
    )

    assert np.isclose(
        selected_performance.cv_mean,
        best_cv,
    )

    assert (
        final.metadata[
            "selected_block"
        ]
        == result.selected_block
    )

    assert (
        final.metadata[
            "block_comparison"
        ]
        is True
    )


def _classification_block_dataset():

    from sklearn.datasets import (
        make_classification,
    )

    X, y = make_classification(
        n_samples=200,
        n_features=8,
        n_informative=6,
        n_redundant=0,
        weights=[
            0.60,
            0.40,
        ],
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
            "x6",
            "x7",
            "x8",
        ],
    )

    df["target"] = y

    blocks = FeatureBlocks.resolve(
        predictors=[
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
            "x6",
            "x7",
            "x8",
        ],
        blocks={
            "A": ["x1", "x2"],
            "B": ["x3", "x4"],
            "C": ["x5", "x6"],
            "D": ["x7", "x8"],
        },
        target="target",
        require_all=True,
    )

    return df, blocks


def test_block_comparison_keeps_default_classification_metric():

    df, blocks = (
        _classification_block_dataset()
    )

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
    )

    result = engine.run(
        df,
        target="target",
        blocks=blocks,
        task="classification",
        models=[
            "logistic_regression",
        ],
    )

    assert all(
        item.cv_metric
        == "f1_weighted"
        for item
        in result.performances
    )

    assert (
        result.final_result
        .metadata[
            "selection_metric"
        ]
        == "f1_weighted"
    )


def test_block_comparison_uses_requested_f1_metric():

    df, blocks = (
        _classification_block_dataset()
    )

    engine = BlockComparisonEngine(
        test_size=0.20,
        random_state=42,
        cv=3,
        selection_metric="f1",
        positive_label=1,
    )

    result = engine.run(
        df,
        target="target",
        blocks=blocks,
        task="classification",
        models=[
            "logistic_regression",
        ],
    )

    assert all(
        item.cv_metric == "f1"
        for item
        in result.performances
    )

    final = result.final_result

    assert final is not None

    assert (
        final.metadata[
            "selection_metric"
        ]
        == "f1"
    )

    assert (
        final.metadata[
            "positive_label"
        ]
        == 1
    )

    assert final.positive_label == 1

    assert (
        final.precision_positive
        is not None
    )

    assert (
        final.recall_positive
        is not None
    )

    assert (
        final.f1_positive
        is not None
    )

    assert final.pr_auc is not None
    assert final.roc_auc is not None
