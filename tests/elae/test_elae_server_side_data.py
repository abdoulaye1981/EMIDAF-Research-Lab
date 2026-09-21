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
