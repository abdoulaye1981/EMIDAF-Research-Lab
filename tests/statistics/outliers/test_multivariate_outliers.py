"""
=========================================================
EMIDAF Framework
Tests - Multivariate Outlier Detection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.multivariate import (
    MinimumCovarianceDeterminant,
    PCAOutlier,
    RobustPCAOutlier,
)


@pytest.fixture
def multivariate_dataframe() -> pd.DataFrame:

    rng = np.random.default_rng(42)

    normal = rng.normal(
        loc=0.0,
        scale=0.5,
        size=(200, 3),
    )

    dataframe = pd.DataFrame(
        normal,
        columns=[
            "x1",
            "x2",
            "x3",
        ],
        index=[
            f"row_{i}"
            for i in range(200)
        ],
    )

    dataframe.loc[
        "row_OUTLIER"
    ] = [
        10.0,
        10.0,
        10.0,
    ]

    return dataframe


DETECTORS = [
    (
        PCAOutlier,
        {
            "n_components": 2,
            "percentile": 95,
        },
    ),
    (
        RobustPCAOutlier,
        {
            "percentile": 97.5,
        },
    ),
    (
        MinimumCovarianceDeterminant,
        {
            "percentile": 97.5,
        },
    ),
]


COVARIANCE_DETECTORS = [
    (
        RobustPCAOutlier,
        {
            "percentile": 97.5,
        },
    ),
    (
        MinimumCovarianceDeterminant,
        {
            "percentile": 97.5,
        },
    ),
]

@pytest.mark.parametrize(
    "detector, kwargs",
    COVARIANCE_DETECTORS,
)

def test_multivariate_detector_detects_extreme_point(
    detector,
    kwargs,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_detector_preserves_custom_index(
    detector,
    kwargs,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    original_index = set(
        multivariate_dataframe.index
    )

    assert set(
        result.outlier_indices
    ).issubset(
        original_index
    )

    assert set(
        result.inlier_indices
    ).issubset(
        original_index
    )

    assert (
        set(result.outlier_indices)
        |
        set(result.inlier_indices)
        == original_index
    )



def test_pca_detects_orthogonal_reconstruction_anomaly():

    rng = np.random.default_rng(42)

    n = 500

    x1 = rng.normal(
        0.0,
        1.0,
        n,
    )

    x2 = rng.normal(
        0.0,
        1.0,
        n,
    )

    # Les observations normales sont presque contenues
    # dans un sous-espace bidimensionnel.
    x3 = (
        x1
        + x2
        + rng.normal(
            0.0,
            0.01,
            n,
        )
    )

    dataframe = pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "x3": x3,
        },
        index=[
            f"row_{i}"
            for i in range(n)
        ],
    )

    # Point qui viole fortement la structure
    # bidimensionnelle x3 ≈ x1 + x2.
    dataframe.loc[
        "row_OUTLIER"
    ] = [
        0.0,
        0.0,
        4.0,
    ]

    result = PCAOutlier.detect(
        dataframe,
        n_components=2,
        percentile=95,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


def test_pca_reconstruction_score_is_higher_for_orthogonal_anomaly():

    rng = np.random.default_rng(42)

    n = 500

    x1 = rng.normal(
        0.0,
        1.0,
        n,
    )

    x2 = rng.normal(
        0.0,
        1.0,
        n,
    )

    x3 = (
        x1
        + x2
        + rng.normal(
            0.0,
            0.01,
            n,
        )
    )

    dataframe = pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "x3": x3,
        },
        index=[
            f"row_{i}"
            for i in range(n)
        ],
    )

    dataframe.loc[
        "row_OUTLIER"
    ] = [
        0.0,
        0.0,
        4.0,
    ]

    result = PCAOutlier.detect(
        dataframe,
        n_components=2,
        percentile=95,
    )

    score_by_index = dict(
        zip(
            dataframe.index,
            result.scores,
        )
    )

    outlier_score = score_by_index[
        "row_OUTLIER"
    ]

    normal_scores = [
        score_by_index[index]
        for index in dataframe.index
        if index != "row_OUTLIER"
    ]

    assert (
        outlier_score
        >
        np.median(normal_scores)
    )

@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_scores_match_observation_count(
    detector,
    kwargs,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    assert (
        len(result.scores)
        == result.total_observations
    )

    assert all(
        np.isfinite(score)
        for score in result.scores
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    COVARIANCE_DETECTORS,
)
def test_multivariate_score_is_higher_for_extreme_anomaly(
    detector,
    kwargs,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    score_by_index = dict(
        zip(
            multivariate_dataframe.index,
            result.scores,
        )
    )

    outlier_score = score_by_index[
        "row_OUTLIER"
    ]

    normal_scores = [
        score_by_index[index]
        for index
        in multivariate_dataframe.index
        if index != "row_OUTLIER"
    ]

    assert (
        outlier_score
        >
        np.median(normal_scores)
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_counts_are_consistent(
    detector,
    kwargs,
    multivariate_dataframe,
):

    result = detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_detector_does_not_mutate_input(
    detector,
    kwargs,
    multivariate_dataframe,
):

    before = multivariate_dataframe.copy(
        deep=True
    )

    detector.detect(
        multivariate_dataframe,
        **kwargs,
    )

    pd.testing.assert_frame_equal(
        multivariate_dataframe,
        before,
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_detector_ignores_non_numeric_columns(
    detector,
    kwargs,
    multivariate_dataframe,
):

    dataframe = multivariate_dataframe.copy(
        deep=True
    )

    dataframe["category"] = "A"

    result = detector.detect(
        dataframe,
        **kwargs,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    DETECTORS,
)
def test_multivariate_detector_excludes_missing_rows(
    detector,
    kwargs,
    multivariate_dataframe,
):

    dataframe = multivariate_dataframe.copy(
        deep=True
    )

    dataframe.loc[
        "row_0",
        "x1",
    ] = np.nan

    result = detector.detect(
        dataframe,
        **kwargs,
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
