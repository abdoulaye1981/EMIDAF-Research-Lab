from __future__ import annotations

import numpy as np
import pandas as pd

from emidaf_core.statistics.outliers.density import (
    DBSCANOutlier,
    LOF,
    OPTICSOutlier,
)


def make_dataframe():

    rng = np.random.default_rng(42)

    return pd.DataFrame(
        {
            "x1": rng.normal(
                0.0,
                1.0,
                50,
            ),
            "x2": rng.normal(
                0.0,
                1.0,
                50,
            ),
        }
    )


def test_lof_metadata():

    result = LOF.detect(
        make_dataframe()
    )

    assert result.method_family == "density"

    assert (
        result.score_type
        == "local_outlier_factor"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is True


def test_dbscan_metadata():

    result = DBSCANOutlier.detect(
        make_dataframe()
    )

    assert result.method_family == "density"
    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.scaling_sensitive is True


def test_optics_metadata():

    result = OPTICSOutlier.detect(
        make_dataframe()
    )

    assert result.method_family == "density"
    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.scaling_sensitive is True
