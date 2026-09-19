from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.ensemble import (
    ABODDetector,
    COPODDetector,
    ECODDetector,
    EllipticEnvelopeDetector,
    HBOSDetector,
    IsolationForestDetector,
    OneClassSVMDetector,
)


@pytest.mark.parametrize(
    "detector,family,score_type,scaling_sensitive",
    [
        (
            IsolationForestDetector,
            "ensemble",
            "negative_decision_function",
            False,
        ),
        (
            OneClassSVMDetector,
            "boundary",
            "negative_decision_function",
            True,
        ),
        (
            EllipticEnvelopeDetector,
            "covariance",
            "negative_decision_function",
            False,
        ),
        (
            HBOSDetector,
            "histogram",
            "hbos_score",
            True,
        ),
        (
            ABODDetector,
            "angle",
            "abod_score",
            True,
        ),
        (
            ECODDetector,
            "distribution",
            "ecod_score",
            False,
        ),
        (
            COPODDetector,
            "copula",
            "copod_score",
            False,
        ),
    ],
)
def test_ensemble_detector_metadata_contract(
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


def test_native_ensemble_metadata_is_propagated():

    rng = np.random.default_rng(42)

    dataframe = pd.DataFrame(
        {
            "x1": rng.normal(size=100),
            "x2": rng.normal(size=100),
        }
    )

    result = IsolationForestDetector.detect(
        dataframe
    )

    assert result.method_family == "ensemble"

    assert (
        result.score_type
        == "negative_decision_function"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )
