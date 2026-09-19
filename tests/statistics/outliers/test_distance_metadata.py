from __future__ import annotations

import numpy as np
import pandas as pd

from emidaf_core.statistics.outliers.distance import (
    CookDistance,
    Leverage,
    Mahalanobis,
    RobustMahalanobis,
)


def make_multivariate_dataframe():

    rng = np.random.default_rng(42)

    return pd.DataFrame(
        {
            "x1": rng.normal(
                0.0,
                1.0,
                100,
            ),
            "x2": rng.normal(
                0.0,
                1.0,
                100,
            ),
        }
    )


def make_regression_dataframe():

    rng = np.random.default_rng(42)

    x1 = rng.normal(
        0.0,
        1.0,
        100,
    )

    x2 = rng.normal(
        0.0,
        1.0,
        100,
    )

    y = (
        2.0
        + 3.0 * x1
        - 1.5 * x2
        + rng.normal(
            0.0,
            0.5,
            100,
        )
    )

    return pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "target": y,
        }
    )


def test_mahalanobis_metadata():

    result = Mahalanobis.detect(
        make_multivariate_dataframe()
    )

    assert result.method_family == "distance"

    assert (
        result.score_type
        == "mahalanobis_distance"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_robust_mahalanobis_metadata():

    result = RobustMahalanobis.detect(
        make_multivariate_dataframe()
    )

    assert result.method_family == "distance"

    assert (
        result.score_type
        == "robust_mahalanobis_distance"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_cook_distance_metadata():

    result = CookDistance.detect(
        make_regression_dataframe(),
        target="target",
    )

    assert result.method_family == "influence"

    assert (
        result.score_type
        == "cooks_distance"
    )

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_leverage_metadata():

    result = Leverage.detect(
        make_regression_dataframe(),
        target="target",
    )

    assert result.method_family == "influence"

    assert result.score_type == "leverage"

    assert (
        result.score_direction
        == "higher_is_more_anomalous"
    )

    assert result.scaling_sensitive is False


def test_mahalanobis_score_type_not_duplicated_in_parameters():

    result = Mahalanobis.detect(
        make_multivariate_dataframe()
    )

    assert "score_type" not in result.parameters


def test_robust_mahalanobis_score_type_not_duplicated_in_parameters():

    result = RobustMahalanobis.detect(
        make_multivariate_dataframe()
    )

    assert "score_type" not in result.parameters
