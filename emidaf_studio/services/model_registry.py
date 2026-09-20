from __future__ import annotations

from typing import Any
from threading import RLock

from emidaf_core.bootstrap import Bootstrap


# ==========================================================
# Cache mémoire
# ==========================================================

_ANALYSIS_RUNS: dict[
    tuple[int, int],
    dict[str, Any],
] = {}


# Protège les opérations lecture -> fusion -> écriture.
_REGISTRY_LOCK = RLock()


# ==========================================================
# Repository persistant
# ==========================================================

_BOOTSTRAP = None
_REPOSITORY = None


def _repository():
    """
    Retourne paresseusement le repository SQLite.

    Le chargement différé évite d'initialiser la base
    tant que le registre n'est pas réellement utilisé.
    """

    global _BOOTSTRAP
    global _REPOSITORY

    if _REPOSITORY is None:

        _BOOTSTRAP = Bootstrap()
        _BOOTSTRAP.initialize()

        _REPOSITORY = (
            _BOOTSTRAP.analysis_result_repository
        )

    return _REPOSITORY


def _key(
    project_id: int,
    dataset_id: int,
) -> tuple[int, int]:

    return (
        int(project_id),
        int(dataset_id),
    )


def _stage(stage: str) -> str:

    value = str(stage).strip().lower()

    if not value:
        raise ValueError(
            "Le nom de l'étape analytique "
            "ne peut pas être vide."
        )

    return value


# ==========================================================
# API analytique générique
# ==========================================================

def register_analysis(
    project_id: int,
    dataset_id: int,
    stage: str,
    payload: Any,
) -> None:
    """
    Enregistre un résultat dans le cache et SQLite.
    L'écriture est protégée contre les accès concurrents.
    """

    project_id = int(project_id)
    dataset_id = int(dataset_id)
    stage = _stage(stage)

    key = _key(
        project_id,
        dataset_id,
    )

    with _REGISTRY_LOCK:

        if key not in _ANALYSIS_RUNS:
            _ANALYSIS_RUNS[key] = {}

        _ANALYSIS_RUNS[
            key
        ][stage] = payload

        _repository().upsert(
            project_id,
            dataset_id,
            stage,
            payload,
        )


def get_analysis(
    project_id: int,
    dataset_id: int,
    stage: str,
    default=None,
):
    """
    Lit d'abord le cache.

    Si le résultat n'est plus en mémoire
    (par exemple après redémarrage de Dash),
    il est restauré depuis SQLite.
    """

    project_id = int(project_id)
    dataset_id = int(dataset_id)
    stage = _stage(stage)

    key = _key(
        project_id,
        dataset_id,
    )

    cached = (
        _ANALYSIS_RUNS
        .get(key, {})
    )

    if stage in cached:
        return cached[stage]

    payload = _repository().get(
        project_id,
        dataset_id,
        stage,
    )

    if payload is None:
        return default

    if key not in _ANALYSIS_RUNS:
        _ANALYSIS_RUNS[key] = {}

    _ANALYSIS_RUNS[key][stage] = payload

    return payload



def merge_analysis_section(
    project_id: int,
    dataset_id: int,
    stage: str,
    section: str,
    payload: Any,
) -> dict[str, Any]:
    """
    Fusionne atomiquement une sous-section dans un stage.

    Exemple :
        elae -> descriptive
        elae -> correlations
        ekde -> pca
    """

    project_id = int(project_id)
    dataset_id = int(dataset_id)
    stage = _stage(stage)

    section = str(section).strip()

    if not section:
        raise ValueError(
            "Le nom de la sous-section analytique "
            "ne peut pas être vide."
        )

    with _REGISTRY_LOCK:

        current = (
            get_analysis(
                project_id,
                dataset_id,
                stage,
                default={},
            )
            or {}
        )

        if not isinstance(current, dict):
            current = {}

        merged = dict(current)

        merged[section] = payload

        register_analysis(
            project_id,
            dataset_id,
            stage,
            merged,
        )

        return merged


def has_analysis(
    project_id: int,
    dataset_id: int,
    stage: str,
) -> bool:

    project_id = int(project_id)
    dataset_id = int(dataset_id)
    stage = _stage(stage)

    key = _key(
        project_id,
        dataset_id,
    )

    if (
        stage
        in _ANALYSIS_RUNS.get(
            key,
            {},
        )
    ):
        return True

    return _repository().exists(
        project_id,
        dataset_id,
        stage,
    )


def get_all_analyses(
    project_id: int,
    dataset_id: int,
) -> dict[str, Any]:
    """
    Retourne tous les résultats disponibles
    pour un jeu de données.

    SQLite constitue la source persistante.
    Le cache est synchronisé avec le résultat.
    """

    project_id = int(project_id)
    dataset_id = int(dataset_id)

    key = _key(
        project_id,
        dataset_id,
    )

    persisted = _repository().get_all(
        project_id,
        dataset_id,
    )

    cached = _ANALYSIS_RUNS.get(
        key,
        {},
    )

    combined = {
        **persisted,
        **cached,
    }

    if combined:
        _ANALYSIS_RUNS[key] = dict(
            combined
        )

    return dict(combined)


def clear_analysis(
    project_id: int,
    dataset_id: int,
    stage: str | None = None,
) -> None:
    """
    Supprime un résultat du cache et de SQLite.

    Si stage=None, tous les résultats du jeu
    de données sont supprimés.
    """

    project_id = int(project_id)
    dataset_id = int(dataset_id)

    key = _key(
        project_id,
        dataset_id,
    )

    if stage is None:

        _ANALYSIS_RUNS.pop(
            key,
            None,
        )

        _repository().delete_dataset(
            project_id,
            dataset_id,
        )

        return

    stage = _stage(stage)

    payload = _ANALYSIS_RUNS.get(
        key
    )

    if payload is not None:

        payload.pop(
            stage,
            None,
        )

        if not payload:
            _ANALYSIS_RUNS.pop(
                key,
                None,
            )

    _repository().delete(
        project_id,
        dataset_id,
        stage,
    )


def clear_cache() -> None:
    """
    Vide seulement le cache RAM.

    Les résultats SQLite sont conservés.
    Cette fonction permet de simuler un
    redémarrage de Dash dans les tests.
    """

    _ANALYSIS_RUNS.clear()


def clear_all(
    *,
    persistent: bool = False,
) -> None:
    """
    Vide le cache.

    persistent=True supprime également tous
    les résultats analytiques enregistrés
    dans SQLite.

    La valeur par défaut protège les résultats
    persistants.
    """

    clear_cache()

    if persistent:
        _repository().delete_all()


# ==========================================================
# Compatibilité EAIE
# ==========================================================

def register_eaie_run(
    project_id: int,
    dataset_id: int,
    context: dict[str, Any],
) -> None:

    register_analysis(
        project_id,
        dataset_id,
        "eaie",
        context,
    )


def get_eaie_run(
    project_id: int,
    dataset_id: int,
):

    return get_analysis(
        project_id,
        dataset_id,
        "eaie",
    )


def has_eaie_run(
    project_id: int,
    dataset_id: int,
) -> bool:

    return has_analysis(
        project_id,
        dataset_id,
        "eaie",
    )


def clear_eaie_run(
    project_id: int,
    dataset_id: int,
) -> None:

    clear_analysis(
        project_id,
        dataset_id,
        "eaie",
    )
