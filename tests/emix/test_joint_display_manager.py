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
            element_1="Résultat quantitatif",
            element_2="Résultat qualitatif",
            relation_type="convergence",
        )
    )

    return engine, integration


def test_joint_display_manager():

    engine, integration = (
        build_context()
    )

    manager = (
        engine.create_joint_display_manager(
            integration
        )
    )

    row = (
        engine.create_joint_display_row(
            row_id="row-1",
            quantitative_result="Résultat A",
            qualitative_result="Thème B",
            relation_type="convergence",
            source_link_id="l1",
        )
    )

    manager.add(row)

    assert len(
        manager.all()
    ) == 1

    assert (
        manager.get(
            "row-1"
        ).source_link_id
        == "l1"
    )


def test_unknown_link_rejected():

    engine, integration = (
        build_context()
    )

    manager = (
        engine.create_joint_display_manager(
            integration
        )
    )

    row = (
        engine.create_joint_display_row(
            row_id="row-1",
            quantitative_result="A",
            qualitative_result="B",
            relation_type="undetermined",
            source_link_id="unknown",
        )
    )

    with pytest.raises(ValueError):
        manager.add(row)
