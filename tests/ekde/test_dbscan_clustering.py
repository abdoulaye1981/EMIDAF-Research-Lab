import pandas as pd
import pytest

from sklearn.preprocessing import StandardScaler

from emidaf_core.ekde import (
    DBSCANClustering,
)


def _sample_dataframe():
    return pd.DataFrame(
        {
            "x1": [
                1.0, 1.1, 0.9,
                5.0, 5.1, 4.9,
                20.0,
            ],
            "x2": [
                1.0, 0.9, 1.1,
                5.0, 5.1, 4.9,
                20.0,
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


def test_dbscan_returns_model_result():
    dataframe = _scaled_dataframe()

    result = DBSCANClustering.fit(
        dataframe,
        eps=0.35,
        min_samples=2,
    )

    assert result.model_name == "DBSCAN"
    assert result.algorithm == "DBSCAN"
    assert result.task == "clustering"
    assert result.fitted is True
    assert result.is_clusterer()


def test_dbscan_detects_clusters_and_noise():
    dataframe = _scaled_dataframe()

    result = DBSCANClustering.fit(
        dataframe,
        eps=0.35,
        min_samples=2,
    )

    assert len(result.predictions) == len(
        dataframe
    )

    assert (
        result.parameters["n_clusters"]
        == 2
    )

    assert (
        result.parameters["noise_count"]
        == 1
    )

    assert -1 in result.predictions


def test_dbscan_computes_metrics_when_valid():
    dataframe = _scaled_dataframe()

    result = DBSCANClustering.fit(
        dataframe,
        eps=0.35,
        min_samples=2,
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


def test_dbscan_keeps_metrics_none_when_no_valid_partition():
    dataframe = pd.DataFrame(
        {
            "x1": [
                1.0,
                1.0,
                1.0,
                1.0,
            ],
            "x2": [
                2.0,
                2.0,
                2.0,
                2.0,
            ],
        }
    )

    result = DBSCANClustering.fit(
        dataframe,
        eps=0.5,
        min_samples=2,
    )

    assert (
        result.parameters["n_clusters"]
        == 1
    )

    assert (
        result.silhouette_score
        is None
    )

    assert (
        result.davies_bouldin_score
        is None
    )

    assert (
        result.calinski_harabasz_score
        is None
    )


def test_dbscan_rejects_non_numeric_variables():
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
        DBSCANClustering.fit(
            dataframe,
            eps=0.5,
            min_samples=2,
        )


def test_dbscan_rejects_missing_values():
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
        DBSCANClustering.fit(
            dataframe,
            eps=0.5,
            min_samples=2,
        )


@pytest.mark.parametrize(
    "eps,min_samples",
    [
        (0, 2),
        (-0.1, 2),
        (0.5, 1),
    ],
)
def test_dbscan_rejects_invalid_parameters(
    eps,
    min_samples,
):
    dataframe = _scaled_dataframe()

    with pytest.raises(
        ValueError
    ):
        DBSCANClustering.fit(
            dataframe,
            eps=eps,
            min_samples=min_samples,
        )
