import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.semantics import (
    TopicModeler,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress examen peur anxiété",
                "stress contrôle peur examen",
                "professeur motivant aide disponible",
                "enseignant motivant explication aide",
                "classe chargée effectif élevé",
                "classe surchargée difficile suivre",
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


def test_topic_modeling_basic(dataframe):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
    )

    assert result.method == "NMF"
    assert result.n_documents == 6
    assert result.n_topics == 3
    assert len(result.topics) == 3


def test_topic_assignments_match_documents(
    dataframe,
):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
    )

    assert (
        len(result.dominant_topics)
        == result.n_documents
    )


def test_topic_document_counts_sum(
    dataframe,
):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
    )

    total = sum(
        topic.document_count
        for topic in result.topics
    )

    assert total == result.n_documents


def test_topic_percentages_sum_to_100(
    dataframe,
):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
    )

    total = sum(
        topic.percentage
        for topic in result.topics
    )

    assert total == pytest.approx(
        100.0
    )


def test_topic_terms_available(
    dataframe,
):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
        top_terms=5,
    )

    assert all(
        topic.top_terms
        for topic in result.topics
    )


def test_topic_modeling_preserves_indices(
    dataframe,
):
    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=3,
    )

    assert result.indices == [
        10,
        20,
        30,
        40,
        50,
        60,
    ]


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

    result = TopicModeler().analyze(
        dataframe,
        "review_text",
        n_topics=2,
    )

    assert result.n_documents == 0
    assert result.topics == []
    assert result.dominant_topics == []


def test_invalid_topic_count(dataframe):
    with pytest.raises(
        ValueError,
        match="n_topics",
    ):
        TopicModeler().analyze(
            dataframe,
            "review_text",
            n_topics=1,
        )


def test_topic_count_less_than_documents(
    dataframe,
):
    with pytest.raises(
        ValueError,
        match="strictement inférieur",
    ):
        TopicModeler().analyze(
            dataframe,
            "review_text",
            n_topics=6,
        )


def test_engine_exposes_topic_modeling(
    dataframe,
):
    result = (
        ETAEEngine()
        .analyze_topics(
            dataframe,
            "review_text",
            n_topics=3,
        )
    )

    assert result.n_topics == 3
