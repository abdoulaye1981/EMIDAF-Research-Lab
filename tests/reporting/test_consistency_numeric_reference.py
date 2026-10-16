from emidaf_core.assistant.consistency_checker import (
    ConsistencyChecker,
)


def test_exact_structured_number_is_allowed():
    source_context = {
        "analyses": {}
    }

    numeric_context = {
        "analyses": {
            "eaie": {
                "cv_mean": 0.4074794901883356,
            }
        }
    }

    result = ConsistencyChecker.check(
        "R² = 0.4074794901883356",
        source_context,
        numeric_source_context=numeric_context,
    )

    assert result["valid"] is True
    assert result["suspicious_numbers"] == []


def test_framework_rendered_percentage_is_allowed():
    source_context = {
        "analyses": {}
    }

    numeric_context = {
        "analyses": {
            "ekde": {
                "cluster_sizes": [
                    {
                        "count": 1255,
                        "percentage": 50.2,
                    },
                    {
                        "count": 1245,
                        "percentage": 49.8,
                    },
                ]
            }
        }
    }

    source_report = (
        "Cluster 1 : 1255 observations (50.2 %)\\n"
        "Cluster 2 : 1245 observations (49.8 %)"
    )

    result = ConsistencyChecker.check(
        (
            "Le premier cluster représente 50.2 % "
            "et le second 49.8 %."
        ),
        source_context,
        numeric_source_context=numeric_context,
        numeric_source_text=source_report,
    )

    assert result["valid"] is True
    assert result["suspicious_numbers"] == []


def test_framework_rendered_confidence_level_is_allowed():
    source_context = {
        "analyses": {}
    }

    numeric_context = {
        "analyses": {
            "elae": {
                "alpha": 0.05,
            }
        }
    }

    source_report = (
        "L'intervalle de confiance à 95 % "
        "est [-1.47, -0.18]."
    )

    result = ConsistencyChecker.check(
        (
            "L'intervalle de confiance à 95 % "
            "est fourni par EMIDAF."
        ),
        source_context,
        numeric_source_context=numeric_context,
        numeric_source_text=source_report,
    )

    assert result["valid"] is True
    assert result["suspicious_numbers"] == []


def test_llm_created_percentage_remains_forbidden():
    source_context = {
        "analyses": {}
    }

    numeric_context = {
        "analyses": {
            "eaie": {
                "cv_mean": 0.4074794901883356,
            }
        }
    }

    source_report = (
        "Score R² moyen en validation croisée : "
        "0.4074794901883356"
    )

    result = ConsistencyChecker.check(
        (
            "Le modèle explique environ "
            "40.75 % de la variance."
        ),
        source_context,
        numeric_source_context=numeric_context,
        numeric_source_text=source_report,
    )

    assert result["valid"] is False
    assert "40.75%" in result["suspicious_numbers"]


def test_llm_created_rounding_remains_forbidden():
    source_context = {
        "analyses": {}
    }

    numeric_context = {
        "analyses": {
            "exaie": {
                "permutation": {
                    "stress": 0.2362317725180468,
                }
            }
        }
    }

    source_report = (
        "stress : 0.2362317725180468"
    )

    result = ConsistencyChecker.check(
        "stress : 0.24",
        source_context,
        numeric_source_context=numeric_context,
        numeric_source_text=source_report,
    )

    assert result["valid"] is False
    assert "0.24" in result["suspicious_numbers"]
