import pandas as pd
import pytest

from emidaf_studio.pages.eaie import callbacks


def test_load_eaie_dataframe_uses_server_dataset(
    monkeypatch,
):
    expected = pd.DataFrame(
        {
            "x1": [1, 2, 3],
            "target": [0, 1, 0],
        }
    )

    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        assert project_id == 10
        assert dataset_id == 20

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

    result = callbacks._load_eaie_dataframe(
        10,
        20,
    )

    pd.testing.assert_frame_equal(
        result,
        expected,
    )


def test_load_eaie_dataframe_rejects_error(
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

    with pytest.raises(
        ValueError,
        match="Dataset indisponible",
    ):
        callbacks._load_eaie_dataframe(
            10,
            20,
        )


def test_load_eaie_dataframe_rejects_invalid_result(
    monkeypatch,
):
    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        return (
            None,
            None,
            {"invalid": True},
        )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    with pytest.raises(
        ValueError,
        match="dataset EAIE",
    ):
        callbacks._load_eaie_dataframe(
            10,
            20,
        )
