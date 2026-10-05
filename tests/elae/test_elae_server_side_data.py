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
                datatypes={
                    "numeric": ["x", "y"],
                    "categorical": [],
                    "boolean": [],
                    "text": [],
                    "identifier": [],
                    "datetime": [],
                },
                correlations={
                    "correlation_matrix": (
                        correlation_matrix
                    )
                },
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


def test_semantic_numeric_columns_excludes_boolean_and_identifier(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "score": [10.0, 12.0, 14.0],
            "binary_flag": [0, 1, 0],
            "id_student": ["A", "B", "C"],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_datatypes",
        lambda df: {
            "numeric": ["score"],
            "boolean": ["binary_flag"],
            "identifier": ["id_student"],
            "categorical": [],
            "text": [],
        },
    )

    result = callbacks._semantic_numeric_columns(
        dataframe
    )

    assert result == ["score"]


def test_semantic_group_columns_accepts_categorical_and_boolean(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "cycle": ["Moyen", "Secondaire", "Moyen"],
            "binary_flag": [0, 1, 0],
            "score": [10.0, 12.0, 14.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_datatypes",
        lambda df: {
            "numeric": ["score"],
            "categorical": ["cycle"],
            "boolean": ["binary_flag"],
            "identifier": [],
            "text": [],
        },
    )

    result = callbacks._semantic_group_columns(
        dataframe
    )

    assert result == [
        "cycle",
        "binary_flag",
    ]


def test_univariate_rejects_identifier(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "id_student": ["A", "B", "C"],
            "score": [10.0, 12.0, 14.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_datatypes",
        lambda df: {
            "numeric": ["score"],
            "categorical": [],
            "boolean": [],
            "identifier": ["id_student"],
            "text": [],
        },
    )

    summary, figure = callbacks.univariate(
        "univariate",
        "id_student",
        10,
        20,
    )

    assert summary is not None
    assert figure == {}


def test_univariate_rejects_free_text(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "texte un",
                "texte deux",
                "texte trois",
            ],
            "score": [10.0, 12.0, 14.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_datatypes",
        lambda df: {
            "numeric": ["score"],
            "categorical": [],
            "boolean": [],
            "identifier": [],
            "text": ["review_text"],
        },
    )

    summary, figure = callbacks.univariate(
        "univariate",
        "review_text",
        10,
        20,
    )

    assert summary is not None
    assert figure == {}


def test_univariate_boolean_is_not_treated_as_numeric(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "binary_flag": [0, 1, 1, 0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_datatypes",
        lambda df: {
            "numeric": [],
            "categorical": [],
            "boolean": ["binary_flag"],
            "identifier": [],
            "text": [],
        },
    )

    persisted = []

    monkeypatch.setattr(
        callbacks,
        "_persist_elae",
        lambda *args: persisted.append(args),
    )

    callbacks.univariate(
        "univariate",
        "binary_flag",
        10,
        20,
    )

    assert persisted

    payload = persisted[0][3]

    assert payload["type"] == "categorical"
    assert payload["unique"] == 2


def test_bivariate_rejects_identifier(
    monkeypatch,
):
    from types import SimpleNamespace

    dataframe = pd.DataFrame(
        {
            "id_student": ["A", "B", "C"],
            "score": [10.0, 12.0, 14.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    class FakeProfiler:
        def profile(self, data):
            return SimpleNamespace(
                datatypes={
                    "numeric": ["score"],
                    "categorical": [],
                    "boolean": [],
                    "text": [],
                    "identifier": ["id_student"],
                    "datetime": [],
                    "semantic": {
                        "ordinal": [],
                    },
                },
                correlations={
                    "adaptive_pairs": [],
                },
            )

    monkeypatch.setattr(
        callbacks,
        "DatasetProfiler",
        FakeProfiler,
    )

    summary, figure = callbacks.bivariate(
        "bivariate",
        "id_student",
        "score",
        10,
        20,
    )

    assert summary is not None
    assert figure == {}


def test_grouped_analysis_rejects_identifier_as_group(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "id_student": ["A", "B", "C"],
            "score": [10.0, 12.0, 14.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_group_columns",
        lambda df: [],
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_numeric_columns",
        lambda df: ["score"],
    )

    summary, figure = callbacks.grouped_analysis(
        "grouped",
        "id_student",
        "score",
        10,
        20,
    )

    assert summary is not None
    assert figure == {}


def test_grouped_analysis_rejects_boolean_as_numeric_value(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "cycle": ["Moyen", "Secondaire", "Moyen"],
            "binary_flag": [0, 1, 0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_group_columns",
        lambda df: ["cycle", "binary_flag"],
    )

    monkeypatch.setattr(
        callbacks,
        "_semantic_numeric_columns",
        lambda df: [],
    )

    summary, figure = callbacks.grouped_analysis(
        "grouped",
        "cycle",
        "binary_flag",
        10,
        20,
    )

    assert summary is not None
    assert figure == {}



def test_bivariate_ordinal_numeric_uses_spearman_and_boxplot(
    monkeypatch,
):
    from types import SimpleNamespace

    dataframe = pd.DataFrame(
        {
            "motivation": [1, 2, 3, 4, 5],
            "note_maths": [6.0, 8.0, 10.0, 13.0, 16.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    class FakeProfiler:
        def profile(self, data):
            return SimpleNamespace(
                datatypes={
                    "numeric": [
                        "motivation",
                        "note_maths",
                    ],
                    "categorical": [],
                    "boolean": [],
                    "text": [],
                    "identifier": [],
                    "datetime": [],
                    "semantic": {
                        "ordinal": [
                            "motivation",
                        ],
                    },
                },
                correlations={
                    "adaptive_pairs": [
                        {
                            "variable_1": "motivation",
                            "variable_2": "note_maths",
                            "correlation": 0.3141,
                            "method": "spearman",
                            "reason": "ordinal_variable",
                        }
                    ],
                },
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

    summary, figure = callbacks.bivariate(
        "bivariate",
        "motivation",
        "note_maths",
        10,
        20,
    )

    assert summary is not None
    assert figure is not None
    assert figure.data
    assert figure.data[0].type == "box"

    assert persisted

    payload = persisted[0][3]

    assert (
        payload["relationship_type"]
        == "ordinal_numeric"
    )
    assert payload["correlation"] == 0.3141
    assert (
        payload["correlation_method"]
        == "spearman"
    )
    assert (
        payload["correlation_reason"]
        == "ordinal_variable"
    )
    assert "pearson_correlation" not in payload


def test_bivariate_non_normal_numeric_pair_uses_spearman(
    monkeypatch,
):
    from types import SimpleNamespace

    dataframe = pd.DataFrame(
        {
            "exercices_semaine": [0, 1, 3, 7, 12],
            "note_maths": [7.0, 9.0, 11.0, 13.0, 15.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    class FakeProfiler:
        def profile(self, data):
            return SimpleNamespace(
                datatypes={
                    "numeric": [
                        "exercices_semaine",
                        "note_maths",
                    ],
                    "categorical": [],
                    "boolean": [],
                    "text": [],
                    "identifier": [],
                    "datetime": [],
                    "semantic": {
                        "ordinal": [],
                    },
                },
                correlations={
                    "adaptive_pairs": [
                        {
                            "variable_1": "exercices_semaine",
                            "variable_2": "note_maths",
                            "correlation": 0.1029,
                            "method": "spearman",
                            "reason": "normality_not_confirmed",
                        }
                    ],
                },
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

    summary, figure = callbacks.bivariate(
        "bivariate",
        "exercices_semaine",
        "note_maths",
        10,
        20,
    )

    assert summary is not None
    assert figure is not None
    assert figure.data
    assert figure.data[0].type == "scatter"

    payload = persisted[0][3]

    assert (
        payload["relationship_type"]
        == "numeric_numeric"
    )
    assert payload["correlation"] == 0.1029
    assert (
        payload["correlation_method"]
        == "spearman"
    )
    assert (
        payload["correlation_reason"]
        == "normality_not_confirmed"
    )


def test_bivariate_normal_numeric_pair_uses_pearson(
    monkeypatch,
):
    from types import SimpleNamespace

    dataframe = pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0, 4.0, 5.0],
            "y": [2.0, 4.0, 5.0, 8.0, 10.0],
        }
    )

    monkeypatch.setattr(
        callbacks,
        "_load_elae_dataframe",
        lambda project_id, dataset_id: dataframe,
    )

    class FakeProfiler:
        def profile(self, data):
            return SimpleNamespace(
                datatypes={
                    "numeric": ["x", "y"],
                    "categorical": [],
                    "boolean": [],
                    "text": [],
                    "identifier": [],
                    "datetime": [],
                    "semantic": {
                        "ordinal": [],
                    },
                },
                correlations={
                    "adaptive_pairs": [
                        {
                            "variable_1": "x",
                            "variable_2": "y",
                            "correlation": 0.9876,
                            "method": "pearson",
                            "reason": (
                                "both_variables_compatible_"
                                "with_normality"
                            ),
                        }
                    ],
                },
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

    summary, figure = callbacks.bivariate(
        "bivariate",
        "x",
        "y",
        10,
        20,
    )

    assert summary is not None
    assert figure is not None
    assert figure.data
    assert figure.data[0].type == "scatter"

    payload = persisted[0][3]

    assert (
        payload["relationship_type"]
        == "numeric_numeric"
    )
    assert payload["correlation"] == 0.9876
    assert (
        payload["correlation_method"]
        == "pearson"
    )
    assert (
        payload["correlation_reason"]
        == (
            "both_variables_compatible_"
            "with_normality"
        )
    )
    assert "pearson_correlation" not in payload
