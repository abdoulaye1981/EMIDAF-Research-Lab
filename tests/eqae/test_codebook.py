import pytest

from emidaf_core.eqae import Codebook


def test_create_codebook():
    codebook = Codebook(
        name="Expérience scolaire",
        description="Analyse des verbatims",
    )

    assert codebook.name == "Expérience scolaire"
    assert codebook.description == "Analyse des verbatims"
    assert codebook.codes == []


def test_codebook_requires_name():
    with pytest.raises(ValueError):
        Codebook(name="   ")


def test_add_code():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    code = codebook.add_code(
        name="Stress scolaire",
        description="Stress lié aux études",
    )

    assert code.name == "Stress scolaire"
    assert code.description == "Stress lié aux études"
    assert code.code_id
    assert len(codebook.codes) == 1


def test_duplicate_code_name_rejected():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    codebook.add_code(
        name="Motivation"
    )

    with pytest.raises(ValueError):
        codebook.add_code(
            name="motivation"
        )


def test_add_child_code():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    parent = codebook.add_code(
        name="Difficultés"
    )

    child = codebook.add_code(
        name="Stress",
        parent_code_id=parent.code_id,
    )

    assert (
        child.parent_code_id
        == parent.code_id
    )


def test_unknown_parent_rejected():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    with pytest.raises(ValueError):
        codebook.add_code(
            name="Stress",
            parent_code_id="unknown",
        )


def test_remove_code():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    code = codebook.add_code(
        name="Motivation"
    )

    removed = codebook.remove_code(
        code.code_id
    )

    assert removed == code
    assert codebook.codes == []


def test_parent_with_children_cannot_be_removed():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    parent = codebook.add_code(
        name="Difficultés"
    )

    codebook.add_code(
        name="Stress",
        parent_code_id=parent.code_id,
    )

    with pytest.raises(ValueError):
        codebook.remove_code(
            parent.code_id
        )


def test_codebook_serialization():
    codebook = Codebook(
        name="Expérience scolaire",
        description="Analyse qualitative",
    )

    codebook.add_code(
        name="Stress scolaire"
    )

    result = codebook.to_dict()

    assert result[
        "name"
    ] == "Expérience scolaire"

    assert result[
        "description"
    ] == "Analyse qualitative"

    assert len(
        result["codes"]
    ) == 1

    assert (
        result["codes"][0]["name"]
        == "Stress scolaire"
    )
