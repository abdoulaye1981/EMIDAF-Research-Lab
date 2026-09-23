import pandas as pd

from emidaf_studio.pages.ekde import callbacks

from emidaf_studio.pages.ekde.callbacks import (
    dbscan_analysis,
)


def _dataframe():
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

    return dataframe


def _use_dataframe(
    monkeypatch,
    dataframe,
):
    monkeypatch.setattr(
        callbacks,
        "_load_ekde_dataframe",
        lambda project_id, dataset_id: dataframe,
    )


def test_dbscan_callback_returns_summary_and_figure(monkeypatch):
    dataframe = _dataframe()

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0.35,
        2,
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


def test_dbscan_callback_displays_noise(monkeypatch):
    dataframe = _dataframe()

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0.35,
        2,
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


def test_dbscan_callback_handles_single_cluster(monkeypatch):
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

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0.5,
        2,
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


def test_dbscan_callback_rejects_invalid_eps(monkeypatch):
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0,
        2,
        None,
        None,
    )

    assert figure == {}

    assert (
        "strictement positif"
        in str(summary)
    )


def test_dbscan_callback_rejects_invalid_min_samples(monkeypatch):
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0.5,
        5,
        None,
        None,
    )

    assert figure == {}

    assert (
        "ne peut pas dépasser"
        in str(summary)
    )


def test_dbscan_callback_requires_numeric_data(monkeypatch):
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

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = dbscan_analysis(
        1,
        0.5,
        2,
        None,
        None,
    )

    assert figure == {}

    assert (
        "variable numérique"
        in str(summary)
    )
