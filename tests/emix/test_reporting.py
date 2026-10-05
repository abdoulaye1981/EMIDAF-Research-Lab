from emidaf_studio.pages.reports.callbacks import (
    _compact_emix_for_report,
)


def test_compact_emix_preserves_source_types():
    payload = {
        "sources": {
            "selected_stages": [
                "etae",
                "eqae",
            ]
        },
        "candidates": {
            "items": []
        },
        "integration": {
            "links": []
        },
        "joint_display": {
            "rows": [
                {
                    "source_label_1": "ETAE",
                    "result_type_label_1": (
                        "Résultat textuel computationnel"
                    ),
                    "result_1": "Thème ETAE",
                    "source_label_2": "EQAE",
                    "result_type_label_2": (
                        "Résultat qualitatif"
                    ),
                    "result_2": "Code Motivation",
                    "relation_type": "undetermined",
                    "integrated_comment": (
                        "Interprétation prudente."
                    ),
                    "source_link_id": "link-1",
                }
            ]
        },
        "meta_inferences": {
            "items": []
        },
        "summary": {
            "validation": {
                "researcher_validated": False,
            },
            "global": {},
        },
    }

    result = _compact_emix_for_report(
        payload
    )

    row = result["joint_display"][0]

    assert row["source_1"]["label"] == "ETAE"
    assert (
        row["source_1"]["type"]
        == "Résultat textuel computationnel"
    )
    assert row["source_2"]["label"] == "EQAE"
    assert (
        row["source_2"]["type"]
        == "Résultat qualitatif"
    )


def test_compact_emix_supports_legacy_joint_display():
    payload = {
        "joint_display": {
            "rows": [
                {
                    "quantitative_result": (
                        "Ancien résultat EAIE"
                    ),
                    "qualitative_result": (
                        "Ancien résultat EQAE"
                    ),
                    "relation_type": "complementarity",
                }
            ]
        }
    }

    result = _compact_emix_for_report(
        payload
    )

    row = result["joint_display"][0]

    assert (
        row["source_1"]["result"]
        == "Ancien résultat EAIE"
    )
    assert (
        row["source_2"]["result"]
        == "Ancien résultat EQAE"
    )


def test_compact_emix_counts_candidate_statuses():
    payload = {
        "candidates": {
            "items": [
                {"status": "accepted"},
                {"status": "pending"},
                {"status": "rejected"},
                {"status": "accepted"},
            ]
        }
    }

    result = _compact_emix_for_report(
        payload
    )

    assert result["candidate_statuses"] == {
        "pending": 1,
        "accepted": 2,
        "rejected": 1,
    }


def test_compact_emix_does_not_invent_relations():
    payload = {
        "integration": {
            "links": []
        },
        "joint_display": {
            "rows": []
        },
    }

    result = _compact_emix_for_report(
        payload
    )

    assert result["relations"] == {
        "convergence": 0,
        "complementarity": 0,
        "divergence": 0,
        "undetermined": 0,
    }


def test_compact_emix_recovers_legacy_source_metadata_from_link():
    payload = {
        "integration": {
            "links": [
                {
                    "link_id": "link-1",
                    "source_id_1": "etae-source",
                    "source_id_2": "eqae-source",
                    "relation_type": "complementarity",
                }
            ]
        },
        "joint_display": {
            "rows": [
                {
                    "source_link_id": "link-1",
                    "quantitative_result": (
                        "Thème computationnel ETAE"
                    ),
                    "qualitative_result": (
                        "Code EQAE Motivation"
                    ),
                    "relation_type": "complementarity",
                }
            ]
        },
    }

    result = _compact_emix_for_report(
        payload
    )

    row = result["joint_display"][0]

    assert row["source_1"]["label"] == "ETAE"
    assert (
        row["source_1"]["type"]
        == "Résultat textuel computationnel"
    )

    assert row["source_2"]["label"] == "EQAE"
    assert (
        row["source_2"]["type"]
        == "Résultat qualitatif"
    )
