from __future__ import annotations

import pandas as pd

from emidaf_core.statistics.outliers.statistical import (
    HampelFilter,
    IQR,
    ModifiedZScore,
    Percentile,
    ThreeSigma,
    TukeyFence,
    ZScore,
)


SERIES = pd.Series(
    [
        1.0,
        2.0,
        3.0,
        4.0,
        100.0,
    ],
    name="x",
)


def test_zscore_metadata():

    result = ZScore.detect(
        SERIES
    )

    assert result.method_family == "statistical"

    assert (
        result.score_type
        == "absolute_z_score"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_modified_zscore_metadata():

    result = ModifiedZScore.detect(
        SERIES
    )

    assert result.method_family == "statistical"

    assert (
        result.score_type
        == "absolute_modified_z_score"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_iqr_metadata():

    result = IQR.detect(
        SERIES
    )

    assert result.method_family == "statistical"
    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.scaling_sensitive is False


def test_tukey_fence_metadata():

    result = TukeyFence.detect(
        SERIES
    )

    assert result.method_family == "statistical"
    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.scaling_sensitive is False


def test_percentile_metadata():

    result = Percentile.detect(
        SERIES
    )

    assert result.method_family == "statistical"
    assert result.score_type == ""
    assert result.score_direction == "none"
    assert result.scaling_sensitive is False


def test_three_sigma_metadata():

    result = ThreeSigma.detect(
        pd.Series(
            [
                *[0.0] * 100,
                100.0,
            ]
        )
    )

    assert result.method_family == "statistical"

    assert (
        result.score_type
        == "absolute_z_score"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_hampel_metadata():

    result = HampelFilter.detect(
        SERIES
    )

    assert result.method_family == "statistical"

    assert (
        result.score_type
        == "robust_deviation_score"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False
