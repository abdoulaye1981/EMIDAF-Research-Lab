"""
=========================================================
EMIDAF Framework
Tests - Clustering Outlier Detection
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from emidaf_core.statistics.outliers.clustering import (
    BirchOutlier,
    GaussianMixtureOutlier,
    KMeansOutlier,
    MiniBatchKMeansOutlier,
)


# =========================================================
# FIXTURE
# =========================================================


@pytest.fixture
def clustering_dataframe() -> pd.DataFrame:

    rng = np.random.default_rng(42)

    cluster_1 = rng.normal(
        loc=[0.0, 0.0],
        scale=0.20,
        size=(100, 2),
    )

    cluster_2 = rng.normal(
        loc=[4.0, 4.0],
        scale=0.20,
        size=(100, 2),
    )

    normal = np.vstack(
        [
            cluster_1,
            cluster_2,
        ]
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
        15.0,
        15.0,
    ]

    return dataframe


# =========================================================
# KMEANS / MINI BATCH / GMM
# =========================================================


SCORED_DETECTORS = [
    (
        KMeansOutlier,
        {
            "n_clusters": 2,
            "percentile": 95,
            "random_state": 42,
        },
    ),
    (
        MiniBatchKMeansOutlier,
        {
            "n_clusters": 2,
            "percentile": 95,
            "random_state": 42,
        },
    ),
    (
        GaussianMixtureOutlier,
        {
            "n_components": 2,
            "percentile": 5,
            "random_state": 42,
        },
    ),
]


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_detector_detects_extreme_point(
    detector,
    kwargs,
    clustering_dataframe,
):

    result = detector.detect(
        clustering_dataframe,
        **kwargs,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_detector_preserves_custom_index(
    detector,
    kwargs,
    clustering_dataframe,
):

    result = detector.detect(
        clustering_dataframe,
        **kwargs,
    )

    original_index = set(
        clustering_dataframe.index
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


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_scores_match_observation_count(
    detector,
    kwargs,
    clustering_dataframe,
):

    result = detector.detect(
        clustering_dataframe,
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
    SCORED_DETECTORS,
)
def test_scored_clustering_counts_are_consistent(
    detector,
    kwargs,
    clustering_dataframe,
):

    result = detector.detect(
        clustering_dataframe,
        **kwargs,
    )

    assert (
        result.outlier_count
        + result.inlier_count
        == result.total_observations
    )


# =========================================================
# SCORE ORIENTATION
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_score_is_higher_for_extreme_anomaly(
    detector,
    kwargs,
    clustering_dataframe,
):
    """
    Contrat EMIDAF :

        score élevé = anomalie plus forte.
    """

    result = detector.detect(
        clustering_dataframe,
        **kwargs,
    )

    score_by_index = dict(
        zip(
            clustering_dataframe.index,
            result.scores,
        )
    )

    outlier_score = score_by_index[
        "row_OUTLIER"
    ]

    normal_scores = [
        score_by_index[index]
        for index
        in clustering_dataframe.index
        if index != "row_OUTLIER"
    ]

    assert (
        outlier_score
        >
        np.median(normal_scores)
    )


# =========================================================
# IMMUTABILITY
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_detector_does_not_mutate_input(
    detector,
    kwargs,
    clustering_dataframe,
):

    before = clustering_dataframe.copy(
        deep=True
    )

    detector.detect(
        clustering_dataframe,
        **kwargs,
    )

    pd.testing.assert_frame_equal(
        clustering_dataframe,
        before,
    )


# =========================================================
# NON NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_ignores_non_numeric_columns(
    detector,
    kwargs,
    clustering_dataframe,
):

    dataframe = clustering_dataframe.copy(
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


# =========================================================
# MISSING ROWS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_excludes_missing_rows(
    detector,
    kwargs,
    clustering_dataframe,
):

    dataframe = clustering_dataframe.copy(
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


# =========================================================
# BIRCH
# =========================================================


def test_birch_preserves_custom_index(
    clustering_dataframe,
):

    result = BirchOutlier.detect(
        clustering_dataframe,
        threshold=0.5,
    )

    original_index = set(
        clustering_dataframe.index
    )

    assert set(
        result.outlier_indices
    ).issubset(
        original_index
    )

    assert (
        set(result.outlier_indices)
        |
        set(result.inlier_indices)
        == original_index
    )


def test_birch_detects_isolated_small_cluster(
    clustering_dataframe,
):

    result = BirchOutlier.detect(
        clustering_dataframe,
        threshold=0.5,
    )

    assert (
        "row_OUTLIER"
        in result.outlier_indices
    )


def test_birch_has_no_continuous_scores(
    clustering_dataframe,
):

    result = BirchOutlier.detect(
        clustering_dataframe,
        threshold=0.5,
    )

    assert result.scores == []


def test_birch_labels_match_observation_count(
    clustering_dataframe,
):

    result = BirchOutlier.detect(
        clustering_dataframe,
        threshold=0.5,
    )

    assert (
        len(result.labels)
        == result.total_observations
    )


def test_birch_does_not_mutate_input(
    clustering_dataframe,
):

    before = clustering_dataframe.copy(
        deep=True
    )

    BirchOutlier.detect(
        clustering_dataframe,
        threshold=0.5,
    )

    pd.testing.assert_frame_equal(
        clustering_dataframe,
        before,
    )
