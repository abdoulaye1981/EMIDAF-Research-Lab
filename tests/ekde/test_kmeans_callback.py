import pandas as pd

from emidaf_studio.pages.ekde.callbacks import (
    kmeans_analysis,
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


def test_kmeans_callback_returns_summary_and_figure():
    summary, figure = kmeans_analysis(
        1,
        3,
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


def test_kmeans_callback_rejects_invalid_cluster_number():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    serialized = dataframe.to_json(
        orient="split"
    )

    summary, figure = kmeans_analysis(
        1,
        4,
        serialized,
        None,
        None,
    )

    assert figure == {}

    assert (
        "strictement inférieur"
        in str(summary)
    )


def test_kmeans_callback_requires_numeric_data():
    dataframe = pd.DataFrame(
        {
            "group": [
                "A",
                "B",
                "C",
                "D",
            ]
        }
    )

    serialized = dataframe.to_json(
        orient="split"
    )

    summary, figure = kmeans_analysis(
        1,
        2,
        serialized,
        None,
        None,
    )

    assert figure == {}

    assert (
        "variable numérique"
        in str(summary)
    )
