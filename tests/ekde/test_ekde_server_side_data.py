import pandas as pd
import pytest

from dash.exceptions import PreventUpdate

from emidaf_studio.pages.ekde import callbacks


def test_load_ekde_dataframe_uses_server_dataset(
    monkeypatch,
):
    expected = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y": [4, 5, 6],
        }
    )

    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        assert project_id == 1
        assert dataset_id == 2

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

    result = callbacks._load_ekde_dataframe(
        1,
        2,
    )

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_load_ekde_dataframe_rejects_error(
    monkeypatch,
):
    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        return (
            None,
            None,
            "Dataset indisponible",
        )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    with pytest.raises(PreventUpdate):
        callbacks._load_ekde_dataframe(
            1,
            2,
        )


def test_load_ekde_dataframe_rejects_invalid_result(
    monkeypatch,
):
    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        return (
            None,
            None,
            {"unexpected": "value"},
        )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    with pytest.raises(PreventUpdate):
        callbacks._load_ekde_dataframe(
            1,
            2,
        )
