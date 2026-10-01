import pytest

from emidaf_core.emix import EMIXEngine


def build_context():

    engine = EMIXEngine()

    registry = (
        engine.create_source_registry()
    )

    registry.add(
        engine.create_source(
            source_id="q1",
            engine="eaie",
            family="quantitative",
            label="Régression",
            result_type="regression",
        )
    )

    registry.add(
        engine.create_source(
            source_id="ql1",
            engine="eqae",
            family="qualitative",
            label="Thème",
            result_type="theme",
        )
    )

    integration = (
        engine.create_integration_manager(
            registry
        )
    )

    integration.add(
        engine.create_link(
            link_id="l1",
            source_id_1="q1",
            source_id_2="ql1",
            element_1="A",
            element_2="B",
            relation_type="complementarity",
        )
    )

    return engine, integration


def test_meta_inference_manager():

    engine, integration = (
        build_context()
    )

    manager = (
        engine.create_meta_inference_manager(
            integration
        )
    )

    inference = (
        engine.create_meta_inference(
            inference_id="inf-1",
            statement=(
                "Les résultats sont "
                "complémentaires."
            ),
            link_ids=("l1",),
            validated=True,
        )
    )

    manager.add(inference)

    assert len(
        manager.all()
    ) == 1

    assert len(
        manager.validated()
    ) == 1


def test_unknown_link_rejected():

    engine, integration = (
        build_context()
    )

    manager = (
        engine.create_meta_inference_manager(
            integration
        )
    )

    inference = (
        engine.create_meta_inference(
            inference_id="inf-1",
            statement="Test",
            link_ids=("unknown",),
        )
    )

    with pytest.raises(ValueError):
        manager.add(inference)
