from emidaf_core.eqae import (
    Codebook,
    EQAEEngine,
)


def test_engine_creates_codebook():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire",
        description="Analyse qualitative",
    )

    assert isinstance(
        codebook,
        Codebook,
    )

    assert (
        codebook.name
        == "Expérience scolaire"
    )


def test_engine_codebook_workflow():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    codebook.add_code(
        name="Stress"
    )

    codebook.add_code(
        name="Motivation"
    )

    result = codebook.to_dict()

    assert len(
        result["codes"]
    ) == 2


def test_engine_creates_coder():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    coder = engine.create_coder(
        codebook
    )

    assert coder.codebook is codebook


def test_engine_creates_thematic_analysis():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    analysis = (
        engine.create_thematic_analysis(
            codebook
        )
    )

    assert analysis.codebook is codebook


def test_engine_creates_quotation_manager():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    coder = engine.create_coder(
        codebook
    )

    thematic = (
        engine.create_thematic_analysis(
            codebook
        )
    )

    manager = (
        engine.create_quotation_manager(
            coder=coder,
            thematic_analysis=thematic,
        )
    )

    assert manager.coder is coder
    assert (
        manager.thematic_analysis
        is thematic
    )


def test_engine_creates_cooccurrence_analyzer():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    coder = engine.create_coder(
        codebook
    )

    analyzer = (
        engine.create_cooccurrence_analyzer(
            coder
        )
    )

    assert analyzer.coder is coder


def test_engine_creates_memo_manager():
    engine = EQAEEngine()

    manager = (
        engine.create_memo_manager()
    )

    memo = manager.add_memo(
        title="Mémo analytique",
        content="Première interprétation.",
    )

    assert memo.memo_id


def test_engine_creates_assisted_coding_manager():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    coder = engine.create_coder(
        codebook
    )

    manager = (
        engine.create_assisted_coding_manager(
            codebook=codebook,
            coder=coder,
        )
    )

    assert manager.codebook is codebook
    assert manager.coder is coder


def test_engine_creates_summary_builder():
    engine = EQAEEngine()

    codebook = engine.create_codebook(
        name="Expérience scolaire"
    )

    coder = engine.create_coder(
        codebook
    )

    thematic = (
        engine.create_thematic_analysis(
            codebook
        )
    )

    builder = (
        engine.create_summary_builder(
            coder=coder,
            thematic_analysis=thematic,
        )
    )

    assert builder.coder is coder
    assert (
        builder.thematic_analysis
        is thematic
    )
