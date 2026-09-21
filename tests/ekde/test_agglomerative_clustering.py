import pandas as pd
import pytest

from sklearn.preprocessing import StandardScaler

from emidaf_core.ekde import (
    AgglomerativeClusteringEngine,
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


def test_agglomerative_returns_model_result():
    dataframe = _scaled_dataframe()

    result = (
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="ward",
        )
    )

    assert (
        result.model_name
        == "Agglomerative Clustering"
    )
    assert (
        result.algorithm
        == "AgglomerativeClustering"
    )
    assert result.task == "clustering"
    assert result.fitted is True
    assert result.is_clusterer()


def test_agglomerative_returns_expected_partition():
    dataframe = _scaled_dataframe()

    result = (
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="ward",
        )
    )

    assert len(
        result.predictions
    ) == len(dataframe)

    assert len(
        set(result.predictions)
    ) == 3


def test_agglomerative_computes_metrics():
    dataframe = _scaled_dataframe()

    result = (
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="ward",
        )
    )

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


def test_agglomerative_ward_forces_euclidean():
    dataframe = _scaled_dataframe()

    result = (
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="ward",
            metric="manhattan",
        )
    )

    assert (
        result.parameters["metric"]
        == "euclidean"
    )


def test_agglomerative_accepts_average_manhattan():
    dataframe = _scaled_dataframe()

    result = (
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="average",
            metric="manhattan",
        )
    )

    assert (
        result.parameters["linkage"]
        == "average"
    )

    assert (
        result.parameters["metric"]
        == "manhattan"
    )


def test_agglomerative_rejects_non_numeric_variables():
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
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=2,
        )


def test_agglomerative_rejects_missing_values():
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
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=2,
        )


@pytest.mark.parametrize(
    "n_clusters",
    [
        0,
        1,
    ],
)
def test_agglomerative_rejects_too_few_clusters(
    n_clusters,
):
    dataframe = _scaled_dataframe()

    with pytest.raises(
        ValueError,
        match="au moins 2 clusters",
    ):
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=n_clusters,
        )


def test_agglomerative_rejects_too_many_clusters():
    dataframe = _scaled_dataframe()

    with pytest.raises(
        ValueError,
        match="strictement inférieur",
    ):
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=len(dataframe),
        )


def test_agglomerative_rejects_invalid_linkage():
    dataframe = _scaled_dataframe()

    with pytest.raises(
        ValueError,
        match="linkage",
    ):
        AgglomerativeClusteringEngine.fit(
            dataframe,
            n_clusters=3,
            linkage="invalid",
        )
