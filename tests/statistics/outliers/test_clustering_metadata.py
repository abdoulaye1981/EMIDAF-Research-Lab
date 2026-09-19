from __future__ import annotations

from emidaf_core.statistics.outliers.clustering import (
    BirchOutlier,
    GaussianMixtureOutlier,
    KMeansOutlier,
    MiniBatchKMeansOutlier,
)


def test_kmeans_metadata():

    assert KMeansOutlier.method_family == "clustering"
    assert KMeansOutlier.score_type == "distance_to_centroid"

    assert (
        KMeansOutlier.score_direction
        == "higher_is_more_anomalous"
    )

    assert KMeansOutlier.scaling_sensitive is True


def test_minibatch_kmeans_metadata():

    assert (
        MiniBatchKMeansOutlier.method_family
        == "clustering"
    )

    assert (
        MiniBatchKMeansOutlier.score_type
        == "distance_to_centroid"
    )

    assert (
        MiniBatchKMeansOutlier.score_direction
        == "higher_is_more_anomalous"
    )

    assert (
        MiniBatchKMeansOutlier.scaling_sensitive
        is True
    )


def test_birch_metadata():

    assert BirchOutlier.method_family == "clustering"
    assert BirchOutlier.score_type == ""
    assert BirchOutlier.score_direction == "none"
    assert BirchOutlier.scaling_sensitive is True


def test_gaussian_mixture_metadata():

    assert (
        GaussianMixtureOutlier.method_family
        == "clustering"
    )

    assert (
        GaussianMixtureOutlier.score_type
        == "negative_log_likelihood"
    )

    assert (
        GaussianMixtureOutlier.score_direction
        == "higher_is_more_anomalous"
    )

    assert (
        GaussianMixtureOutlier.scaling_sensitive
        is True
    )
