import pytest

from emidaf_core.emix import EMIXEngine


def build_candidate_context():

    engine = EMIXEngine()

    q = engine.create_source(
        source_id="q1",
        engine="eaie",
        family="quantitative",
        label="Quantitatif",
        result_type="regression",
    )

    ql = engine.create_source(
        source_id="ql1",
        engine="eqae",
        family="qualitative",
        label="Qualitatif",
        result_type="theme",
    )

    manager = (
        engine.create_candidate_manager()
    )

    candidate = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="Résultat quantitatif",
        element_2="Thème qualitatif",
        candidate_id="c1",
    )

    manager.add(
        candidate
    )

    return engine, manager


def test_accepted_candidate_conversion():

    engine, manager = (
        build_candidate_context()
    )

    manager.accept(
        "c1"
    )

    converter = (
        engine.create_candidate_converter(
            manager
        )
    )

    link = converter.convert(
        candidate_id="c1",
        relation_type="complementarity",
        researcher_note=(
            "Le résultat qualitatif apporte "
            "un éclairage complémentaire."
        ),
        link_id="l1",
    )

    assert link.link_id == "l1"

    assert (
        link.candidate_id
        == "c1"
    )

    assert (
        link.relation_type
        == "complementarity"
    )

    assert link.validated is True


def test_pending_candidate_cannot_be_converted():

    engine, manager = (
        build_candidate_context()
    )

    converter = (
        engine.create_candidate_converter(
            manager
        )
    )

    with pytest.raises(ValueError):
        converter.convert(
            candidate_id="c1",
            relation_type="convergence",
        )


def test_rejected_candidate_cannot_be_converted():

    engine, manager = (
        build_candidate_context()
    )

    manager.reject(
        "c1"
    )

    converter = (
        engine.create_candidate_converter(
            manager
        )
    )

    with pytest.raises(ValueError):
        converter.convert(
            candidate_id="c1",
            relation_type="divergence",
        )


def test_relation_type_must_be_explicit_and_valid():

    engine, manager = (
        build_candidate_context()
    )

    manager.accept(
        "c1"
    )

    converter = (
        engine.create_candidate_converter(
            manager
        )
    )

    with pytest.raises(ValueError):
        converter.convert(
            candidate_id="c1",
            relation_type="automatic",
        )
