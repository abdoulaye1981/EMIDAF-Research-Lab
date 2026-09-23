import pandas as pd

from emidaf_core.preprocessing.dimensionality import (
    TSNEReduction,
)

from emidaf_studio.pages.ekde import callbacks

from emidaf_studio.pages.ekde.callbacks import (
    tsne_analysis,
)


def _use_dataframe(
    monkeypatch,
    dataframe,
):
    monkeypatch.setattr(
        callbacks,
        "_load_ekde_dataframe",
        lambda project_id, dataset_id: dataframe,
    )


def test_tsne_reduction_accepts_perplexity():
    model = TSNEReduction(
        n_components=2,
        perplexity=5,
    )

    assert (
        model.model.perplexity
        == 5.0
    )


def test_tsne_fit_transform_returns_two_components():
    dataframe = pd.DataFrame(
        {
            "x1": range(1, 11),
            "x2": range(11, 21),
            "x3": [
                value % 3
                for value in range(10)
            ],
        }
    )

    model = TSNEReduction(
        n_components=2,
        perplexity=3,
    )

    result = model.fit_transform(
        dataframe
    )

    assert isinstance(
        result,
        pd.DataFrame,
    )

    assert result.shape == (
        10,
        2,
    )

    assert list(
        result.columns
    ) == [
        "TSNE1",
        "TSNE2",
    ]


def test_tsne_is_reproducible_with_fixed_random_state():
    dataframe = pd.DataFrame(
        {
            "x1": range(1, 16),
            "x2": range(15, 0, -1),
            "x3": [
                value % 4
                for value in range(15)
            ],
        }
    )

    first = TSNEReduction(
        n_components=2,
        perplexity=4,
    ).fit_transform(
        dataframe
    )

    second = TSNEReduction(
        n_components=2,
        perplexity=4,
    ).fit_transform(
        dataframe
    )

    pd.testing.assert_frame_equal(
        first,
        second,
    )


def test_tsne_callback_adjusts_invalid_perplexity(monkeypatch):
    dataframe = pd.DataFrame(
        {
            "x1": range(1, 11),
            "x2": range(10, 0, -1),
            "x3": [
                value % 2
                for value in range(10)
            ],
        }
    )

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = tsne_analysis(
        1,
        100,
        None,
        None,
    )

    assert isinstance(
        summary,
        list,
    )

    assert figure is not None


def test_tsne_callback_requires_two_numeric_variables(monkeypatch):
    dataframe = pd.DataFrame(
        {
            "x1": range(1, 11),
            "category": [
                "A",
                "B",
                "A",
                "B",
                "A",
                "B",
                "A",
                "B",
                "A",
                "B",
            ],
        }
    )

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = tsne_analysis(
        1,
        3,
        None,
        None,
    )

    assert figure == {}

    text = str(summary)

    assert (
        "deux variables numériques"
        in text
    )
