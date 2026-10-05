import pandas as pd
import pytest

from emidaf_core.eaie.roles import (
    FeatureRoles,
    resolve_feature_roles,
)


def _dataset():

    return pd.DataFrame(
        {
            "id_eleve": [
                "ELEVE_1",
                "ELEVE_2",
                "ELEVE_3",
                "ELEVE_4",
            ],
            "genre": [
                "F",
                "M",
                "F",
                "M",
            ],
            "motivation": [
                1,
                2,
                4,
                5,
            ],
            "stress": [
                5,
                4,
                2,
                1,
            ],
            "poste": [
                "Proviseur",
                "Censeur",
                "Proviseur",
                "Censeur",
            ],
            "statut_coherence_parent": [
                "coherent",
                "coherent",
                "incoherent",
                "coherent",
            ],
            "review_text": [
                "Cet élève rencontre des difficultés importantes.",
                "Cet élève progresse régulièrement en mathématiques.",
                "Cet élève manque de confiance en mathématiques.",
                "Cet élève participe activement pendant les cours.",
            ],
            "note_maths": [
                8.0,
                12.0,
                9.0,
                15.0,
            ],
        }
    )


def test_feature_roles_excludes_protected_columns():

    result = FeatureRoles.resolve(
        _dataset(),
        target="note_maths",
        excluded=[
            "poste",
        ],
    )

    assert result.valid is True

    assert (
        "id_eleve"
        in result.identifiers
    )

    assert (
        "review_text"
        in result.text
    )

    assert (
        "statut_coherence_parent"
        in result.quality
    )

    assert (
        "poste"
        in result.excluded
    )

    assert (
        "note_maths"
        not in result.predictors
    )

    assert (
        "id_eleve"
        not in result.predictors
    )

    assert (
        "review_text"
        not in result.predictors
    )

    assert (
        "statut_coherence_parent"
        not in result.predictors
    )

    assert (
        "poste"
        not in result.predictors
    )

    assert result.predictors == [
        "genre",
        "motivation",
        "stress",
    ]


def test_feature_roles_protects_target():

    result = resolve_feature_roles(
        _dataset(),
        target="note_maths",
        excluded=[
            "poste",
        ],
    )

    assert (
        "note_maths"
        in result.protected
    )

    assert (
        "note_maths"
        not in result.predictors
    )


def test_feature_roles_detects_target_conflict():

    result = FeatureRoles.resolve(
        _dataset(),
        target="note_maths",
        excluded=[
            "note_maths",
        ],
    )

    assert result.valid is False

    assert any(
        "cible" in message.lower()
        for message in result.conflicts
    )


def test_feature_roles_rejects_unknown_target():

    with pytest.raises(
        ValueError,
        match="Cible introuvable",
    ):
        FeatureRoles.resolve(
            _dataset(),
            target="variable_absente",
        )


def test_feature_roles_rejects_unknown_exclusion():

    with pytest.raises(
        ValueError,
        match="Variables exclues introuvables",
    ):
        FeatureRoles.resolve(
            _dataset(),
            target="note_maths",
            excluded=[
                "variable_absente",
            ],
        )


def test_feature_roles_to_dict():

    result = FeatureRoles.resolve(
        _dataset(),
        target="note_maths",
        excluded=[
            "poste",
        ],
    )

    payload = result.to_dict()

    assert (
        payload["target"]
        == "note_maths"
    )

    assert (
        payload["predictors"]
        == [
            "genre",
            "motivation",
            "stress",
        ]
    )

    assert payload["valid"] is True
