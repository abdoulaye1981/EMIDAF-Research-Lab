import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.vectorization import (
    ETAETfidfVectorizer,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress avant examen",
                "stress avant devoir",
                "professeur motivant disponible",
                "mathématiques très intéressantes",
            ]
        }
    )


def test_tfidf_basic(dataframe):
    result = (
        ETAETfidfVectorizer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert result.n_documents == 4
    assert result.n_features > 0
    assert len(result.feature_names) > 0
    assert len(result.top_terms) > 0


def test_tfidf_sparsity(dataframe):
    result = (
        ETAETfidfVectorizer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert 0.0 <= result.sparsity <= 1.0


def test_tfidf_bigram(dataframe):
    result = (
        ETAETfidfVectorizer()
        .analyze(
            dataframe,
            "review_text",
            ngram_range=(1, 2),
        )
    )

    assert (
        "stress avant"
        in result.feature_names
    )


def test_tfidf_transform_preserves_indices():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "texte un",
                None,
                "",
                "texte deux",
            ]
        },
        index=[
            10,
            20,
            30,
            40,
        ],
    )

    matrix, vectorizer, indices = (
        ETAETfidfVectorizer()
        .transform(
            dataframe,
            "review_text",
        )
    )

    assert matrix.shape[0] == 2
    assert indices == [10, 40]
    assert len(
        vectorizer.get_feature_names_out()
    ) > 0


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

    result = (
        ETAETfidfVectorizer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert result.n_documents == 0
    assert result.n_features == 0
    assert result.feature_names == []


def test_unknown_column_rejected(dataframe):
    with pytest.raises(
        ValueError,
        match="Colonne textuelle introuvable",
    ):
        ETAETfidfVectorizer().analyze(
            dataframe,
            "unknown",
        )


def test_invalid_dataframe_rejected():
    with pytest.raises(
        TypeError,
        match="DataFrame pandas",
    ):
        ETAETfidfVectorizer().analyze(
            ["texte"],
            "review_text",
        )


def test_engine_exposes_tfidf(dataframe):
    result = (
        ETAEEngine()
        .analyze_tfidf(
            dataframe,
            "review_text",
            ngram_range=(1, 2),
        )
    )

    assert result.n_documents == 4
    assert result.n_features > 0
