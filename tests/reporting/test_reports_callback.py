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
