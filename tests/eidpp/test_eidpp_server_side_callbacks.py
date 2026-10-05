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
            {},
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


def test_predictor_columns_exclude_protected_roles():

    dataframe = pd.DataFrame(
        {
            "id_eleve": ["E1", "E2", "E3"],
            "note_maths": [10.0, 12.0, 14.0],
            "age": [15.0, 16.0, 17.0],
            "group": ["A", "B", "A"],
            "statut_audit": [
                "ok",
                "ok",
                "review",
            ],
            "review_text": [
                "texte un",
                "texte deux",
                "texte trois",
            ],
            "poste": [
                "X",
                "Y",
                "Z",
            ],
        }
    )

    roles = {
        "target": "note_maths",
        "identifiers": ["id_eleve"],
        "quality": ["statut_audit"],
        "text": ["review_text"],
        "excluded": ["poste"],
        "protected": [
            "id_eleve",
            "note_maths",
            "statut_audit",
            "review_text",
            "poste",
        ],
        "valid": True,
        "conflicts": [],
    }

    predictors = (
        callbacks._predictor_columns_from_roles(
            dataframe,
            roles,
        )
    )

    assert predictors == [
        "age",
        "group",
    ]


def test_scale_dataframe_respects_selected_columns():

    dataframe = pd.DataFrame(
        {
            "age": [18, 20, 22, 24],
            "note_maths": [10, 12, 15, 18],
            "id_eleve": [
                "E1",
                "E2",
                "E3",
                "E4",
            ],
        }
    )

    result = callbacks._scale_dataframe(
        dataframe,
        "standard",
        columns=["age"],
    )

    # Le prédicteur autorisé est transformé.
    assert str(
        result["age"].dtype
    ) == "float64"

    assert (
        result["age"].tolist()
        != dataframe["age"].tolist()
    )

    # La cible reste strictement inchangée.
    assert result[
        "note_maths"
    ].tolist() == dataframe[
        "note_maths"
    ].tolist()

    assert result[
        "note_maths"
    ].dtype == dataframe[
        "note_maths"
    ].dtype

    # L'identifiant reste strictement inchangé.
    assert result[
        "id_eleve"
    ].tolist() == dataframe[
        "id_eleve"
    ].tolist()


def test_encode_dataframe_respects_selected_columns():

    dataframe = pd.DataFrame(
        {
            "group": [
                "A",
                "B",
                "A",
                "B",
            ],
            "id_eleve": [
                "E1",
                "E2",
                "E3",
                "E4",
            ],
            "statut_audit": [
                "ok",
                "ok",
                "review",
                "ok",
            ],
            "review_text": [
                "texte un",
                "texte deux",
                "texte trois",
                "texte quatre",
            ],
            "poste": [
                "X",
                "Y",
                "X",
                "Y",
            ],
        }
    )

    result = callbacks._encode_dataframe(
        dataframe,
        "onehot",
        columns=["group"],
    )

    # La variable prédictive catégorielle
    # d'origine est remplacée.
    assert "group" not in result.columns

    assert "group_A" in result.columns
    assert "group_B" in result.columns

    # Les colonnes protégées restent présentes
    # et strictement inchangées.
    for column in (
        "id_eleve",
        "statut_audit",
        "review_text",
        "poste",
    ):
        assert column in result.columns

        assert result[
            column
        ].tolist() == dataframe[
            column
        ].tolist()


def test_apply_preprocessing_persists_roles_and_predictors(
    monkeypatch,
):

    dataframe = pd.DataFrame(
        {
            "id_eleve": [
                "E1",
                "E2",
                "E3",
                "E4",
            ],
            "note_maths": [
                10.0,
                12.0,
                14.0,
                16.0,
            ],
            "age": [
                15.0,
                16.0,
                17.0,
                18.0,
            ],
            "group": [
                "A",
                "A",
                "B",
                "B",
            ],
            "statut_audit": [
                "ok",
                "ok",
                "review",
                "ok",
            ],
            "review_text": [
                "texte un",
                "texte deux",
                "texte trois",
                "texte quatre",
            ],
            "poste": [
                "X",
                "Y",
                "X",
                "Y",
            ],
        }
    )

    roles = {
        "target": "note_maths",
        "identifiers": [
            "id_eleve",
        ],
        "quality": [
            "statut_audit",
        ],
        "text": [
            "review_text",
        ],
        "excluded": [
            "poste",
        ],
        "protected": [
            "id_eleve",
            "note_maths",
            "statut_audit",
            "review_text",
            "poste",
        ],
        "valid": True,
        "conflicts": [],
    }

    persisted = {}

    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
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
        callbacks.apply_preprocessing(
            1,
            "none",
            [],
            "none",
            "none",
            "none",
            roles,
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
        payload["variable_roles"]
        == roles
    )

    assert payload[
        "predictor_columns"
    ] == [
        "age",
        "group",
    ]

    processed = payload[
        "processed_dataframe"
    ]

    # Aucune transformation demandée :
    # le dataset doit rester identique.
    pd.testing.assert_frame_equal(
        processed,
        dataframe,
    )


def test_apply_preprocessing_blocks_invalid_roles(
    monkeypatch,
):

    dataframe = _dataset()

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        lambda *args, **kwargs: (
            object(),
            object(),
            dataframe.copy(),
        ),
    )

    invalid_roles = {
        "target": "score",
        "protected": ["score"],
        "valid": False,
        "conflicts": [
            (
                "La cible 'score' est aussi "
                "déclarée comme excluded."
            )
        ],
    }

    comparison, preview, alert = (
        callbacks.apply_preprocessing(
            1,
            "none",
            [],
            "none",
            "none",
            "none",
            invalid_roles,
            1,
            2,
        )
    )

    assert comparison is callbacks.no_update
    assert preview is callbacks.no_update
    assert alert is not None
