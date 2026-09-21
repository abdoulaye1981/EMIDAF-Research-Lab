import pandas as pd

from emidaf_studio.pages.ekde.callbacks import (
    umap_analysis,
)


def _serialized_dataframe():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0, 1.1, 0.9,
                5.0, 5.2, 4.8,
                9.0, 9.1, 8.9,
            ],
            "x2": [
                1.0, 0.9, 1.1,
                5.0, 4.9, 5.1,
                9.0, 8.9, 9.1,
            ],
            "x3": [
                0.9, 1.0, 1.1,
                4.9, 5.1, 5.0,
                8.8, 9.0, 9.2,
            ],
        }
    )

    return dataframe.to_json(
        orient="split"
    )


def test_umap_callback_returns_summary_and_figure():
    summary, figure = umap_analysis(
        1,
        3,
        0.1,
        "euclidean",
        _serialized_dataframe(),
        None,
        None,
    )

    assert isinstance(
        summary,
        list,
    )

    assert figure is not None

    assert len(
        figure.data
    ) > 0


def test_umap_callback_adjusts_neighbors():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5],
            "x2": [5, 4, 3, 2, 1],
            "x3": [1, 1, 2, 2, 3],
        }
    )

    summary, figure = umap_analysis(
        1,
        50,
        0.1,
        "euclidean",
        dataframe.to_json(
            orient="split"
        ),
        None,
        None,
    )

    summary_text = str(summary)

    assert isinstance(
        summary,
        list,
    )

    assert figure is not None

    assert "50" in summary_text
    assert "4" in summary_text


def test_umap_callback_rejects_invalid_min_dist():
    summary, figure = umap_analysis(
        1,
        3,
        -0.1,
        "euclidean",
        _serialized_dataframe(),
        None,
        None,
    )

    assert figure == {}

    assert (
        "supérieur ou égal à 0"
        in str(summary)
    )


def test_umap_callback_rejects_invalid_metric():
    summary, figure = umap_analysis(
        1,
        3,
        0.1,
        "invalid",
        _serialized_dataframe(),
        None,
        None,
    )

    assert figure == {}

    assert (
        "Métrique UMAP non reconnue"
        in str(summary)
    )


def test_umap_callback_requires_two_numeric_variables():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "group": [
                "A",
                "B",
                "C",
                "D",
            ],
        }
    )

    summary, figure = umap_analysis(
        1,
        3,
        0.1,
        "euclidean",
        dataframe.to_json(
            orient="split"
        ),
        None,
        None,
    )

    assert figure == {}

    assert (
        "deux variables numériques"
        in str(summary)
    )
