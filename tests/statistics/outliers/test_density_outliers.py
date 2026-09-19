"""
=========================================================
EMIDAF Framework
Tests - Density Based Outlier Detection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.density import (
    DBSCANOutlier,
    LOF,
    OPTICSOutlier,
)


@pytest.fixture
def density_dataframe() -> pd.DataFrame:

    rng = np.random.default_rng(42)

    cluster = rng.normal(
        loc=0.0,
        scale=0.15,
        size=(100, 2),
    )

    dataframe = pd.DataFrame(
        cluster,
        columns=[
            "x1",
            "x2",
        ],
        index=[
            f"row_{i}"
            for i in range(100)
        ],
    )

    dataframe.loc[
        "row_OUTLIER"
    ] = [
        8.0,
        8.0,
    ]

    return dataframe


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_preserves_custom_index(
    detector,
    density_dataframe,
):

    result = detector.detect(
        density_dataframe
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(density_dataframe.index)
    )

    assert set(
        result.inlier_indices
    ).issubset(
        set(density_dataframe.index)
    )

    assert (
        set(result.outlier_indices)
        |
        set(result.inlier_indices)
        == set(density_dataframe.index)
    )


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_detects_isolated_point(
    detector,
    density_dataframe,
):

    result = detector.detect(
        density_dataframe
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_counts_are_consistent(
    detector,
    density_dataframe,
):

    result = detector.detect(
        density_dataframe
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_does_not_mutate_input(
    detector,
    density_dataframe,
):

    before = density_dataframe.copy(
        deep=True
    )

    detector.detect(
        density_dataframe
    )

    pd.testing.assert_frame_equal(
        density_dataframe,
        before,
    )


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_ignores_non_numeric_columns(
    detector,
    density_dataframe,
):

    dataframe = density_dataframe.copy(
        deep=True
    )

    dataframe["category"] = "A"

    result = detector.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


@pytest.mark.parametrize(
    "detector",
    [
        LOF,
        DBSCANOutlier,
        OPTICSOutlier,
    ],
)
def test_density_detector_excludes_missing_rows(
    detector,
    density_dataframe,
):

    dataframe = density_dataframe.copy(
        deep=True
    )

    dataframe.loc[
        "row_0",
        "x1",
    ] = np.nan

    result = detector.detect(
        dataframe
    )

    assert (
        "row_0"
        not in result.outlier_indices
    )

    assert (
        "row_0"
        not in result.inlier_indices
    )

    assert (
        result.total_observations
        == len(dataframe) - 1
    )
