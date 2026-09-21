import pandas as pd
import pytest

from sklearn.preprocessing import StandardScaler

from emidaf_core.ekde import (
    KMeansClustering,
)


def _sample_dataframe():
    return pd.DataFrame(
        {
            "x1": [
                1.0, 1.1, 0.9,
                5.0, 5.2, 4.8,
                9.0, 9.1, 8.9,
            ],
            "x2": [
                1.0, 0.9, 1.1,
                5.0, 4.9, 5.1,
                9.0, 8.9, 9.1,
            ],
        }
    )


def _scaled_dataframe():
    dataframe = _sample_dataframe()

    return pd.DataFrame(
        StandardScaler().fit_transform(
            dataframe
        ),
        columns=dataframe.columns,
    )


def test_kmeans_clustering_returns_model_result():
    dataframe = _scaled_dataframe()

    result = KMeansClustering.fit(
        dataframe,
        n_clusters=3,
    )

    assert result.model_name == "K-Means"
    assert result.algorithm == "KMeans"
    assert result.task == "clustering"
    assert result.fitted is True
    assert result.is_clusterer()


def test_kmeans_clustering_returns_expected_shapes():
    dataframe = _scaled_dataframe()

    result = KMeansClustering.fit(
        dataframe,
        n_clusters=3,
    )

    assert len(result.predictions) == len(
        dataframe
    )

    assert len(
        result.cluster_centers
    ) == 3

    assert len(
        result.cluster_centers[0]
    ) == dataframe.shape[1]


def test_kmeans_clustering_computes_metrics():
    dataframe = _scaled_dataframe()

    result = KMeansClustering.fit(
        dataframe,
        n_clusters=3,
    )

    assert result.inertia is not None
    assert result.inertia >= 0

    assert (
        result.silhouette_score
        is not None
    )

    assert (
        result.davies_bouldin_score
        is not None
    )

    assert (
        result.calinski_harabasz_score
        is not None
    )


def test_kmeans_clustering_is_reproducible():
    dataframe = _scaled_dataframe()

    first = KMeansClustering.fit(
        dataframe,
        n_clusters=3,
        random_state=42,
    )

    second = KMeansClustering.fit(
        dataframe,
        n_clusters=3,
        random_state=42,
    )

    assert (
        first.predictions
        == second.predictions
    )

    assert (
        first.cluster_centers
        == second.cluster_centers
    )


def test_kmeans_rejects_non_numeric_variables():
    dataframe = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4],
            "group": [
                "A",
                "A",
                "B",
                "B",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="numériques",
    ):
        KMeansClustering.fit(
            dataframe,
            n_clusters=2,
        )


def test_kmeans_rejects_missing_values():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                2.0,
                None,
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
        ValueError,
        match="valeurs manquantes",
    ):
        KMeansClustering.fit(
            dataframe,
            n_clusters=2,
        )


def test_kmeans_rejects_invalid_cluster_number():
    dataframe = _scaled_dataframe()

    with pytest.raises(
        ValueError,
        match="au moins",
    ):
        KMeansClustering.fit(
            dataframe,
            n_clusters=1,
        )

    with pytest.raises(
        ValueError,
        match="strictement inférieur",
    ):
        KMeansClustering.fit(
            dataframe,
            n_clusters=len(dataframe),
        )
