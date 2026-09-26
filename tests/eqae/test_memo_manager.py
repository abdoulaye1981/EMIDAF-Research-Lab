import pytest

from emidaf_core.eqae import (
    MemoManager,
)


def test_add_analysis_memo():
    manager = MemoManager()

    memo = manager.add_memo(
        title="Première interprétation",
        content=(
            "Le stress semble revenir dans "
            "plusieurs entretiens."
        ),
    )

    assert memo.memo_id

    assert (
        memo.target_type
        == "analysis"
    )

    assert memo.target_id is None

    assert memo.created_at


def test_add_code_memo():
    manager = MemoManager()

    memo = manager.add_memo(
        title="Définition du code",
        content=(
            "Ce code couvre les manifestations "
            "explicites de stress."
        ),
        target_type="code",
        target_id="code-001",
    )

    assert (
        memo.target_type
        == "code"
    )

    assert (
        memo.target_id
        == "code-001"
    )


def test_title_required():
    manager = MemoManager()

    with pytest.raises(ValueError):
        manager.add_memo(
            title=" ",
            content="Contenu",
        )


def test_content_required():
    manager = MemoManager()

    with pytest.raises(ValueError):
        manager.add_memo(
            title="Titre",
            content=" ",
        )


def test_invalid_target_type():
    manager = MemoManager()

    with pytest.raises(ValueError):
        manager.add_memo(
            title="Titre",
            content="Contenu",
            target_type="variable",
            target_id="x",
        )


def test_target_id_required():
    manager = MemoManager()

    with pytest.raises(ValueError):
        manager.add_memo(
            title="Titre",
            content="Contenu",
            target_type="theme",
        )


def test_analysis_target_rejects_id():
    manager = MemoManager()

    with pytest.raises(ValueError):
        manager.add_memo(
            title="Titre",
            content="Contenu",
            target_type="analysis",
            target_id="unexpected",
        )


def test_memos_for_target():
    manager = MemoManager()

    first = manager.add_memo(
        title="Mémo 1",
        content="Observation 1",
        target_type="theme",
        target_id="theme-001",
    )

    manager.add_memo(
        title="Mémo 2",
        content="Observation 2",
        target_type="code",
        target_id="code-001",
    )

    result = manager.memos_for_target(
        target_type="theme",
        target_id="theme-001",
    )

    assert result == [first]


def test_global_analysis_memos():
    manager = MemoManager()

    memo = manager.add_memo(
        title="Synthèse",
        content="Réflexion globale.",
    )

    result = manager.memos_for_target(
        target_type="analysis"
    )

    assert result == [memo]


def test_remove_memo():
    manager = MemoManager()

    memo = manager.add_memo(
        title="Mémo",
        content="Contenu",
    )

    removed = manager.remove_memo(
        memo.memo_id
    )

    assert removed == memo
    assert manager.memos == []


def test_serialization():
    manager = MemoManager()

    manager.add_memo(
        title="Mémo analytique",
        content="Interprétation.",
        author="Chercheur",
    )

    result = manager.to_dict()

    assert len(
        result["memos"]
    ) == 1

    assert (
        result["memos"][0]["title"]
        == "Mémo analytique"
    )

    assert (
        result["memos"][0]["author"]
        == "Chercheur"
    )
