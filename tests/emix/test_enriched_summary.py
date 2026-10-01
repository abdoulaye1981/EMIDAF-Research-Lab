from emidaf_core.emix import EMIXEngine


def test_enriched_mixed_methods_summary():

    engine = EMIXEngine()

    session = engine.create_session()

    q = engine.create_source(
        source_id="q1",
        engine="eaie",
        family="quantitative",
        label="Régression",
        result_type="regression",
    )

    ql = engine.create_source(
        source_id="ql1",
        engine="eqae",
        family="qualitative",
        label="Analyse qualitative",
        result_type="theme",
    )

    session.source_registry.add(q)
    session.source_registry.add(ql)

    candidate_manager = (
        engine.create_candidate_manager()
    )

    c1 = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="Résultat Q",
        element_2="Thème QL",
        candidate_id="c1",
    )

    c2 = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="Résultat Q2",
        element_2="Thème QL2",
        candidate_id="c2",
    )

    c3 = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="Résultat Q3",
        element_2="Thème QL3",
        candidate_id="c3",
    )

    candidate_manager.add(c1)
    candidate_manager.add(c2)
    candidate_manager.add(c3)

    candidate_manager.accept("c1")
    candidate_manager.reject("c2")

    converter = (
        engine.create_candidate_converter(
            candidate_manager
        )
    )

    link = converter.convert(
        candidate_id="c1",
        relation_type="complementarity",
        link_id="l1",
    )

    session.integration_manager.add(
        link
    )

    row = (
        engine.create_joint_display_row(
            row_id="r1",
            quantitative_result="Résultat Q",
            qualitative_result="Thème QL",
            relation_type="complementarity",
            source_link_id="l1",
        )
    )

    session.joint_display_manager.add(
        row
    )

    inference = (
        engine.create_meta_inference(
            inference_id="i1",
            statement=(
                "Le résultat qualitatif "
                "complète le résultat "
                "quantitatif."
            ),
            link_ids=("l1",),
            validated=True,
        )
    )

    session.meta_inference_manager.add(
        inference
    )

    summary = engine.summarize_session(
        session,
        candidates=(
            candidate_manager.all()
        ),
    )

    data = summary.to_dict()

    assert data["global"]["n_sources"] == 2
    assert data["global"]["n_candidates"] == 3
    assert data["global"]["n_links"] == 1

    assert (
        data["candidate_statuses"]["pending"]
        == 1
    )

    assert (
        data["candidate_statuses"]["accepted"]
        == 1
    )

    assert (
        data["candidate_statuses"]["rejected"]
        == 1
    )

    assert (
        data["relations"]["complementarity"]
        == 1
    )

    assert (
        data["global"]["n_validated_links"]
        == 1
    )

    assert (
        data["global"][
            "n_validated_meta_inferences"
        ]
        == 1
    )

    assert (
        data["validation"][
            "suggestions_are_conclusions"
        ]
        is False
    )


def test_accepted_candidate_is_not_automatically_a_link():

    engine = EMIXEngine()

    session = engine.create_session()

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

    session.source_registry.add(q)
    session.source_registry.add(ql)

    manager = engine.create_candidate_manager()

    candidate = engine.create_candidate(
        source_1=q,
        source_2=ql,
        element_1="A",
        element_2="B",
        candidate_id="c1",
    )

    manager.add(candidate)
    manager.accept("c1")

    summary = engine.summarize_session(
        session,
        candidates=manager.all(),
    )

    data = summary.to_dict()

    assert (
        data["candidate_statuses"]["accepted"]
        == 1
    )

    assert data["global"]["n_links"] == 0

    assert (
        data["global"]["n_validated_links"]
        == 0
    )
