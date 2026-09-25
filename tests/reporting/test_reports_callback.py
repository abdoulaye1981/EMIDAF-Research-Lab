import json
from types import SimpleNamespace

import pandas as pd

from emidaf_studio.pages.reports import callbacks


def _section_by_title(payload, title):
    for section in payload["sections"]:
        if section["title"] == title:
            return section

    raise AssertionError(
        f"Section introuvable : {title}"
    )


def test_generate_report_uses_persisted_analyses(
    monkeypatch,
):
    dataframe = pd.DataFrame(
        {
            "x1": [1.0, 2.0, 3.0],
            "x2": [10.0, 20.0, 30.0],
            "target": [0, 1, 0],
        }
    )

    project = SimpleNamespace(
        name="Projet test"
    )

    dataset = SimpleNamespace(
        name="Dataset test"
    )

    native = pd.DataFrame(
        {
            "feature": ["x1", "x2"],
            "importance": [0.7, 0.3],
        }
    )

    permutation = pd.DataFrame(
        {
            "feature": ["x1", "x2"],
            "importance": [0.5, 0.2],
        }
    )

    local_contributions = pd.DataFrame(
        {
            "feature": ["x1", "x2"],
            "contribution": [0.4, -0.1],
        }
    )

    profiles = pd.DataFrame(
        {
            "x1": [1.0, 2.0],
            "prediction": [0, 1],
        }
    )

    scenario_table = pd.DataFrame(
        {
            "probability": [0.2, 0.8],
            "selected": [False, True],
        }
    )

    analyses = {
        "eaie": {
            "model_name": "logistic_regression",
            "task": "classification",
            "target": "target",
            "features": ["x1", "x2"],
            "cv_mean": 0.82,
            "cv_std": 0.03,
            "test_score": 0.80,
            "baseline_cv_mean": 0.60,
            "better_than_baseline": True,
        },
        "exaie": {
            "model_name": "logistic_regression",
            "task": "classification",
            "target": "target",
            "cv_mean": 0.82,
            "cv_std": 0.03,
            "test_score": 0.80,
            "native_importance": native,
            "permutation_importance": permutation,
            "local_explanation": {
                "available": True,
                "row": 0,
                "prediction": 0,
                "contributions": local_contributions,
            },
            "summary": {
                "native_interpretation": (
                    "Importance native persistée."
                ),
                "permutation_interpretation": (
                    "Importance par permutation persistée."
                ),
            },
            "shap": {
                "available": True,
                "model_name": "logistic_regression",
                "explainer_type": "LinearExplainer",
                "n_observations": 3,
                "feature_importance": {
                    "x1": 0.42,
                    "x2": 0.18,
                },
                "local_explanation": {
                    "row": 0,
                    "prediction": 0,
                    "contributions": {
                        "x1": 0.31,
                        "x2": -0.07,
                    },
                },
                "output_names": [
                    "classe_0",
                    "classe_1",
                ],
            },
            "predictive_warning": None,
            "limitations": [
                (
                    "Les importances ne constituent "
                    "pas une preuve de causalité."
                )
            ],
        },
        "edse": {
            "model_name": "logistic_regression",
            "task": "classification",
            "target": "target",
            "threshold": 0.50,
            "direction": "above",
            "summary": {
                "assessment": {
                    "evaluable": True,
                    "reliable": True,
                    "level": "acceptable",
                    "warnings": [],
                }
            },
            "scenario": {
                "summary": {
                    "observations": 2,
                    "selected": 1,
                    "not_selected": 1,
                    "selected_rate": 0.5,
                },
                "table": scenario_table,
                "interpretation": (
                    "Scénario persistant."
                ),
            },
            "profiles": profiles,
        },
    }

    def fake_load_dataset(
        project_id,
        dataset_id,
    ):
        assert project_id == 10
        assert dataset_id == 20

        return (
            project,
            dataset,
            dataframe,
        )

    def fake_get_all_analyses(
        project_id,
        dataset_id,
    ):
        assert project_id == 10
        assert dataset_id == 20

        return analyses

    monkeypatch.setattr(
        callbacks,
        "load_dataset",
        fake_load_dataset,
    )

    monkeypatch.setattr(
        callbacks,
        "get_all_analyses",
        fake_get_all_analyses,
    )

    (
        status,
        preview,
        content,
        filename,
        disabled,
    ) = callbacks.generate_report(
        1,
        "Rapport test",
        [
            "eaie",
            "exaie",
            "edse",
        ],
        "json",
        10,
        20,
    )

    assert content is not None
    assert filename.endswith(".json")
    assert disabled is False
    assert preview

    payload = json.loads(content)

    eaie = _section_by_title(
        payload,
        "Modélisation prédictive",
    )

    assert (
        eaie["data"]["baseline_cv_mean"]
        == 0.60
    )
    assert (
        eaie["data"]["better_than_baseline"]
        is True
    )

    exaie = _section_by_title(
        payload,
        "Explicabilité des modèles",
    )

    assert (
        "importance_native"
        in exaie["data"]
    )
    assert (
        "importance_permutation"
        in exaie["data"]
    )
    assert (
        "local_explanation"
        in exaie["data"]
    )

    assert "shap" in exaie["data"]

    assert (
        exaie["data"]["shap"][
            "available"
        ]
        is True
    )

    assert (
        exaie["data"]["shap"][
            "explainer_type"
        ]
        == "LinearExplainer"
    )

    assert (
        exaie["data"]["shap"][
            "feature_importance"
        ]["x1"]
        == 0.42
    )

    edse = _section_by_title(
        payload,
        "Aide à la décision",
    )

    assert "scenario" in edse["data"]
    assert "profiles" in edse["data"]

    assert (
        edse["category"]
        == "decision_support"
    )


