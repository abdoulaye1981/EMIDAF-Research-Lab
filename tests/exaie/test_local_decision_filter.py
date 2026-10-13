from emidaf_studio.pages.exaie.callbacks import (
    _classification_decision,
)


def test_vrai_positif():
    assert (
        _classification_decision(
            1,
            1,
            1,
        )
        == "tp"
    )


def test_faux_negatif():
    assert (
        _classification_decision(
            1,
            0,
            1,
        )
        == "fn"
    )


def test_faux_positif():
    assert (
        _classification_decision(
            0,
            1,
            1,
        )
        == "fp"
    )


def test_vrai_negatif():
    assert (
        _classification_decision(
            0,
            0,
            1,
        )
        == "tn"
    )


def test_respecte_classe_positive_non_standard():
    assert (
        _classification_decision(
            "difficulte",
            "difficulte",
            "difficulte",
        )
        == "tp"
    )

    assert (
        _classification_decision(
            "difficulte",
            "normal",
            "difficulte",
        )
        == "fn"
    )
