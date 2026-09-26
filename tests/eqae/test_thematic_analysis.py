import pytest

from emidaf_core.eqae import (
    Codebook,
    ThematicAnalysis,
)


def build_analysis():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    stress = codebook.add_code(
        name="Stress"
    )

    motivation = codebook.add_code(
        name="Motivation"
    )

    analysis = ThematicAnalysis(
        codebook
    )

    return (
        codebook,
        stress,
        motivation,
        analysis,
    )


def test_add_theme():
    _, _, _, analysis = (
        build_analysis()
    )

    theme = analysis.add_theme(
        name="Bien-être scolaire"
    )

    assert theme.theme_id
    assert (
        theme.name
        == "Bien-être scolaire"
    )


def test_add_subtheme():
    _, _, _, analysis = (
        build_analysis()
    )

    parent = analysis.add_theme(
        name="Bien-être scolaire"
    )

    child = analysis.add_theme(
        name="Stress académique",
        parent_theme_id=parent.theme_id,
    )

    assert (
        child.parent_theme_id
        == parent.theme_id
    )


def test_unknown_parent_theme_rejected():
    _, _, _, analysis = (
        build_analysis()
    )

    with pytest.raises(ValueError):
        analysis.add_theme(
            name="Stress",
            parent_theme_id="unknown",
        )


def test_link_code_to_theme():
    _, stress, _, analysis = (
        build_analysis()
    )

    theme = analysis.add_theme(
        name="Difficultés scolaires"
    )

    analysis.link_code(
        theme_id=theme.theme_id,
        code_id=stress.code_id,
    )

    assert (
        stress.code_id
        in analysis.codes_for_theme(
            theme.theme_id
        )
    )


def test_unknown_code_rejected():
    _, _, _, analysis = (
        build_analysis()
    )

    theme = analysis.add_theme(
        name="Difficultés scolaires"
    )

    with pytest.raises(ValueError):
        analysis.link_code(
            theme_id=theme.theme_id,
            code_id="unknown",
        )


def test_multiple_codes_for_theme():
    _, stress, motivation, analysis = (
        build_analysis()
    )

    theme = analysis.add_theme(
        name="Expérience scolaire"
    )

    analysis.link_code(
        theme_id=theme.theme_id,
        code_id=stress.code_id,
    )

    analysis.link_code(
        theme_id=theme.theme_id,
        code_id=motivation.code_id,
    )

    assert len(
        analysis.codes_for_theme(
            theme.theme_id
        )
    ) == 2


def test_child_themes():
    _, _, _, analysis = (
        build_analysis()
    )

    parent = analysis.add_theme(
        name="Expérience scolaire"
    )

    child = analysis.add_theme(
        name="Stress académique",
        parent_theme_id=parent.theme_id,
    )

    children = analysis.child_themes(
        parent.theme_id
    )

    assert children == [child]


def test_parent_theme_cannot_be_removed():
    _, _, _, analysis = (
        build_analysis()
    )

    parent = analysis.add_theme(
        name="Expérience scolaire"
    )

    analysis.add_theme(
        name="Stress",
        parent_theme_id=parent.theme_id,
    )

    with pytest.raises(ValueError):
        analysis.remove_theme(
            parent.theme_id
        )


def test_thematic_analysis_serialization():
    _, stress, _, analysis = (
        build_analysis()
    )

    theme = analysis.add_theme(
        name="Difficultés scolaires"
    )

    analysis.link_code(
        theme_id=theme.theme_id,
        code_id=stress.code_id,
    )

    result = analysis.to_dict()

    assert len(
        result["themes"]
    ) == 1

    assert (
        result["themes"][0]["name"]
        == "Difficultés scolaires"
    )

    assert (
        stress.code_id
        in result["themes"][0]["code_ids"]
    )