def test_stage_unavailable_does_not_claim_session_only():
    result = callbacks._stage_unavailable(
        "EAIE"
    )

    assert (
        result["status"]
        == "non_disponible"
    )

    assert (
        "session actuelle"
        not in result["message"]
    )

    assert (
        "jeu de données"
        in result["message"]
    )


def test_compact_ekde_removes_verbose_clustering_outputs():

    original = {
        "kmeans": {
            "n_clusters": 3,
            "n_observations": 1200,
            "silhouette_score": 0.51,
            "cluster_sizes": [
                {"Cluster": 1, "Effectif": 400},
                {"Cluster": 2, "Effectif": 420},
                {"Cluster": 3, "Effectif": 380},
            ],
            "labels": [1, 2, 3, 1],
            "cluster_centers": [
                [0.1, 0.2],
                [0.3, 0.4],
                [0.5, 0.6],
            ],
        },
        "dbscan": {
            "n_clusters": 2,
            "noise_count": 12,
            "noise_percentage": 1.0,
            "labels": [0, 0, 1, -1],
        },
        "agglomerative": {
            "n_clusters": 3,
            "linkage": "ward",
            "silhouette_score": 0.44,
            "labels": [1, 2, 3, 1],
        },
    }

    compact = callbacks._compact_ekde_for_report(
        original
    )

    assert "labels" not in compact["kmeans"]
    assert "cluster_centers" not in compact["kmeans"]
    assert compact["kmeans"]["silhouette_score"] == 0.51
    assert "cluster_sizes" in compact["kmeans"]

    assert "labels" not in compact["dbscan"]
    assert compact["dbscan"]["noise_count"] == 12

    assert "labels" not in compact["agglomerative"]
    assert compact["agglomerative"]["linkage"] == "ward"


def test_compact_ekde_preserves_pca_information():

    original = {
        "pca": {
            "n_components": 2,
            "numeric_variables": ["x1", "x2"],
            "explained_variance": [
                {
                    "Composante": "PC1",
                    "Variance expliquée": 62.5,
                    "Variance cumulée": 62.5,
                },
                {
                    "Composante": "PC2",
                    "Variance expliquée": 24.3,
                    "Variance cumulée": 86.8,
                },
            ],
            "cumulative_variance_percent": 86.8,
        },
    }

    compact = callbacks._compact_ekde_for_report(
        original
    )

    assert (
        compact["pca"]["explained_variance"]
        == original["pca"]["explained_variance"]
    )

    assert (
        compact["pca"]["cumulative_variance_percent"]
        == 86.8
    )


def test_compact_ekde_removes_internal_selector_repr():

    original = {
        "selection": {
            "method": "variance",
            "target": None,
            "variance_threshold": 0.2,
            "numeric_variables": ["x1", "x2"],
            "result": [
                {
                    "Résultat": (
                        "VarianceThreshold("
                        "threshold=0.2)"
                    )
                }
            ],
        },
    }

    compact = callbacks._compact_ekde_for_report(
        original
    )

    selection = compact["selection"]

    assert selection["method"] == "variance"
    assert selection["variance_threshold"] == 0.2
    assert "result" not in selection


def test_compact_ekde_keeps_scientific_selection_rows():

    original = {
        "selection": {
            "method": "mutual_information",
            "target": "target",
            "result": [
                {
                    "Variable": "x1",
                    "Score": 0.81,
                },
                {
                    "Variable": "x2",
                    "Score": 0.34,
                },
            ],
        },
    }

    compact = callbacks._compact_ekde_for_report(
        original
    )

    assert (
        compact["selection"]["result"]
        == original["selection"]["result"]
    )


def test_compact_ekde_does_not_modify_original_context():

    original = {
        "kmeans": {
            "n_clusters": 2,
            "labels": [1, 2, 1],
            "cluster_centers": [
                [0.1],
                [0.9],
            ],
        },
    }

    compact = callbacks._compact_ekde_for_report(
        original
    )

    assert "labels" not in compact["kmeans"]
    assert "cluster_centers" not in compact["kmeans"]

    assert original["kmeans"]["labels"] == [1, 2, 1]

    assert (
        original["kmeans"]["cluster_centers"]
        == [
            [0.1],
            [0.9],
        ]
    )
