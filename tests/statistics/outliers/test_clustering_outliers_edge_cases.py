"""
=========================================================
EMIDAF Framework
Tests - Clustering Outliers Edge Cases
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


# =========================================================
# INFINITE VALUES
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_rejects_infinite_values(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                np.inf,
                3.0,
                4.0,
                5.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


def test_birch_rejects_infinite_values():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                np.inf,
                3.0,
                4.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        BirchOutlier.detect(
            dataframe
        )


# =========================================================
# EMPTY COMPLETE DATASET
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_rejects_empty_complete_dataset(
    detector,
    kwargs,
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

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


def test_birch_rejects_empty_complete_dataset():

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

    with pytest.raises(ValueError):
        BirchOutlier.detect(
            dataframe
        )


# =========================================================
# NO NUMERIC COLUMNS
# =========================================================


@pytest.mark.parametrize(
    "detector, kwargs",
    SCORED_DETECTORS,
)
def test_scored_clustering_rejects_no_numeric_columns(
    detector,
    kwargs,
):

    dataframe = pd.DataFrame(
        {
            "category": [
                "A",
                "B",
                "C",
            ],
        }
    )

    with pytest.raises(ValueError):
        detector.detect(
            dataframe,
            **kwargs,
        )


def test_birch_rejects_no_numeric_columns():

    dataframe = pd.DataFrame(
        {
            "category": [
                "A",
                "B",
                "C",
            ],
        }
    )

    with pytest.raises(ValueError):
        BirchOutlier.detect(
            dataframe
        )


# =========================================================
# INVALID CLUSTER COUNTS
# =========================================================


def test_kmeans_rejects_more_clusters_than_samples():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                2.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        KMeansOutlier.detect(
            dataframe,
            n_clusters=5,
        )


def test_minibatch_kmeans_rejects_more_clusters_than_samples():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                2.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        MiniBatchKMeansOutlier.detect(
            dataframe,
            n_clusters=5,
        )


def test_gmm_rejects_more_components_than_samples():

    dataframe = pd.DataFrame(
        {
            "x1": [
                0.0,
                1.0,
                2.0,
            ],
            "x2": [
                0.0,
                1.0,
                2.0,
            ],
        }
    )

    with pytest.raises(ValueError):
        GaussianMixtureOutlier.detect(
            dataframe,
            n_components=5,
        )


# =========================================================
# INVALID PERCENTILES
# =========================================================


@pytest.mark.parametrize(
    "percentile",
    [
        -1,
        101,
    ],
)
def test_kmeans_rejects_invalid_percentile(
    percentile,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                20,
                dtype=float,
            ),
            "x2": np.arange(
                20,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        KMeansOutlier.detect(
            dataframe,
            n_clusters=2,
            percentile=percentile,
        )


@pytest.mark.parametrize(
    "percentile",
    [
        -1,
        101,
    ],
)
def test_minibatch_kmeans_rejects_invalid_percentile(
    percentile,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                20,
                dtype=float,
            ),
            "x2": np.arange(
                20,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        MiniBatchKMeansOutlier.detect(
            dataframe,
            n_clusters=2,
            percentile=percentile,
        )


@pytest.mark.parametrize(
    "percentile",
    [
        -1,
        101,
    ],
)
def test_gmm_rejects_invalid_percentile(
    percentile,
):

    dataframe = pd.DataFrame(
        {
            "x1": np.arange(
                20,
                dtype=float,
            ),
            "x2": np.arange(
                20,
                dtype=float,
            ),
        }
    )

    with pytest.raises(ValueError):
        GaussianMixtureOutlier.detect(
            dataframe,
            n_components=2,
            percentile=percentile,
        )


# =========================================================
# CONSTANT FEATURES
# =========================================================


def test_kmeans_handles_constant_features():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0] * 20,
            "x2": [2.0] * 20,
        }
    )

    result = KMeansOutlier.detect(
        dataframe,
        n_clusters=2,
        percentile=95,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


def test_minibatch_kmeans_handles_constant_features():

    dataframe = pd.DataFrame(
        {
            "x1": [1.0] * 20,
            "x2": [2.0] * 20,
        }
    )

    result = MiniBatchKMeansOutlier.detect(
        dataframe,
        n_clusters=2,
        percentile=95,
    )

    assert (
        result.total_observations
        == len(dataframe)
    )


# =========================================================
# REPRODUCIBILITY
# =========================================================


def test_kmeans_is_reproducible():

    rng = np.random.default_rng(42)

    dataframe = pd.DataFrame(
        rng.normal(
            size=(100, 3)
        ),
        columns=[
            "x1",
            "x2",
            "x3",
        ],
    )

    first = KMeansOutlier.detect(
        dataframe,
        n_clusters=3,
        random_state=42,
    )

    second = KMeansOutlier.detect(
        dataframe,
        n_clusters=3,
        random_state=42,
    )

    assert (
        first.outlier_indices
        == second.outlier_indices
    )

    np.testing.assert_allclose(
        first.scores,
        second.scores,
    )


def test_gmm_is_reproducible():

    rng = np.random.default_rng(42)

    dataframe = pd.DataFrame(
        rng.normal(
            size=(100, 3)
        ),
        columns=[
            "x1",
            "x2",
            "x3",
        ],
    )

    first = GaussianMixtureOutlier.detect(
        dataframe,
        n_components=3,
        random_state=42,
    )

    second = GaussianMixtureOutlier.detect(
        dataframe,
        n_components=3,
        random_state=42,
    )

    assert (
        first.outlier_indices
        == second.outlier_indices
    )

    np.testing.assert_allclose(
        first.scores,
        second.scores,
    )
