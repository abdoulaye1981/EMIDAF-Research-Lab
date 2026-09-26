from emidaf_core.eqae import (
    AssistedCodingManager,
    Codebook,
    QualitativeCoder,
    QualitativeSegment,
    QualitativeSummaryBuilder,
    QuotationManager,
    ThematicAnalysis,
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
        name="Bien-être"
    )

    thematic.link_code(
        theme_id=theme.theme_id,
        code_id=stress.code_id,
    )

    quotation_manager = (
        QuotationManager(
            coder=coder,
            thematic_analysis=thematic,
        )
    )

    assisted = AssistedCodingManager(
        codebook=codebook,
        coder=coder,
    )

    return (
        codebook,
        stress,
        motivation,
        coder,
        thematic,
        theme,
        quotation_manager,
        assisted,
    )


def test_code_summary():

    (
        _,
        stress,
        _,
        coder,
        thematic,
        _,
        quotations,
        assisted,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    quotations.add_quotation(
        segment=segment
    )

    builder = QualitativeSummaryBuilder(
        coder=coder,
        thematic_analysis=thematic,
        quotation_manager=quotations,
        assisted_coding=assisted,
    )

    summaries = (
        builder.summarize_codes()
    )

    stress_summary = next(
        item
        for item in summaries
        if item.code_id == stress.code_id
    )

    assert (
        stress_summary.n_assignments
        == 1
    )

    assert (
        stress_summary.n_documents
        == 1
    )

    assert (
        stress_summary.n_quotations
        == 1
    )


def test_theme_summary():

    (
        _,
        stress,
        _,
        coder,
        thematic,
        theme,
        quotations,
        assisted,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Les examens me stressent.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    quotations.add_quotation(
        segment=segment
    )

    builder = QualitativeSummaryBuilder(
        coder=coder,
        thematic_analysis=thematic,
        quotation_manager=quotations,
        assisted_coding=assisted,
    )

    summaries = (
        builder.summarize_themes()
    )

    result = next(
        item
        for item in summaries
        if item.theme_id == theme.theme_id
    )

    assert result.n_codes == 1
    assert result.n_assignments == 1
    assert result.n_documents == 1
    assert result.n_quotations == 1


def test_assisted_status_counts():

    (
        _,
        stress,
        _,
        coder,
        thematic,
        _,
        quotations,
        assisted,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé.",
    )

    suggestion = (
        assisted.suggest_code(
            segment=segment,
            code_id=stress.code_id,
        )
    )

    assisted.accept(
        suggestion.suggestion_id
    )

    builder = QualitativeSummaryBuilder(
        coder=coder,
        thematic_analysis=thematic,
        quotation_manager=quotations,
        assisted_coding=assisted,
    )

    result = (
        builder.assisted_status_counts()
    )

    assert result["accepted"] == 1
    assert result["pending"] == 0
    assert result["modified"] == 0
    assert result["rejected"] == 0


def test_global_indicators():

    (
        _,
        stress,
        _,
        coder,
        thematic,
        _,
        quotations,
        assisted,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    quotations.add_quotation(
        segment=segment
    )

    assisted.suggest_code(
        segment=segment,
        code_id=stress.code_id,
    )

    builder = QualitativeSummaryBuilder(
        coder=coder,
        thematic_analysis=thematic,
        quotation_manager=quotations,
        assisted_coding=assisted,
    )

    result = (
        builder.global_indicators()
    )

    assert result["n_codes"] == 2
    assert result["n_themes"] == 1
    assert result["n_assignments"] == 1
    assert result["n_documents_coded"] == 1
    assert result["n_segments_coded"] == 1
    assert result["n_quotations"] == 1
    assert result[
        "n_assisted_suggestions"
    ] == 1


def test_full_serialization():

    (
        _,
        stress,
        _,
        coder,
        thematic,
        _,
        quotations,
        assisted,
    ) = build_objects()

    segment = QualitativeSegment.create(
        document_id="doc-001",
        text="Je suis stressé.",
    )

    coder.assign_code(
        segment=segment,
        code_id=stress.code_id,
    )

    builder = QualitativeSummaryBuilder(
        coder=coder,
        thematic_analysis=thematic,
        quotation_manager=quotations,
        assisted_coding=assisted,
    )

    result = builder.to_dict()

    assert "global" in result
    assert "codes" in result
    assert "themes" in result
    assert "assisted_coding" in result
