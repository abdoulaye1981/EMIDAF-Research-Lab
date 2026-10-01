from emidaf_core.emix import EMIXEngine


def test_candidate_generation():

    engine = EMIXEngine()

    q = engine.create_source(
        source_id="eaie-1",
        engine="eaie",
        family="quantitative",
        label="Régression",
        result_type="regression",
    )

    ql = engine.create_source(
        source_id="eqae-1",
        engine="eqae",
        family="qualitative",
        label="Thèmes",
        result_type="theme",
    )

    candidate = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1=(
            "interet_maths associé "
            "positivement à note_maths"
        ),
        element_2=(
            "Thème Motivation et intérêt"
        ),
        rationale=(
            "Les deux résultats portent "
            "sur l'intérêt pour les mathématiques."
        ),
        candidate_id="c1",
    )

    assert candidate.status == "pending"
    assert candidate.source_id_1 == "eaie-1"
    assert candidate.source_id_2 == "eqae-1"


def test_candidate_manager_accept_reject():

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

    manager = engine.create_candidate_manager()

    c1 = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="A",
        element_2="B",
        candidate_id="c1",
    )

    c2 = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="C",
        element_2="D",
        candidate_id="c2",
    )

    manager.add(c1)
    manager.add(c2)

    accepted = manager.accept(
        "c1"
    )

    rejected = manager.reject(
        "c2"
    )

    assert accepted.status == "accepted"
    assert rejected.status == "rejected"
    assert manager.pending() == []


def test_candidate_does_not_assign_relation_type():

    engine = EMIXEngine()

    q = engine.create_source(
        source_id="q1",
        engine="eaie",
        family="quantitative",
        label="Q",
        result_type="regression",
    )

    ql = engine.create_source(
        source_id="ql1",
        engine="eqae",
        family="qualitative",
        label="QL",
        result_type="theme",
    )

    candidate = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="A",
        element_2="B",
    )

    data = candidate.to_dict()

    assert "relation_type" not in data
