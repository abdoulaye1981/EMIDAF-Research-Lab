from emidaf_studio.pages.emix.callbacks import (
    _extract_target_correlations,
    _generate_elae_eaie_candidates,
    _generate_ekde_eaie_candidates,
    _generate_eaie_edse_candidates,
)


def test_extract_target_correlations():

    payload = {
        "correlations": {
            "matrix": {
                "note_maths": {
                    "note_maths": 1.0,
                    "motivation": 0.31,
                    "stress": -0.29,
                }
            }
        }
    }

    result = _extract_target_correlations(
        payload,
        target="note_maths",
        matrix_path=(
            "correlations",
            "matrix",
        ),
    )

    by_variable = {
        item["variable"]: item
        for item in result
    }

    assert set(by_variable) == {
        "motivation",
        "stress",
    }

    assert (
        by_variable["motivation"][
            "correlation"
        ]
        == 0.31
    )

    assert (
        by_variable["stress"][
            "correlation"
        ]
        == -0.29
    )


def test_elae_eaie_candidate_is_pending():

    elae = {
        "correlations": {
            "matrix": {
                "note_maths": {
                    "note_maths": 1.0,
                    "interet_maths": 0.40,
                    "stress": -0.29,
                }
            }
        }
    }

    eaie = {
        "target": "note_maths",
        "features": [
            "interet_maths",
        ],
    }

    exaie = {
        "shap": {
            "available": True,
            "feature_importance": {
                "numeric__interet_maths": 1.25,
            },
        }
    }

    result = (
        _generate_elae_eaie_candidates(
            elae,
            eaie,
            exaie,
        )
    )

    assert len(result) == 1

    candidate = result[0]

    assert (
        candidate["source_id_1"]
        == "elae-source"
    )

    assert (
        candidate["source_id_2"]
        == "eaie-source"
    )

    assert (
        candidate["status"]
        == "pending"
    )

    assert (
        "relation_type"
        not in candidate
    )

    assert (
        candidate["metadata"][
            "variable"
        ]
        == "interet_maths"
    )

    assert (
        candidate["metadata"][
            "global_shap_importance"
        ]
        == 1.25
    )


def test_ekde_eaie_uses_only_eaie_features():

    ekde = {
        "structure": {
            "correlation_matrix": {
                "note_maths": {
                    "note_maths": 1.0,
                    "motivation": 0.32,
                    "budget_annuel": 0.02,
                }
            }
        }
    }

    eaie = {
        "target": "note_maths",
        "features": [
            "motivation",
        ],
    }

    result = (
        _generate_ekde_eaie_candidates(
            ekde,
            eaie,
        )
    )

    assert len(result) == 1

    assert (
        result[0]["metadata"][
            "variable"
        ]
        == "motivation"
    )


def test_eaie_edse_requires_same_target():

    eaie = {
        "target": "note_maths",
        "model_name": "LinearRegression",
    }

    edse = {
        "target": "note_maths",
        "model_name": "LinearRegression",
        "threshold": 10.84,
    }

    result = (
        _generate_eaie_edse_candidates(
            eaie,
            edse,
        )
    )

    assert len(result) == 1

    candidate = result[0]

    assert (
        candidate["status"]
        == "pending"
    )

    assert (
        "relation_type"
        not in candidate
    )

    assert (
        candidate["source_id_1"]
        == "eaie-source"
    )

    assert (
        candidate["source_id_2"]
        == "edse-source"
    )


def test_eaie_edse_rejects_different_targets():

    eaie = {
        "target": "note_maths",
    }

    edse = {
        "target": "autre_cible",
    }

    assert (
        _generate_eaie_edse_candidates(
            eaie,
            edse,
        )
        == []
    )
