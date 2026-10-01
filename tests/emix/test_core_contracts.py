import pytest

from emidaf_core.emix import (
    IntegrationLink,
    JointDisplayRow,
    MetaInference,
    MixedMethodSource,
    MixedMethodsSummary,
)


def test_mixed_method_source():

    source = MixedMethodSource(
        source_id="quant-1",
        engine="eaie",
        family="quantitative",
        label="Régression réussite",
        result_type="regression",
    )

    data = source.to_dict()

    assert data["engine"] == "eaie"
    assert data["family"] == "quantitative"


def test_invalid_source_family():

    with pytest.raises(ValueError):

        MixedMethodSource(
            source_id="x",
            engine="eaie",
            family="invalid",
            label="Test",
            result_type="test",
        )


def test_integration_link():

    link = IntegrationLink(
        link_id="link-1",
        source_id_1="quant-1",
        source_id_2="qual-1",
        element_1=(
            "Intérêt associé positivement "
            "à la note"
        ),
        element_2=(
            "Thème Motivation et intérêt"
        ),
        relation_type="convergence",
        validated=True,
    )

    assert link.relation_type == "convergence"
    assert link.validated is True


def test_same_source_link_is_rejected():

    with pytest.raises(ValueError):

        IntegrationLink(
            link_id="link-1",
            source_id_1="same",
            source_id_2="same",
            element_1="A",
            element_2="B",
            relation_type="convergence",
        )


def test_joint_display_row():

    row = JointDisplayRow(
        row_id="row-1",
        quantitative_result=(
            "Association positive"
        ),
        qualitative_result=(
            "Motivation et intérêt"
        ),
        relation_type="complementarity",
    )

    assert (
        row.relation_type
        == "complementarity"
    )


def test_meta_inference_defaults_to_unvalidated():

    inference = MetaInference(
        inference_id="inf-1",
        statement=(
            "Les résultats suggèrent "
            "une complémentarité."
        ),
    )

    assert inference.validated is False


def test_mixed_methods_summary():

    quantitative = MixedMethodSource(
        source_id="quant-1",
        engine="eaie",
        family="quantitative",
        label="Régression",
        result_type="regression",
    )

    qualitative = MixedMethodSource(
        source_id="qual-1",
        engine="eqae",
        family="qualitative",
        label="Thèmes",
        result_type="theme",
    )

    link = IntegrationLink(
        link_id="link-1",
        source_id_1="quant-1",
        source_id_2="qual-1",
        element_1="Résultat quantitatif",
        element_2="Résultat qualitatif",
        relation_type="convergence",
        validated=True,
    )

    row = JointDisplayRow(
        row_id="row-1",
        quantitative_result=(
            "Résultat quantitatif"
        ),
        qualitative_result=(
            "Résultat qualitatif"
        ),
        relation_type="convergence",
        source_link_id="link-1",
    )

    inference = MetaInference(
        inference_id="inf-1",
        statement="Interprétation intégrée",
        link_ids=("link-1",),
        validated=True,
    )

    summary = MixedMethodsSummary(
        sources=(
            quantitative,
            qualitative,
        ),
        links=(link,),
        joint_display=(row,),
        meta_inferences=(inference,),
    )

    data = summary.to_dict()

    assert data["global"]["n_sources"] == 2
    assert data["global"]["n_links"] == 1

    assert (
        data["relations"]["convergence"]
        == 1
    )

    assert (
        data["global"][
            "n_validated_meta_inferences"
        ]
        == 1
    )
