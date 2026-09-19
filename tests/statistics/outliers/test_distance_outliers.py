"""
=========================================================
EMIDAF Framework
Tests - Distance Based Outlier Detection
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
# FIXTURES
# =========================================================


@pytest.fixture
def multivariate_dataframe() -> pd.DataFrame:
    """
    Dataset bidimensionnel reproductible contenant
    une observation multivariée extrêmement éloignée.
    """

    rng = np.random.default_rng(42)

    normal_data = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(200, 2),
    )

    dataframe = pd.DataFrame(
        normal_data,
        columns=[
            "x1",
            "x2",
        ],
    )

    dataframe.loc[200] = [
        12.0,
        12.0,
    ]

    return dataframe


@pytest.fixture
def dataframe_with_missing_values(
    multivariate_dataframe,
) -> pd.DataFrame:
    """
    Dataset contenant des valeurs manquantes.
    Les détecteurs actuels utilisent dropna().
    """

    dataframe = (
        multivariate_dataframe.copy(
            deep=True
        )
    )

    dataframe.loc[0, "x1"] = np.nan
    dataframe.loc[1, "x2"] = np.nan

    return dataframe


# =========================================================
# MAHALANOBIS
# =========================================================


def test_mahalanobis_detects_extreme_observation(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        200
        in result.outlier_indices
    )


def test_mahalanobis_method_name(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.method
        == "Mahalanobis"
    )


def test_mahalanobis_total_observations(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.total_observations
        == len(multivariate_dataframe)
    )


def test_mahalanobis_scores_length(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        len(result.scores)
        == len(multivariate_dataframe)
    )


def test_mahalanobis_threshold_is_positive(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert result.threshold > 0


def test_mahalanobis_counts_are_consistent(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


def test_mahalanobis_indices_are_valid(
    multivariate_dataframe,
):

    result = Mahalanobis.detect(
        multivariate_dataframe
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(multivariate_dataframe.index)
    )


def test_mahalanobis_does_not_mutate_input(
    multivariate_dataframe,
):

    before = (
        multivariate_dataframe.copy(
            deep=True
        )
    )

    Mahalanobis.detect(
        multivariate_dataframe
    )

    pd.testing.assert_frame_equal(
        multivariate_dataframe,
        before,
    )


# =========================================================
# ROBUST MAHALANOBIS
# =========================================================


def test_robust_mahalanobis_detects_extreme_observation(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        200
        in result.outlier_indices
    )


def test_robust_mahalanobis_method_name(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.method
        == "Robust Mahalanobis"
    )


def test_robust_mahalanobis_total_observations(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.total_observations
        == len(multivariate_dataframe)
    )


def test_robust_mahalanobis_scores_length(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        len(result.scores)
        == len(multivariate_dataframe)
    )


def test_robust_mahalanobis_threshold_is_positive(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert result.threshold > 0


def test_robust_mahalanobis_counts_are_consistent(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


def test_robust_mahalanobis_indices_are_valid(
    multivariate_dataframe,
):

    result = RobustMahalanobis.detect(
        multivariate_dataframe
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(multivariate_dataframe.index)
    )


def test_robust_mahalanobis_does_not_mutate_input(
    multivariate_dataframe,
):

    before = (
        multivariate_dataframe.copy(
            deep=True
        )
    )

    RobustMahalanobis.detect(
        multivariate_dataframe
    )

    pd.testing.assert_frame_equal(
        multivariate_dataframe,
        before,
    )


# =========================================================
# MISSING VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_excludes_incomplete_rows(
    detector,
    dataframe_with_missing_values,
):

    result = detector.detect(
        dataframe_with_missing_values
    )

    expected_complete_rows = (
        dataframe_with_missing_values
        .dropna()
    )

    assert (
        result.total_observations
        == len(expected_complete_rows)
    )

    assert (
        0
        not in result.outlier_indices
    )

    assert (
        1
        not in result.outlier_indices
    )


# =========================================================
# NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_ignores_non_numeric_columns(
    detector,
    multivariate_dataframe,
):

    dataframe = (
        multivariate_dataframe.copy(
            deep=True
        )
    )

    dataframe["category"] = "A"

    result = detector.detect(
        dataframe
    )

    assert (
        result.total_observations
        == len(dataframe)
    )

    assert (
        200
        in result.outlier_indices
    )


# =========================================================
# REPRODUCIBILITY / BASIC CONTRACT
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_returns_scores(
    detector,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe
    )

    assert result.scores

    assert all(
        np.isfinite(score)
        for score
        in result.scores
    )


@pytest.mark.parametrize(
    "detector",
    [
        Mahalanobis,
        RobustMahalanobis,
    ],
)
def test_distance_detector_outlier_count_matches_indices(
    detector,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe
    )

    assert (
        result.outlier_count
        == len(
            result.outlier_indices
        )
    )
