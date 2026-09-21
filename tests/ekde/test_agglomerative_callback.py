import pandas as pd

from emidaf_studio.pages.ekde.callbacks import (
    agglomerative_analysis,
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
        }
    )

    return dataframe.to_json(
        orient="split"
    )


def test_agglomerative_callback_returns_summary_and_figure():
    summary, figure = agglomerative_analysis(
        1,
        3,
        "ward",
        "euclidean",
        _serialized_dataframe(),
        None,
        None,
    )

    assert isinstance(summary, list)
    assert figure is not None
    assert len(figure.data) > 0


def test_agglomerative_callback_ward_forces_euclidean():
    summary, figure = agglomerative_analysis(
        1,
        3,
        "ward",
        "manhattan",
        _serialized_dataframe(),
        None,
        None,
    )

    assert isinstance(summary, list)
    assert figure is not None

    summary_text = str(summary)

    assert "Ward" in summary_text
    assert "euclidean" in summary_text


def test_agglomerative_callback_accepts_average_manhattan():
    summary, figure = agglomerative_analysis(
        1,
        3,
        "average",
        "manhattan",
        _serialized_dataframe(),
        None,
        None,
    )

    assert isinstance(summary, list)
    assert figure is not None
    assert "manhattan" in str(summary)


def test_agglomerative_callback_rejects_invalid_cluster_number():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "x2": [4, 3, 2, 1],
        }
    )

    summary, figure = agglomerative_analysis(
        1,
        4,
        "ward",
        "euclidean",
        dataframe.to_json(orient="split"),
        None,
        None,
    )

    assert figure == {}

    assert (
        "strictement inférieur"
        in str(summary)
    )


def test_agglomerative_callback_rejects_invalid_linkage():
    summary, figure = agglomerative_analysis(
        1,
        3,
        "invalid",
        "euclidean",
        _serialized_dataframe(),
        None,
        None,
    )

    assert figure == {}
    assert "Linkage non reconnu" in str(summary)


def test_agglomerative_callback_rejects_invalid_metric():
    summary, figure = agglomerative_analysis(
        1,
        3,
        "average",
        "invalid",
        _serialized_dataframe(),
        None,
        None,
    )

    assert figure == {}
    assert "Métrique non reconnue" in str(summary)


def test_agglomerative_callback_requires_numeric_data():
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

    summary, figure = agglomerative_analysis(
        1,
        2,
        "ward",
        "euclidean",
        dataframe.to_json(
            orient="split"
        ),
        None,
        None,
    )

    assert figure == {}

    assert (
        "variable numérique"
        in str(summary)
    )
