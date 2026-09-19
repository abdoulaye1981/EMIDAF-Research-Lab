"""
=========================================================
EMIDAF Framework
Tests - Distance Outliers Edge Cases
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.distance import (
    Mahalanobis,
    RobustMahalanobis,
)


# =========================================================
# PERFECT COLLINEARITY
# =========================================================


def test_mahalanobis_perfect_collinearity():

    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 100],
            "x2": [2, 4, 6, 8, 10, 200],
        }
    )

    result = Mahalanobis.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


def test_robust_mahalanobis_perfect_collinearity():

    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 100],
            "x2": [2, 4, 6, 8, 10, 200],
        }
    )

    result = RobustMahalanobis.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


# =========================================================
# CONSTANT COLUMN
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_constant_column(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                1,
                2,
                3,
                4,
                5,
                100,
            ],
            "constant": [
                10,
                10,
                10,
                10,
                10,
                10,
            ],
        }
    )

    result = detector.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


# =========================================================
# SINGLE NUMERIC COLUMN
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_single_column(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x": [
                1,
                2,
                3,
                4,
                5,
                100,
            ]
        }
    )

    result = detector.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


# =========================================================
# ALL MISSING
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_all_missing(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                np.nan,
                np.nan,
            ],
            "x2": [
                np.nan,
                np.nan,
            ],
        }
    )

    with pytest.raises(
        (
            ValueError,
            RuntimeError,
            np.linalg.LinAlgError,
        )
    ):
        detector.detect(
            dataframe
        )


# =========================================================
# INFINITE VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_infinite_values(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
                np.inf,
                4.0,
            ],
            "x2": [
                1.0,
                2.0,
                3.0,
                4.0,
            ],
        }
    )

    with pytest.raises(
        (
            ValueError,
            RuntimeError,
            np.linalg.LinAlgError,
        )
    ):
        detector.detect(
            dataframe
        )


# =========================================================
# SMALL SAMPLE
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_small_sample(
    detector,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
            ],
            "x2": [
                1.0,
                2.0,
            ],
            "x3": [
                1.0,
                2.0,
            ],
        }
    )

    with pytest.raises(
        (
            ValueError,
            RuntimeError,
            np.linalg.LinAlgError,
        )
    ):
        detector.detect(
            dataframe
        )
