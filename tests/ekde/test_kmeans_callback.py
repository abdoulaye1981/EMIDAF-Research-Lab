import pandas as pd

from emidaf_studio.pages.ekde import callbacks

from emidaf_studio.pages.ekde.callbacks import (
    kmeans_analysis,
)


def _dataframe():
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


def test_kmeans_callback_returns_summary_and_figure(monkeypatch):
    dataframe = _dataframe()

    _use_dataframe(
        monkeypatch,
        dataframe,
    )

    summary, figure = kmeans_analysis(
        1,
        3,
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


def test_kmeans_callback_rejects_invalid_cluster_number(monkeypatch):
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

    summary, figure = kmeans_analysis(
        1,
        4,
        None,
        None,
    )

    assert figure == {}

    assert (
        "strictement inférieur"
        in str(summary)
    )


def test_kmeans_callback_requires_numeric_data(monkeypatch):
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

    summary, figure = kmeans_analysis(
        1,
        2,
        None,
        None,
    )

    assert figure == {}

    assert (
        "variable numérique"
        in str(summary)
    )
