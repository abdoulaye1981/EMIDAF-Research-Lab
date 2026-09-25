"""
=========================================================
EMIDAF Studio - Router access tests
=========================================================

Vérifie les protections transversales du routeur :
- authentification ;
- propriété du projet ;
- existence du dataset ;
- appartenance du dataset au projet ;
- poursuite du routage lorsque l'accès est valide.
=========================================================
"""

from __future__ import annotations

import sys
from types import ModuleType
from types import SimpleNamespace

from dash import dcc

import emidaf_studio.router as router


# =========================================================
# HELPERS
# =========================================================

def _component_text(component) -> str:
    """
    Extrait récursivement le texte visible d'un
    composant Dash.
    """

    if component is None:
        return ""

    if isinstance(component, str):
        return component

    if isinstance(component, (list, tuple)):
        return " ".join(
            _component_text(item)
            for item in component
        )

    children = getattr(
        component,
        "children",
        None,
    )

    return _component_text(children)


def _user(
    user_id: int = 1,
):
    return SimpleNamespace(
        id=user_id,
        role="user",
    )


def _bootstrap(
    *,
    owns_project: bool,
    dataset=None,
):
    project_controller = SimpleNamespace(
        exists_for_user=lambda project_id, user_id: (
            owns_project
        )
    )

    dataset_controller = SimpleNamespace(
        get=lambda dataset_id: dataset
    )

    return SimpleNamespace(
        project_controller=project_controller,
        dataset_controller=dataset_controller,
    )


# =========================================================
# AUTHENTICATION
# =========================================================

def test_private_route_redirects_to_login_when_unauthenticated(
    monkeypatch,
):
    monkeypatch.setattr(
        router,
        "_current_user",
        lambda: None,
    )

    result = router.get_page_layout(
        "/projects"
    )

    assert isinstance(
        result,
        dcc.Location,
    )

    assert result.href == "/login"


# =========================================================
# PROJECT ACCESS
# =========================================================

def test_project_route_rejects_project_not_owned_by_user(
    monkeypatch,
):
    monkeypatch.setattr(
        router,
        "_current_user",
        lambda: _user(),
    )

    monkeypatch.setattr(
        router,
        "_auth_bootstrap",
        lambda: _bootstrap(
            owns_project=False,
        ),
    )

    result = router.get_page_layout(
        "/projects/10/datasets/20/eaie"
    )

    text = _component_text(result)

    assert "Accès non autorisé" in text

    assert (
        "Ce projet n'appartient pas"
        in text
    )


# =========================================================
# DATASET ACCESS
# =========================================================

def test_dataset_route_rejects_missing_dataset(
    monkeypatch,
):
    monkeypatch.setattr(
        router,
        "_current_user",
        lambda: _user(),
    )

    monkeypatch.setattr(
        router,
        "_auth_bootstrap",
        lambda: _bootstrap(
            owns_project=True,
            dataset=None,
        ),
    )

    result = router.get_page_layout(
        "/projects/10/datasets/999/eaie"
    )

    text = _component_text(result)

    assert "Dataset introuvable" in text

    assert (
        "n'existe pas dans le projet demandé"
        in text
    )


def test_dataset_route_rejects_dataset_from_another_project(
    monkeypatch,
):
    dataset = SimpleNamespace(
        id=20,
        project_id=11,
    )

    monkeypatch.setattr(
        router,
        "_current_user",
        lambda: _user(),
    )

    monkeypatch.setattr(
        router,
        "_auth_bootstrap",
        lambda: _bootstrap(
            owns_project=True,
            dataset=dataset,
        ),
    )

    result = router.get_page_layout(
        "/projects/10/datasets/20/eaie"
    )

    text = _component_text(result)

    assert "Dataset introuvable" in text

    assert (
        "n'existe pas dans le projet demandé"
        in text
    )


# =========================================================
# VALID ROUTING
# =========================================================

def test_dataset_route_continues_when_dataset_belongs_to_project(
    monkeypatch,
):
    dataset = SimpleNamespace(
        id=20,
        project_id=10,
    )

    monkeypatch.setattr(
        router,
        "_current_user",
        lambda: _user(),
    )

    monkeypatch.setattr(
        router,
        "_auth_bootstrap",
        lambda: _bootstrap(
            owns_project=True,
            dataset=dataset,
        ),
    )

    sentinel = object()

    fake_module = ModuleType(
        "emidaf_studio.pages.eaie.layout"
    )

    fake_module.eaie_layout = (
        lambda project_id, dataset_id: (
            sentinel
            if (
                project_id == 10
                and dataset_id == 20
            )
            else None
        )
    )

    monkeypatch.setitem(
        sys.modules,
        "emidaf_studio.pages.eaie.layout",
        fake_module,
    )

    result = router.get_page_layout(
        "/projects/10/datasets/20/eaie"
    )

    assert result is sentinel
