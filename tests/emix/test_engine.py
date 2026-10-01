import pytest

from emidaf_core.emix import EMIXEngine


def test_engine_creates_registry_and_manager():

    engine = EMIXEngine()

    registry = (
        engine.create_source_registry()
    )

    manager = (
        engine.create_integration_manager(
            registry
        )
    )

    assert registry.all() == []
    assert manager.all() == []


def test_registry_and_integration_workflow():

    engine = EMIXEngine()

    registry = (
        engine.create_source_registry()
    )

    quantitative = engine.create_source(
        source_id="quant-1",
        engine="eaie",
        family="quantitative",
        label="Régression",
        result_type="regression",
    )

    qualitative = engine.create_source(
        source_id="qual-1",
        engine="eqae",
        family="qualitative",
        label="Analyse thématique",
        result_type="theme",
    )

    registry.add(
        quantitative
    )
    registry.add(
        qualitative
    )

    manager = (
        engine.create_integration_manager(
            registry
        )
    )

    link = engine.create_link(
        link_id="link-1",
        source_id_1="quant-1",
        source_id_2="qual-1",
        element_1=(
            "Association positive "
            "entre intérêt et réussite"
        ),
        element_2=(
            "Thème Motivation et intérêt"
        ),
        relation_type="complementarity",
        validated=True,
    )

    manager.add(
        link
    )

    assert len(
        registry.all()
    ) == 2

    assert len(
        manager.all()
    ) == 1

    assert (
        manager.get(
            "link-1"
        ).validated
        is True
    )


def test_manager_refuses_unknown_source():

    engine = EMIXEngine()

    registry = (
        engine.create_source_registry()
    )

    source = engine.create_source(
        source_id="quant-1",
        engine="eaie",
        family="quantitative",
        label="Régression",
        result_type="regression",
    )

    registry.add(source)

    manager = (
        engine.create_integration_manager(
            registry
        )
    )

    link = engine.create_link(
        link_id="link-1",
        source_id_1="quant-1",
        source_id_2="unknown",
        element_1="A",
        element_2="B",
        relation_type="undetermined",
    )

    with pytest.raises(ValueError):
        manager.add(link)


def test_summary_workflow():

    engine = EMIXEngine()

    source_1 = engine.create_source(
        source_id="q1",
        engine="eaie",
        family="quantitative",
        label="Résultat quantitatif",
        result_type="regression",
    )

    source_2 = engine.create_source(
        source_id="ql1",
        engine="eqae",
        family="qualitative",
        label="Résultat qualitatif",
        result_type="theme",
    )

    link = engine.create_link(
        link_id="l1",
        source_id_1="q1",
        source_id_2="ql1",
        element_1="Résultat A",
        element_2="Thème B",
        relation_type="convergence",
        validated=True,
    )

    row = engine.create_joint_display_row(
        row_id="row-1",
        quantitative_result="Résultat A",
        qualitative_result="Thème B",
        relation_type="convergence",
        source_link_id="l1",
    )

    inference = (
        engine.create_meta_inference(
            inference_id="inf-1",
            statement=(
                "Les deux résultats sont "
                "interprétés conjointement."
            ),
            link_ids=("l1",),
            validated=True,
        )
    )

    summary = engine.create_summary(
        sources=[
            source_1,
            source_2,
        ],
        links=[link],
        joint_display=[row],
        meta_inferences=[inference],
    )

    data = summary.to_dict()

    assert (
        data["global"]["n_sources"]
        == 2
    )

    assert (
        data["relations"]["convergence"]
        == 1
    )
