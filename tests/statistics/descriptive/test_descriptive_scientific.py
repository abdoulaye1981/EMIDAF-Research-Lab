from __future__ import annotations

import math

import numpy as np
import pytest

from emidaf_core.statistics.descriptive.location import (
    Mean,
    Median,
)

from emidaf_core.statistics.descriptive.dispersion import (
    Variance,
    StandardDeviation,
    InterquartileRange,
    CoefficientVariation,
)

from emidaf_core.statistics.descriptive.multivariate import (
    Covariance,
    EuclideanDistance,
)

from emidaf_core.statistics.descriptive.weighted import (
    WeightedMean,
    WeightedVariance,
)

from emidaf_core.statistics.descriptive.circular import (
    CircularMean,
    MeanDirection,
)


def test_mean():

    x = np.array([
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ])

    result = Mean().compute(x)

    assert result.value == pytest.approx(
        3.0
    )


def test_median():

    x = np.array([
        1.0,
        2.0,
        10.0,
        20.0,
        100.0,
    ])

    result = Median().compute(x)

    assert result.value == pytest.approx(
        10.0
    )


def test_variance_uses_sample_ddof_one():

    x = np.array([
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ])

    result = Variance().compute(x)

    expected = np.var(
        x,
        ddof=1,
    )

    assert result.value == pytest.approx(
        expected
    )

    assert result.value == pytest.approx(
        2.5
    )


def test_standard_deviation_uses_sample_ddof_one():

    x = np.array([
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ])

    result = StandardDeviation().compute(
        x
    )

    expected = np.std(
        x,
        ddof=1,
    )

    assert result.value == pytest.approx(
        expected
    )


def test_interquartile_range():

    x = np.array([
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    ])

    result = InterquartileRange().compute(
        x
    )

    expected = (
        np.percentile(x, 75)
        - np.percentile(x, 25)
    )

    assert result.value == pytest.approx(
        expected
    )

    assert result.value == pytest.approx(
        2.0
    )


def test_coefficient_variation():

    x = np.array([
        2.0,
        4.0,
        6.0,
        8.0,
    ])

    result = CoefficientVariation().compute(
        x
    )

    expected = (
        np.std(
            x,
            ddof=1,
        )
        / np.mean(x)
    )

    assert result.value == pytest.approx(
        expected
    )


def test_coefficient_variation_zero_mean():

    x = np.array([
        -1.0,
        1.0,
    ])

    result = CoefficientVariation().compute(
        x
    )

    assert math.isnan(
        result.value
    )


def test_covariance_uses_sample_covariance():

    x = np.array([
        1.0,
        2.0,
        3.0,
        4.0,
    ])

    y = np.array([
        2.0,
        4.0,
        6.0,
        8.0,
    ])

    result = Covariance().compute(
        x,
        y,
    )

    expected = np.cov(
        x,
        y,
        ddof=1,
    )[0, 1]

    assert result.value == pytest.approx(
        expected
    )


def test_euclidean_distance():

    x = np.array([
        0.0,
        0.0,
    ])

    y = np.array([
        3.0,
        4.0,
    ])

    result = EuclideanDistance().compute(
        x,
        y,
    )

    assert result.value == pytest.approx(
        5.0
    )


def test_weighted_mean():

    x = np.array([
        10.0,
        20.0,
        30.0,
    ])

    weights = np.array([
        1.0,
        2.0,
        1.0,
    ])

    result = WeightedMean().compute(
        x,
        weights,
    )

    expected = np.average(
        x,
        weights=weights,
    )

    assert result.value == pytest.approx(
        expected
    )

    assert result.value == pytest.approx(
        20.0
    )


def test_weighted_variance():

    x = np.array([
        10.0,
        20.0,
        30.0,
    ])

    weights = np.array([
        1.0,
        2.0,
        1.0,
    ])

    result = WeightedVariance().compute(
        x,
        weights,
    )

    mean = np.average(
        x,
        weights=weights,
    )

    expected = np.average(
        (x - mean) ** 2,
        weights=weights,
    )

    assert result.value == pytest.approx(
        expected
    )


def test_circular_mean_zero_direction():

    x = np.array([
        0.0,
        0.0,
        0.0,
    ])

    result = CircularMean().compute(x)

    assert result.value == pytest.approx(
        0.0
    )


def test_mean_direction_normalized_to_0_2pi():

    x = np.array([
        -np.pi / 2,
        -np.pi / 2,
    ])

    result = MeanDirection().compute(x)

    assert (
        0.0
        <= result.value
        < 2 * np.pi
    )

    assert result.value == pytest.approx(
        3 * np.pi / 2
    )
