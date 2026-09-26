import pytest

from emidaf_core.eqae import (
    Codebook,
    CooccurrenceAnalyzer,
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

    soutien = codebook.add_code(
        name="Soutien"
    )

    coder = QualitativeCoder(
        codebook
    )

    return (
        codebook,
        stress,
        motivation,
        soutien,
        coder,
    )


def test_segment_cooccurrence():
    (
        _,
        stress,
        motivation,
        _,
        coder,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Texte",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    coder.assign_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    results = analyzer.analyze(
        level="segment"
    )

    assert len(results) == 1

    assert {
        results[0].code_id_1,
        results[0].code_id_2,
    } == {
        stress.code_id,
        motivation.code_id,
    }

    assert results[0].count == 1


def test_repeated_segment_cooccurrence_count():
    (
        _,
        stress,
        motivation,
        _,
        coder,
    ) = build_objects()

    for index in range(2):

        segment = QualitativeSegment.create(
            document_id=f"doc-{index}",
            text=f"Texte {index}",
        )

        coder.assign_code(
            segment=segment,
            code_id=stress.code_id,
        )

        coder.assign_code(
            segment=segment,
            code_id=motivation.code_id,
        )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    results = analyzer.analyze()

    assert len(results) == 1
    assert results[0].count == 2


def test_document_level_cooccurrence():
    (
        _,
        stress,
        motivation,
        _,
        coder,
    ) = build_objects()

    first = QualitativeSegment.create(
        document_id="doc-001",
        text="Stress",
    )

    second = QualitativeSegment.create(
        document_id="doc-001",
        text="Motivation",
    )

    coder.assign_code(
        segment=first,
        code_id=stress.code_id,
    )

    coder.assign_code(
        segment=second,
        code_id=motivation.code_id,
    )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    segment_result = analyzer.analyze(
        level="segment"
    )

    document_result = analyzer.analyze(
        level="document"
    )

    assert segment_result == []
    assert len(document_result) == 1


def test_same_code_not_self_cooccurrence():
    (
        _,
        stress,
        _,
        _,
        coder,
    ) = build_objects()

    first = QualitativeSegment.create(
        document_id="doc-001",
        text="Premier",
    )

    second = QualitativeSegment.create(
        document_id="doc-001",
        text="Deuxième",
    )

    coder.assign_code(
        segment=first,
        code_id=stress.code_id,
    )

    coder.assign_code(
        segment=second,
        code_id=stress.code_id,
    )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    assert analyzer.analyze(
        level="document"
    ) == []


def test_invalid_level_rejected():
    *_, coder = build_objects()

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    with pytest.raises(ValueError):
        analyzer.analyze(
            level="paragraph"
        )


def test_matrix_is_symmetric():
    (
        _,
        stress,
        motivation,
        _,
        coder,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Texte",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    coder.assign_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    matrix = analyzer.matrix()

    assert (
        matrix[stress.code_id][motivation.code_id]
        == 1
    )

    assert (
        matrix[motivation.code_id][stress.code_id]
        == 1
    )


def test_serialization():
    (
        _,
        stress,
        motivation,
        _,
        coder,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Texte",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    coder.assign_code(
        segment=segment,
        code_id=motivation.code_id,
    )

    analyzer = CooccurrenceAnalyzer(
        coder
    )

    result = analyzer.to_dict()

    assert result["level"] == "segment"

    assert len(
        result["cooccurrences"]
    ) == 1

    assert "matrix" in result
