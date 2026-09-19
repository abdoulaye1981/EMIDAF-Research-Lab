from __future__ import annotations

import pandas as pd
import pytest

from emidaf_core.statistics.outliers.ensemble import (
    ABODDetector,
    COPODDetector,
    ECODDetector,
    HBOSDetector,
)

from emidaf_core.statistics.outliers.multivariate import (
    FeatureBaggingOutlier,
)


def make_dataframe():

    return pd.DataFrame(
        {
            "x1": [
                0.0,
                0.1,
                -0.1,
                0.2,
                5.0,
            ],
            "x2": [
                0.0,
                -0.1,
                0.1,
                0.2,
                5.0,
            ],
        }
    )


@pytest.mark.parametrize(
    "detector",
    [
        HBOSDetector,
        ABODDetector,
        ECODDetector,
        COPODDetector,
        FeatureBaggingOutlier,
    ],
)
def test_pyod_detector_reports_missing_optional_dependency(
    detector,
):

    dataframe = make_dataframe()

    with pytest.raises(
        ImportError,
        match="PyOD",
    ):
        detector.detect(
            dataframe
        )
