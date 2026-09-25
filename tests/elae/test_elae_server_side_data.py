import inspect

import pandas as pd
import pytest
from dash.exceptions import PreventUpdate

from emidaf_studio.pages.elae import callbacks


def test_load_elae_dataframe_uses_server_dataset(
    monkeypatch,
):
    expected = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
    )

    calls = []

    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        calls.append(
            (
                project_id,
                dataset_id,
            )
        )
        return (
            object(),
            object(),
            expected,
        )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    result = (
        callbacks._load_elae_dataframe(
            10,
            20,
        )
    )

    assert calls == [(10, 20)]
    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_load_elae_dataframe_stops_on_error(
    monkeypatch,
):
    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        return (
            None,
            None,
            "Dataset introuvable.",
        )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    with pytest.raises(PreventUpdate):
        callbacks._load_elae_dataframe(
            10,
            20,
        )


@pytest.mark.parametrize(
    "function_name",
    [
        "descriptive_analysis",
        "univariate",
        "bivariate",
        "correlations",
        "grouped_analysis",
        "download_summary",
    ],
)
def test_elae_callbacks_do_not_receive_dataframe_json(
    function_name,
):
    function = getattr(
        callbacks,
        function_name,
    )

    parameters = inspect.signature(
        function
    ).parameters

    assert "data" not in parameters


def test_elae_callbacks_keep_project_and_dataset_context():
    function_names = [
        "descriptive_analysis",
        "univariate",
        "bivariate",
        "correlations",
        "grouped_analysis",
        "download_summary",
    ]

    for function_name in function_names:
        function = getattr(
            callbacks,
            function_name,
        )

        parameters = inspect.signature(
            function
        ).parameters

        assert "project_id" in parameters
        assert "dataset_id" in parameters


def test_correlations_accepts_dataframe_matrix(
    monkeypatch,
):
    """
    Une matrice de corrélation fournie sous forme de
    DataFrame ne doit jamais être évaluée comme booléen.
    """

    from types import SimpleNamespace

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0],
            "y": [2.0, 4.0, 6.0],
        }
    )

    correlation_matrix = pd.DataFrame(
        {
            "x": [1.0, 1.0],
            "y": [1.0, 1.0],
        },
        index=["x", "y"],
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    class FakeProfiler:
        def profile(self, data):
            return SimpleNamespace(
                correlations={
                    "correlation_matrix": (
                        correlation_matrix
                    )
                }
            )

    monkeypatch.setattr(
        callbacks,
        "DatasetProfiler",
        FakeProfiler,
    )

    persisted = []

    monkeypatch.setattr(
        callbacks,
        "_persist_elae",
        lambda *args: persisted.append(args),
    )

    table, figure = callbacks.correlations(
        "correlations",
        10,
        20,
    )

    assert table is not None
    assert figure is not None
    assert len(figure.data) > 0

    assert persisted

    assert (
        persisted[0][2]
        == "correlations"
    )
