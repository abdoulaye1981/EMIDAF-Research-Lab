import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.semantics import (
    TextClusterer,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress examen peur anxiété",
                "stress devoir peur examen",
                "professeur motivant disponible aide",
                "enseignant disponible explication aide",
                "classe chargée difficile suivre",
                "effectif élevé classe chargée",
            ]
        },
        index=[
            10,
            20,
            30,
            40,
            50,
            60,
        ],
    )


def test_text_clustering_basic(dataframe):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
    )

    assert result.n_documents == 6
    assert result.n_clusters == 3
    assert len(result.labels) == 6
    assert len(result.clusters) == 3


def test_text_clustering_preserves_indices(
    dataframe,
):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
    )

    assert result.indices == [
        10,
        20,
        30,
        40,
        50,
        60,
    ]


def test_cluster_sizes_sum_to_documents(
    dataframe,
):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
    )

    total = sum(
        cluster.size
        for cluster in result.clusters
    )

    assert total == result.n_documents


def test_cluster_percentages_sum_to_100(
    dataframe,
):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
    )

    total = sum(
        cluster.percentage
        for cluster in result.clusters
    )

    assert total == pytest.approx(
        100.0
    )


def test_cluster_top_terms_available(
    dataframe,
):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
        top_terms=5,
    )

    assert all(
        cluster.top_terms
        for cluster in result.clusters
    )


def test_quality_metrics_available(
    dataframe,
):
    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=3,
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


def test_empty_corpus():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                None,
                "",
                " ",
            ]
        }
    )

    result = TextClusterer().analyze(
        dataframe,
        "review_text",
        n_clusters=2,
    )

    assert result.n_documents == 0
    assert result.clusters == []
    assert result.labels == []


def test_invalid_cluster_count(dataframe):
    with pytest.raises(
        ValueError,
        match="n_clusters",
    ):
        TextClusterer().analyze(
            dataframe,
            "review_text",
            n_clusters=1,
        )


def test_cluster_count_cannot_equal_documents(
    dataframe,
):
    with pytest.raises(
        ValueError,
        match="strictement inférieur",
    ):
        TextClusterer().analyze(
            dataframe,
            "review_text",
            n_clusters=6,
        )


def test_engine_exposes_text_clustering(
    dataframe,
):
    result = (
        ETAEEngine()
        .cluster_texts(
            dataframe,
            "review_text",
            n_clusters=3,
        )
    )

    assert result.n_clusters == 3
