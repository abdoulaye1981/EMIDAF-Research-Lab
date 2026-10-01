from emidaf_core.emix import EMIXEngine


def test_emix_session_roundtrip():

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
        label="Thème motivation",
        result_type="theme",
    )

    session.source_registry.add(q)
    session.source_registry.add(ql)

    link = engine.create_link(
        link_id="l1",
        source_id_1="q1",
        source_id_2="ql1",
        element_1=(
            "Association positive entre "
            "intérêt et réussite"
        ),
        element_2=(
            "Thème Motivation et intérêt"
        ),
        relation_type="complementarity",
        researcher_note=(
            "À examiner conjointement."
        ),
        validated=True,
    )

    session.integration_manager.add(
        link
    )

    row = (
        engine.create_joint_display_row(
            row_id="r1",
            quantitative_result=(
                "Association positive"
            ),
            qualitative_result=(
                "Motivation et intérêt"
            ),
            relation_type="complementarity",
            integrated_comment=(
                "Le qualitatif précise "
                "le résultat quantitatif."
            ),
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
                "Les résultats suggèrent "
                "une complémentarité."
            ),
            link_ids=("l1",),
            limitations=(
                "Interprétation non causale.",
            ),
            researcher_note=(
                "Validée par le chercheur."
            ),
            validated=True,
        )
    )

    session.meta_inference_manager.add(
        inference
    )

    payload = session.to_dict()

    restored = engine.restore_session(
        payload
    )

    assert (
        restored.to_dict()
        == payload
    )

    assert len(
        restored.source_registry.all()
    ) == 2

    assert len(
        restored.integration_manager.all()
    ) == 1

    assert len(
        restored.joint_display_manager.all()
    ) == 1

    assert len(
        restored.meta_inference_manager.all()
    ) == 1
