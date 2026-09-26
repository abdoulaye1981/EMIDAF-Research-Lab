import pytest

from emidaf_core.eqae import (
    QualitativeSegment,
)


def test_create_segment():
    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé avant les examens.",
    )

    assert segment.segment_id
    assert segment.document_id == "doc-001"
    assert (
        segment.text
        == "Je suis stressé avant les examens."
    )


def test_segment_requires_document_id():
    with pytest.raises(ValueError):
        QualitativeSegment.create(
            document_id="",
            text="Texte",
        )


def test_segment_requires_text():
    with pytest.raises(ValueError):
        QualitativeSegment.create(
            document_id="doc-001",
            text="   ",
        )


def test_segment_invalid_offsets():
    with pytest.raises(ValueError):
        QualitativeSegment.create(
            document_id="doc-001",
            text="Texte",
            start=10,
            end=4,
        )


def test_segment_serialization():
    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Texte qualitatif",
        metadata={
            "participant": "P01",
        },
    )

    result = segment.to_dict()

    assert (
        result["document_id"]
        == "doc-001"
    )

    assert (
        result["metadata"]["participant"]
        == "P01"
    )
