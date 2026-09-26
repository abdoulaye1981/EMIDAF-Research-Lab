import pytest

from emidaf_core.eqae import (
    AssistedCodingManager,
    Codebook,
    QualitativeCoder,
    QualitativeSegment,
)


def build_objects():
    codebook = Codebook(
        name="Expérience scolaire"
    )

    stress = codebook.add_code(
        name="Stress"
    )

    motivation = codebook.add_code(
        name="Motivation"
    )

    coder = QualitativeCoder(
        codebook
    )

    manager = AssistedCodingManager(
        codebook=codebook,
        coder=coder,
    )

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text=(
            "Je suis stressé avant "
            "les examens."
        ),
    )

    return (
        codebook,
        stress,
        motivation,
        coder,
        manager,
        segment,
    )


def test_create_pending_suggestion():
    (
        _,
        stress,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    suggestion = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
        confidence=0.85,
        rationale="Présence du terme stressé.",
    )

    assert (
        suggestion.status
        == "pending"
    )

    assert (
        suggestion.suggested_code_id
        == stress.code_id
    )

    assert suggestion.confidence == 0.85


def test_invalid_confidence_rejected():
    (
        _,
        stress,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    with pytest.raises(ValueError):
        manager.suggest_code(
            segment=segment,
            code_id=stress.code_id,
            confidence=1.5,
        )


def test_unknown_code_rejected():
    (
        _,
        _,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    with pytest.raises(ValueError):
        manager.suggest_code(
            segment=segment,
            code_id="unknown",
        )


def test_accept_suggestion_creates_assignment():
    (
        _,
        stress,
        _,
        coder,
        manager,
        segment,
    ) = build_objects()

    suggestion = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    reviewed = manager.accept(
        suggestion.suggestion_id,
        reviewer_note="Suggestion validée.",
    )

    assert reviewed.status == "accepted"

    assert (
        reviewed.reviewed_code_id
        == stress.code_id
    )

    assert len(
        coder.assignments
    ) == 1

    assert (
        coder.assignments[0].mode
        == "assisted"
    )


def test_modify_suggestion():
    (
        _,
        stress,
        motivation,
        coder,
        manager,
        segment,
    ) = build_objects()

    suggestion = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    reviewed = manager.modify(
        suggestion.suggestion_id,
        code_id=motivation.code_id,
        reviewer_note=(
            "Le chercheur retient Motivation."
        ),
    )

    assert reviewed.status == "modified"

    assert (
        reviewed.reviewed_code_id
        == motivation.code_id
    )

    assert (
        coder.assignments[0].code_id
        == motivation.code_id
    )


def test_reject_does_not_create_assignment():
    (
        _,
        stress,
        _,
        coder,
        manager,
        segment,
    ) = build_objects()

    suggestion = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    reviewed = manager.reject(
        suggestion.suggestion_id,
        reviewer_note="Suggestion non pertinente.",
    )

    assert reviewed.status == "rejected"
    assert reviewed.reviewed_code_id is None
    assert coder.assignments == []


def test_reviewed_suggestion_cannot_be_reviewed_again():
    (
        _,
        stress,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    suggestion = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    manager.reject(
        suggestion.suggestion_id
    )

    with pytest.raises(ValueError):
        manager.accept(
            suggestion.suggestion_id
        )


def test_filter_suggestions_by_status():
    (
        _,
        stress,
        motivation,
        _,
        manager,
        segment,
    ) = build_objects()

    first = manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    manager.suggest_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    manager.accept(
        first.suggestion_id
    )

    assert len(
        manager.suggestions_by_status(
            "accepted"
        )
    ) == 1

    assert len(
        manager.suggestions_by_status(
            "pending"
        )
    ) == 1


def test_duplicate_pending_suggestion_rejected():
    (
        _,
        stress,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    with pytest.raises(ValueError):
        manager.suggest_code(
            segment=segment,
            code_id=stress.code_id,
        )


def test_serialization():
    (
        _,
        stress,
        _,
        _,
        manager,
        segment,
    ) = build_objects()

    manager.suggest_code(
        segment=segment,
        code_id=stress.code_id,
        confidence=0.75,
    )

    result = manager.to_dict()

    assert len(
        result["suggestions"]
    ) == 1

    assert (
        result["suggestions"][0]["status"]
        == "pending"
    )
