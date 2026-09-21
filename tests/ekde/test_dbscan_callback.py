import pandas as pd

from emidaf_studio.pages.ekde.callbacks import (
    dbscan_analysis,
)


def _serialized_dataframe():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0, 1.1, 0.9,
                5.0, 5.1, 4.9,
                20.0,
            ],
            "x2": [
                1.0, 0.9, 1.1,
                5.0, 5.1, 4.9,
                20.0,
            ],
        }
    )

    return dataframe.to_json(
        orient="split"
    )


def test_dbscan_callback_returns_summary_and_figure():
    summary, figure = dbscan_analysis(
        1,
        0.35,
        2,
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


def test_dbscan_callback_displays_noise():
    summary, figure = dbscan_analysis(
        1,
        0.35,
        2,
        _serialized_dataframe(),
        None,
        None,
    )

    trace_names = [
        trace.name
        for trace in figure.data
    ]

    assert "Bruit" in trace_names

    assert (
        "Bruit"
        in str(summary)
    )


def test_dbscan_callback_handles_single_cluster():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                1.0,
                1.0,
                1.0,
            ],
            "x2": [
                2.0,
                2.0,
                2.0,
                2.0,
            ],
        }
    )

    serialized = dataframe.to_json(
        orient="split"
    )

    summary, figure = dbscan_analysis(
        1,
        0.5,
        2,
        serialized,
        None,
        None,
    )

    assert isinstance(
        summary,
        list,
    )

    assert figure is not None

    assert (
        "au moins deux clusters"
        in str(summary)
    )


def test_dbscan_callback_rejects_invalid_eps():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    serialized = dataframe.to_json(
        orient="split"
    )

    summary, figure = dbscan_analysis(
        1,
        0,
        2,
        serialized,
        None,
        None,
    )

    assert figure == {}

    assert (
        "strictement positif"
        in str(summary)
    )


def test_dbscan_callback_rejects_invalid_min_samples():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    serialized = dataframe.to_json(
        orient="split"
    )

    summary, figure = dbscan_analysis(
        1,
        0.5,
        5,
        serialized,
        None,
        None,
    )

    assert figure == {}

    assert (
        "ne peut pas dépasser"
        in str(summary)
    )


def test_dbscan_callback_requires_numeric_data():
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

    summary, figure = dbscan_analysis(
        1,
        0.5,
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
