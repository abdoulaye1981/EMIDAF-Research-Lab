import pytest

from emidaf_core.eqae import (
    Codebook,
    QualitativeCoder,
    QualitativeSegment,
)


def build_objects():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    code = codebook.add_code(
        name="Stress scolaire"
    )

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé avant les examens.",
    )

    coder = QualitativeCoder(
        codebook
    )

    return (
        codebook,
        code,
        segment,
        coder,
    )


def test_assign_code():
    _, code, segment, coder = (
        build_objects()
    )

    assignment = coder.assign_code(
        segment=segment,
        code_id=code.code_id,
    )

    assert (
        assignment.segment_id
        == segment.segment_id
    )

    assert (
        assignment.code_id
        == code.code_id
    )

    assert assignment.mode == "manual"


def test_unknown_code_rejected():
    _, _, segment, coder = (
        build_objects()
    )

    with pytest.raises(ValueError):
        coder.assign_code(
            segment=segment,
            code_id="unknown",
        )


def test_invalid_mode_rejected():
    _, code, segment, coder = (
        build_objects()
    )

    with pytest.raises(ValueError):
        coder.assign_code(
            segment=segment,
            code_id=code.code_id,
            mode="automatic",
        )


def test_duplicate_assignment_rejected():
    _, code, segment, coder = (
        build_objects()
    )

    coder.assign_code(
        segment=segment,
        code_id=code.code_id,
    )

    with pytest.raises(ValueError):
        coder.assign_code(
            segment=segment,
            code_id=code.code_id,
        )


def test_multiple_codes_on_same_segment():
    codebook, code, segment, coder = (
        build_objects()
    )

    motivation = codebook.add_code(
        name="Motivation"
    )

    coder.assign_code(
        segment=segment,
        code_id=code.code_id,
    )

    coder.assign_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    assignments = (
        coder.assignments_for_segment(
            segment.segment_id
        )
    )

    assert len(assignments) == 2


def test_remove_assignment():
    _, code, segment, coder = (
        build_objects()
    )

    assignment = coder.assign_code(
        segment=segment,
        code_id=code.code_id,
    )

    removed = coder.remove_assignment(
        assignment.assignment_id
    )

    assert removed == assignment
    assert coder.assignments == []


def test_coder_serialization():
    _, code, segment, coder = (
        build_objects()
    )

    coder.assign_code(
        segment=segment,
        code_id=code.code_id,
        memo="Verbatim explicite.",
    )

    result = coder.to_dict()

    assert len(
        result["assignments"]
    ) == 1

    assert (
        result["assignments"][0]["memo"]
        == "Verbatim explicite."
    )
