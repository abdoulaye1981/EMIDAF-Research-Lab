import pytest

from emidaf_core.emix import EMIXEngine


def test_restore_rejects_broken_link_reference():

    engine = EMIXEngine()

    payload = {
        "sources": [
            {
                "source_id": "q1",
                "engine": "eaie",
                "family": "quantitative",
                "label": "Quantitatif",
                "result_type": "regression",
                "result_ref": None,
                "description": "",
            }
        ],
        "links": [
            {
                "link_id": "l1",
                "source_id_1": "q1",
                "source_id_2": "missing",
                "element_1": "A",
                "element_2": "B",
                "relation_type": "undetermined",
                "researcher_note": "",
                "validated": False,
            }
        ],
        "joint_display": [],
        "meta_inferences": [],
    }

    with pytest.raises(ValueError):
        engine.restore_session(
            payload
        )
