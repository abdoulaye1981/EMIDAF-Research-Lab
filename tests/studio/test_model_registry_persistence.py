"""
=========================================================
Tests EMIDAF - Model Registry Persistence
=========================================================

Vérifie que les résultats analytiques persistent dans
SQLite après vidage du cache mémoire.
=========================================================
"""

from __future__ import annotations

import pytest

from emidaf_studio.services import (
    model_registry,
)


@pytest.fixture
def isolated_registry(
    tmp_path,
    monkeypatch,
):
    """
    Isole complètement le registre analytique dans
    une base SQLite et un workspace temporaires.
    """

    database_path = (
        tmp_path
        / "emidaf_test_registry.db"
    )

    workspace_path = (
        tmp_path
        / "workspace"
    )

    monkeypatch.setenv(
        "EMIDAF_DATABASE_PATH",
        str(database_path),
    )

    monkeypatch.setenv(
        "EMIDAF_WORKSPACE_PATH",
        str(workspace_path),
    )

    # Réinitialisation complète des singletons locaux
    # du registre avant chaque test.
    model_registry._ANALYSIS_RUNS.clear()
    model_registry._BOOTSTRAP = None
    model_registry._REPOSITORY = None

    yield model_registry

    # Nettoyage mémoire.
    model_registry._ANALYSIS_RUNS.clear()

    bootstrap = model_registry._BOOTSTRAP

    if (
        bootstrap is not None
        and hasattr(
            bootstrap,
            "database_manager",
        )
    ):
        bootstrap.database_manager.close()

    model_registry._BOOTSTRAP = None
    model_registry._REPOSITORY = None


def test_analysis_survives_cache_clear(
    isolated_registry,
):
    """
    Simule un redémarrage de Dash :
    écriture -> vidage RAM -> récupération SQLite.
    """

    registry = isolated_registry

    payload = {
        "model_name": "ridge",
        "task": "regression",
        "test_score": 0.84,
    }

    registry.register_analysis(
        101,
        201,
        "eaie",
        payload,
    )

    assert (
        registry.get_analysis(
            101,
            201,
            "eaie",
        )
        == payload
    )

    registry.clear_cache()

    assert (
        registry._ANALYSIS_RUNS
        == {}
    )

    restored = registry.get_analysis(
        101,
        201,
        "eaie",
    )

    assert restored == payload

    assert (
        registry._ANALYSIS_RUNS[
            (101, 201)
        ]["eaie"]
        == payload
    )


def test_merge_analysis_section_survives_cache_clear(
    isolated_registry,
):
    """
    Vérifie qu'un stage composé de plusieurs
    sous-sections est restauré intégralement.
    """

    registry = isolated_registry

    registry.merge_analysis_section(
        102,
        202,
        "ekde",
        "pca",
        {
            "n_components": 2,
            "cumulative_variance_percent": 87.4,
        },
    )

    registry.merge_analysis_section(
        102,
        202,
        "ekde",
        "kmeans",
        {
            "n_clusters": 3,
            "silhouette_score": 0.52,
        },
    )

    registry.clear_cache()

    restored = registry.get_analysis(
        102,
        202,
        "ekde",
    )

    assert set(
        restored
    ) == {
        "pca",
        "kmeans",
    }

    assert (
        restored["pca"][
            "n_components"
        ]
        == 2
    )

    assert (
        restored["kmeans"][
            "n_clusters"
        ]
        == 3
    )


def test_get_all_analyses_restores_all_stages(
    isolated_registry,
):
    """
    Vérifie la restauration de plusieurs stages
    analytiques depuis SQLite.
    """

    registry = isolated_registry

    payloads = {
        "ekde": {
            "kmeans": {
                "n_clusters": 3,
            },
        },
        "eaie": {
            "model_name": "ridge",
        },
        "exaie": {
            "shap": {
                "available": True,
            },
        },
        "edse": {
            "threshold": 0.5,
        },
    }

    for stage, payload in payloads.items():

        registry.register_analysis(
            103,
            203,
            stage,
            payload,
        )

    registry.clear_cache()

    restored = registry.get_all_analyses(
        103,
        203,
    )

    assert restored == payloads

    assert (
        registry._ANALYSIS_RUNS[
            (103, 203)
        ]
        == payloads
    )


def test_clear_all_preserves_sqlite_by_default(
    isolated_registry,
):
    """
    clear_all() sans persistent=True doit uniquement
    vider le cache RAM.
    """

    registry = isolated_registry

    payload = {
        "model_name": "random_forest",
        "test_score": 0.79,
    }

    registry.register_analysis(
        104,
        204,
        "eaie",
        payload,
    )

    registry.clear_all()

    assert (
        registry._ANALYSIS_RUNS
        == {}
    )

    restored = registry.get_analysis(
        104,
        204,
        "eaie",
    )

    assert restored == payload


def test_clear_all_persistent_removes_sqlite(
    isolated_registry,
):
    """
    persistent=True doit supprimer RAM + SQLite.
    """

    registry = isolated_registry

    registry.register_analysis(
        105,
        205,
        "eaie",
        {
            "model_name": "xgboost",
        },
    )

    assert registry.has_analysis(
        105,
        205,
        "eaie",
    )

    registry.clear_all(
        persistent=True,
    )

    assert (
        registry._ANALYSIS_RUNS
        == {}
    )

    assert (
        registry.get_analysis(
            105,
            205,
            "eaie",
        )
        is None
    )

    assert not registry.has_analysis(
        105,
        205,
        "eaie",
    )
