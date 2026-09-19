"""
=========================================================
EMIDAF Framework
Tests - Statistical Outlier Detection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.statistical import (
    HampelFilter,
    IQR,
    ModifiedZScore,
    Percentile,
    ThreeSigma,
    TukeyFence,
    ZScore,
)

# =========================================================
# FIXTURES
# =========================================================


@pytest.fixture
def iqr_series() -> pd.Series:
    """
    Série simple contenant une valeur aberrante
    évidente selon la règle IQR.
    """

    return pd.Series(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            100,
        ],
        name="value",
    )


@pytest.fixture
def zscore_series() -> pd.Series:
    """
    Série permettant de produire un Z-score
    supérieur à 3 pour la dernière observation.
    """

    return pd.Series(
        [
            *np.zeros(100),
            100.0,
        ],
        name="value",
    )


@pytest.fixture
def modified_zscore_series() -> pd.Series:
    """
    Série avec MAD non nul et anomalie évidente.
    """

    return pd.Series(
        [
            -2,
            -1,
            -1,
            0,
            0,
            0,
            1,
            1,
            2,
            20,
        ],
        name="value",
    )


# =========================================================
# IQR
# =========================================================


def test_iqr_detects_extreme_value(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert result.outlier_count == 1
    assert result.outlier_indices == [10]
    assert result.outlier_values == [100]


def test_iqr_preserves_variable_name(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert result.variable == "value"


def test_iqr_method_name(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert result.method == "IQR"


def test_iqr_total_observations(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert (
        result.total_observations
        == len(iqr_series)
    )


def test_iqr_counts_are_consistent(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


def test_iqr_bounds_are_recorded(
    iqr_series,
):

    result = IQR.detect(
        iqr_series
    )

    assert (
        "lower_bound"
        in result.parameters
    )

    assert (
        "upper_bound"
        in result.parameters
    )

    assert (
        "iqr"
        in result.parameters
    )


def test_iqr_does_not_mutate_input(
    iqr_series,
):

    before = (
        iqr_series.copy(
            deep=True
        )
    )

    IQR.detect(
        iqr_series
    )

    pd.testing.assert_series_equal(
        iqr_series,
        before,
    )


# =========================================================
# Z SCORE
# =========================================================


def test_zscore_detects_extreme_value(
    zscore_series,
):

    result = ZScore.detect(
        zscore_series,
        threshold=3.0,
    )

    assert result.outlier_count == 1

    assert (
        result.outlier_indices
        == [100]
    )


def test_zscore_has_scores(
    zscore_series,
):

    result = ZScore.detect(
        zscore_series
    )

    assert (
        len(result.scores)
        == len(zscore_series)
    )


def test_zscore_method_name(
    zscore_series,
):

    result = ZScore.detect(
        zscore_series
    )

    assert (
        result.method
        == "Z-Score"
    )


def test_zscore_threshold_is_recorded(
    zscore_series,
):

    result = ZScore.detect(
        zscore_series,
        threshold=2.5,
    )

    assert result.threshold == 2.5


def test_zscore_fit_matches_detect(
    zscore_series,
):

    detect_result = (
        ZScore.detect(
            zscore_series
        )
    )

    fit_result = (
        ZScore.fit(
            zscore_series
        )
    )

    assert (
        fit_result.outlier_indices
        == detect_result.outlier_indices
    )


# =========================================================
# MODIFIED Z SCORE
# =========================================================


def test_modified_zscore_detects_extreme_value(
    modified_zscore_series,
):

    result = (
        ModifiedZScore.detect(
            modified_zscore_series
        )
    )

    assert result.outlier_count == 1

    assert (
        result.outlier_indices
        == [9]
    )

    assert (
        result.outlier_values
        == [20]
    )


def test_modified_zscore_method_name(
    modified_zscore_series,
):

    result = (
        ModifiedZScore.detect(
            modified_zscore_series
        )
    )

    assert (
        result.method
        == "Modified Z-Score"
    )


def test_modified_zscore_has_scores(
    modified_zscore_series,
):

    result = (
        ModifiedZScore.detect(
            modified_zscore_series
        )
    )

    assert (
        len(result.scores)
        == len(
            modified_zscore_series
        )
    )


def test_modified_zscore_zero_mad_is_safe():

    series = pd.Series(
        [
            5,
            5,
            5,
            5,
            5,
        ],
        name="constant",
    )

    result = (
        ModifiedZScore.detect(
            series
        )
    )

    assert result.outlier_count == 0

    assert all(
        score == 0
        for score
        in result.scores
    )


# =========================================================
# GENERAL CONSISTENCY
# =========================================================


@pytest.mark.parametrize(
    "detector, series",
    [
        (
            IQR,
            pd.Series(
                [1, 2, 3, 4, 100],
                name="x",
            ),
        ),
        (
            ZScore,
            pd.Series(
                [
                    *np.zeros(100),
                    100,
                ],
                name="x",
            ),
        ),
        (
            ModifiedZScore,
            pd.Series(
                [
                    -2,
                    -1,
                    0,
                    1,
                    2,
                    20,
                ],
                name="x",
            ),
        ),
    ],
)
def test_result_indices_are_valid(
    detector,
    series,
):

    result = detector.detect(
        series
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(series.index)
    )


@pytest.mark.parametrize(
    "detector",
    [
        IQR,
        ZScore,
        ModifiedZScore,
    ],
)
def test_numeric_array_is_accepted(
    detector,
):

    values = np.array(
        [
            1.0,
            2.0,
            3.0,
            4.0,
            100.0,
        ]
    )

    result = detector.detect(
        values
    )

    assert (
        result.total_observations
        == len(values)
    )

# =========================================================
# TUKEY FENCE
# =========================================================


def test_tukey_fence_matches_iqr():

    series = pd.Series(
        [
            1,
            2,
            3,
            4,
            5,
            100,
        ],
        name="value",
    )

    iqr_result = IQR.detect(
        series,
        factor=1.5,
    )

    tukey_result = TukeyFence.detect(
        series,
        factor=1.5,
    )

    assert (
        tukey_result.outlier_indices
        == iqr_result.outlier_indices
    )


def test_tukey_fence_method_name():

    series = pd.Series(
        [
            1,
            2,
            3,
            4,
            100,
        ],
        name="value",
    )

    result = TukeyFence.detect(
        series
    )

    # TukeyFence délègue actuellement à IQR.detect(),
    # donc la méthode retournée peut être "IQR".
    assert result.method in {
        "Tukey Fence",
        "IQR",
    }


# =========================================================
# PERCENTILE
# =========================================================


def test_percentile_detects_tail_values():

    series = pd.Series(
        np.arange(
            1,
            101,
            dtype=float,
        ),
        name="value",
    )

    result = Percentile.detect(
        series
    )

    assert (
        result.outlier_count
        > 0
    )


def test_percentile_indices_are_valid():

    series = pd.Series(
        np.arange(
            1,
            101,
            dtype=float,
        ),
        name="value",
    )

    result = Percentile.detect(
        series
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(series.index)
    )


# =========================================================
# THREE SIGMA
# =========================================================


def test_three_sigma_detects_extreme_value():

    series = pd.Series(
        [
            *np.zeros(100),
            100.0,
        ],
        name="value",
    )

    result = ThreeSigma.detect(
        series
    )

    assert result.outlier_count == 1

    assert (
        result.outlier_indices
        == [100]
    )


def test_three_sigma_counts_consistent():

    series = pd.Series(
        [
            *np.zeros(100),
            100.0,
        ],
        name="value",
    )

    result = ThreeSigma.detect(
        series
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


# =========================================================
# HAMPEL FILTER
# =========================================================


def test_hampel_filter_detects_local_extreme():

    series = pd.Series(
        [
            10,
            10,
            11,
            10,
            100,
            10,
            11,
            10,
            10,
        ],
        name="value",
    )

    result = HampelFilter.detect(
        series
    )

    assert (
        4
        in result.outlier_indices
    )


def test_hampel_filter_indices_are_valid():

    series = pd.Series(
        [
            10,
            10,
            11,
            10,
            100,
            10,
            11,
            10,
            10,
        ],
        name="value",
    )

    result = HampelFilter.detect(
        series
    )

    assert set(
        result.outlier_indices
    ).issubset(
        set(series.index)
    )


# =========================================================
# INPUT IMMUTABILITY
# =========================================================


@pytest.mark.parametrize(
    "detector",
    [
        TukeyFence,
        Percentile,
        ThreeSigma,
        HampelFilter,
    ],
)
def test_additional_detector_does_not_mutate_input(
    detector,
):

    series = pd.Series(
        [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            100.0,
        ],
        name="x",
    )

    before = series.copy(
        deep=True
    )

    detector.detect(
        series
    )

    pd.testing.assert_series_equal(
        series,
        before,
    )


# =========================================================
# SCIENTIFIC SCORE CONTRACT
# =========================================================


def test_modified_zscore_uses_raw_mad_definition():

    series = pd.Series(
        [
            1.0,
            2.0,
            3.0,
            4.0,
            10.0,
        ]
    )

    result = ModifiedZScore.detect(
        series,
        threshold=100.0,
    )

    median = np.median(series)

    raw_mad = np.median(
        np.abs(
            series - median
        )
    )

    expected = (
        0.6745
        * np.abs(
            series - median
        )
        / raw_mad
    )

    assert np.allclose(
        result.scores,
        expected,
    )


def test_modified_zscore_scores_follow_anomaly_direction():

    series = pd.Series(
        [
            -100.0,
            -2.0,
            -1.0,
            0.0,
            1.0,
            2.0,
            100.0,
        ]
    )

    result = ModifiedZScore.detect(
        series,
        threshold=1000.0,
    )

    assert all(
        score >= 0
        for score in result.scores
    )

    assert result.scores[0] > result.scores[1]

    assert result.scores[-1] > result.scores[-2]


def test_tukey_fence_preserves_method_identity():

    series = pd.Series(
        [
            1.0,
            2.0,
            2.0,
            3.0,
            100.0,
        ]
    )

    result = TukeyFence.detect(
        series
    )

    assert result.method == "Tukey Fence"


def test_three_sigma_preserves_method_identity():

    series = pd.Series(
        [
            *np.zeros(100),
            100.0,
        ]
    )

    result = ThreeSigma.detect(
        series
    )

    assert result.method == "Three Sigma"
