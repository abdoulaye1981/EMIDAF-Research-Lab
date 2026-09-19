"""
=========================================================
EMIDAF Framework
Tests - Base Outlier Detector
=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from emidaf_core.statistics.outliers.distance import (
    Mahalanobis,
    RobustMahalanobis,
)


def test_mahalanobis_preserves_custom_dataframe_index():

    rng = np.random.default_rng(
        42
    )

    normal = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(200, 2),
    )

    dataframe = pd.DataFrame(
        normal,
        columns=[
            "x1",
            "x2",
        ],
        index=[
            f"row_{i}"
            for i in range(200)
        ],
    )

    dataframe.loc[
        "row_OUTLIER"
    ] = [
        12.0,
        12.0,
    ]

    result = Mahalanobis.detect(
        dataframe,
        alpha=0.05,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )

    assert set(
        result.inlier_indices
    ).issubset(
        set(dataframe.index)
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(dataframe.index)
    )

    assert (
        set(result.inlier_indices)
        |
        set(result.outlier_indices)
        == set(dataframe.index)
    )

def test_robust_mahalanobis_preserves_custom_dataframe_index():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                0.2,
                -0.1,
                0.1,
                -0.2,
                0.0,
                0.1,
                -0.1,
                0.2,
                -0.2,
                15.0,
            ],
            "x2": [
                0.1,
                -0.1,
                0.2,
                0.0,
                -0.2,
                0.2,
                -0.1,
                0.1,
                0.0,
                -0.1,
                15.0,
            ],
        },
        index=[
            "row_A",
            "row_B",
            "row_C",
            "row_D",
            "row_E",
            "row_F",
            "row_G",
            "row_H",
            "row_I",
            "row_J",
            "row_OUTLIER",
        ],
    )

    result = RobustMahalanobis.detect(
        dataframe,
        alpha=0.05,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )

    assert set(
        result.inlier_indices
    ).issubset(
        set(dataframe.index)
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(dataframe.index)
    )


def test_mahalanobis_inlier_and_outlier_indices_partition_index():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                0.1,
                -0.1,
                0.2,
                -0.2,
                12.0,
            ],
            "x2": [
                0.0,
                -0.1,
                0.1,
                0.2,
                -0.2,
                12.0,
            ],
        },
        index=[
            101,
            205,
            309,
            412,
            587,
            999,
        ],
    )

    result = Mahalanobis.detect(
        dataframe,
        alpha=0.05,
    )

    returned_indices = (
        set(result.inlier_indices)
        |
        set(result.outlier_indices)
    )

    assert returned_indices == set(
        dataframe.index
    )

    assert not (
        set(result.inlier_indices)
        &
        set(result.outlier_indices)
    )
