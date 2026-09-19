from __future__ import annotations

import pytest

from emidaf_core.statistics.outliers.multivariate import (
    AutoEncoderOutlier,
    FeatureBaggingOutlier,
    MinimumCovarianceDeterminant,
    PCAOutlier,
    RobustPCAOutlier,
)


@pytest.mark.parametrize(
    (
        "detector,"
        "family,"
        "score_type,"
        "scaling_sensitive"
    ),
    [
        (
            PCAOutlier,
            "dimensionality_reduction",
            "reconstruction_error",
            True,
        ),
        (
            RobustPCAOutlier,
            "covariance",
            "squared_robust_mahalanobis_distance",
            False,
        ),
        (
            FeatureBaggingOutlier,
            "ensemble",
            "pyod_decision_score",
            True,
        ),
        (
            AutoEncoderOutlier,
            "neural_network",
            "reconstruction_error",
            True,
        ),
        (
            MinimumCovarianceDeterminant,
            "covariance",
            "squared_robust_mahalanobis_distance",
            False,
        ),
    ],
)
def test_multivariate_metadata_contract(
    detector,
    family,
    score_type,
    scaling_sensitive,
):

    assert detector.method_family == family
    assert detector.score_type == score_type

    assert (
        detector.score_direction
        == "higher_is_more_anomalous"
    )

    assert (
        detector.scaling_sensitive
        is scaling_sensitive
    )
