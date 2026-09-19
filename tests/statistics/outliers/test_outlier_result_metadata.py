from __future__ import annotations

from emidaf_core.common.results import OutlierResult


def test_outlier_result_has_scientific_score_metadata():

    result = OutlierResult()

    assert hasattr(
        result,
        "score_type",
    )

    assert hasattr(
        result,
        "score_direction",
    )

    assert hasattr(
        result,
        "method_family",
    )

    assert hasattr(
        result,
        "scaling_sensitive",
    )


def test_outlier_result_metadata_defaults_are_safe():

    result = OutlierResult()

    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.method_family == ""
    assert result.scaling_sensitive is False


def test_outlier_result_accepts_explicit_metadata():

    result = OutlierResult(
        method="Example",
        score_type="distance",
        score_direction="higher_is_more_anomalous",
        method_family="distance",
        scaling_sensitive=True,
    )

    assert result.score_type == "distance"

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.method_family == "distance"

    assert result.scaling_sensitive is True
