import pandas as pd

from emidaf_studio.pages.eidpp import callbacks


def _dataset():
    return pd.DataFrame(
        {
            "age": [20.0, 21.0, 22.0, 23.0],
            "score": [10.0, 12.0, 14.0, 16.0],
            "group": ["A", "A", "B", "B"],
        }
    )


def test_apply_preprocessing_uses_server_side_dataset(
    monkeypatch,
):
    dataframe = _dataset()

    persisted = {}

    def fake_load_dataset(project_id, dataset_id):
        assert project_id == 1
        assert dataset_id == 2

        project = object()
        dataset = object()

        return (
            project,
            dataset,
            dataframe.copy(),
        )

    def fake_register_analysis(
        project_id,
        dataset_id,
        stage,
        payload,
    ):
        persisted["project_id"] = project_id
        persisted["dataset_id"] = dataset_id
        persisted["stage"] = stage
        persisted["payload"] = payload

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    monkeypatch.setattr(
        callbacks,
        "register_analysis",
        fake_register_analysis,
    )

    comparison, preview, alert = (
        callbacks.apply_preprocessing(
            1,
            "none",
            [],
            "none",
            "none",
            "none",
            1,
            2,
        )
    )

    assert comparison is not None
    assert preview is not None
    assert alert is not None

    assert persisted["project_id"] == 1
    assert persisted["dataset_id"] == 2
    assert persisted["stage"] == "eidpp"

    payload = persisted["payload"]

    assert (
        payload["rows_before"]
        == len(dataframe)
    )

    assert (
        payload["rows_after"]
        == len(dataframe)
    )

    assert isinstance(
        payload["processed_dataframe"],
        pd.DataFrame,
    )


def test_reset_preprocessing_reloads_source_dataset(
    monkeypatch,
):
    dataframe = _dataset()

    persisted = {}

    def fake_load_dataset(project_id, dataset_id):
        return (
            object(),
            object(),
            dataframe.copy(),
        )

    def fake_register_analysis(
        project_id,
        dataset_id,
        stage,
        payload,
    ):
        persisted["payload"] = payload
        persisted["stage"] = stage

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    monkeypatch.setattr(
        callbacks,
        "register_analysis",
        fake_register_analysis,
    )

    comparison, preview, alert = (
        callbacks.reset_preprocessing(
            1,
            1,
            2,
        )
    )

    assert comparison is not None
    assert preview is not None
    assert alert is not None

    assert persisted["stage"] == "eidpp"

    payload = persisted["payload"]

    assert (
        payload["before_metrics"]
        == payload["after_metrics"]
    )

    assert (
        payload["operations"]["imputation"]
        == "none"
    )

    assert (
        payload["operations"]["duplicates"]
        == []
    )


def test_download_uses_persisted_processed_dataframe(
    monkeypatch,
):
    dataframe = _dataset()

    def fake_get_analysis(
        project_id,
        dataset_id,
        stage,
        default=None,
    ):
        assert project_id == 1
        assert dataset_id == 2
        assert stage == "eidpp"

        return {
            "processed_dataframe":
                dataframe.copy()
        }

    def forbidden_load_dataset(*args, **kwargs):
        raise AssertionError(
            "Le dataset source ne doit pas "
            "être rechargé si un résultat "
            "EIDPP existe."
        )

    monkeypatch.setattr(
        callbacks,
        "get_analysis",
        fake_get_analysis,
    )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        forbidden_load_dataset,
    )

    result = (
        callbacks.download_processed_dataset(
            1,
            1,
            2,
        )
    )

    assert result is not None

    assert (
        result.get("filename")
        == "dataset_2_eidpp.csv"
    )


def test_download_falls_back_to_source_dataset(
    monkeypatch,
):
    dataframe = _dataset()

    monkeypatch.setattr(
        callbacks,
        "get_analysis",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        lambda *args, **kwargs: (
            object(),
            object(),
            dataframe.copy(),
        ),
    )

    result = (
        callbacks.download_processed_dataset(
            1,
            1,
            2,
        )
    )

    assert result is not None

    assert (
        result.get("filename")
        == "dataset_2_eidpp.csv"
    )


def test_scale_dataframe_converts_integer_columns_to_float():

    dataframe = pd.DataFrame(
        {
            "age": [18, 20, 22, 24],
            "score": [10, 12, 15, 18],
            "group": ["A", "B", "A", "B"],
        }
    )

    result = callbacks._scale_dataframe(
        dataframe,
        "standard",
    )

    assert result is not dataframe

    assert str(
        result["age"].dtype
    ) == "float64"

    assert str(
        result["score"].dtype
    ) == "float64"

    assert result[
        "group"
    ].tolist() == dataframe[
        "group"
    ].tolist()

    assert str(
        result["group"].dtype
    ) == str(
        dataframe["group"].dtype
    )

    assert dataframe[
        "age"
    ].dtype == "int64"

    assert dataframe[
        "score"
    ].dtype == "int64"
