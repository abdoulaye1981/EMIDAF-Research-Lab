import pytest

from emidaf_core.eqae import (
    Codebook,
    QualitativeCoder,
    QualitativeSegment,
    ThematicAnalysis,
    QuotationManager,
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

    thematic = ThematicAnalysis(
        codebook
    )

    theme = thematic.add_theme(
        name="Bien-être scolaire"
    )

    thematic.link_code(
        theme_id=theme.theme_id,
        code_id=stress.code_id,
    )

    manager = QuotationManager(
        coder=coder,
        thematic_analysis=thematic,
    )

    return (
        codebook,
        stress,
        motivation,
        coder,
        thematic,
        theme,
        manager,
    )


def test_add_quotation():
    *_, manager = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé avant les examens.",
    )

    quotation = manager.add_quotation(
        segment=segment
    )

    assert quotation.quotation_id
    assert (
        quotation.text
        == segment.text
    )


def test_duplicate_quotation_rejected():
    *_, manager = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Texte qualitatif",
    )

    manager.add_quotation(
        segment=segment
    )

    with pytest.raises(ValueError):
        manager.add_quotation(
            segment=segment
        )


def test_quotations_for_code():
    (
        _,
        stress,
        _,
        coder,
        _,
        _,
        manager,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    quotation = manager.add_quotation(
        segment=segment
    )

    result = manager.quotations_for_code(
        stress.code_id
    )

    assert result == [quotation]


def test_quotations_for_theme():
    (
        _,
        stress,
        _,
        coder,
        _,
        theme,
        manager,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Les examens me stressent beaucoup.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    quotation = manager.add_quotation(
        segment=segment
    )

    result = manager.quotations_for_theme(
        theme.theme_id
    )

    assert result == [quotation]


def test_unlinked_code_not_returned_for_theme():
    (
        _,
        _,
        motivation,
        coder,
        _,
        theme,
        manager,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="J'aime apprendre.",
    )

    coder.assign_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    manager.add_quotation(
        segment=segment
    )

    assert (
        manager.quotations_for_theme(
            theme.theme_id
        )
        == []
    )


def test_quotations_for_document():
    *_, manager = build_objects()

    first = QualitativeSegment.create(
        document_id="doc-001",
        text="Premier extrait",
    )

    second = QualitativeSegment.create(
        document_id="doc-002",
        text="Deuxième extrait",
    )

    q1 = manager.add_quotation(
        segment=first
    )

    manager.add_quotation(
        segment=second
    )

    result = (
        manager.quotations_for_document(
            "doc-001"
        )
    )

    assert result == [q1]


def test_remove_quotation():
    *_, manager = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Verbatim",
    )

    quotation = manager.add_quotation(
        segment=segment
    )

    removed = manager.remove_quotation(
        quotation.quotation_id
    )

    assert removed == quotation
    assert manager.quotations == []


def test_serialization():
    *_, manager = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Un verbatim important.",
    )

    manager.add_quotation(
        segment=segment,
        note="Illustration du thème.",
    )

    result = manager.to_dict()

    assert len(
        result["quotations"]
    ) == 1

    assert (
        result["quotations"][0]["note"]
        == "Illustration du thème."
    )
