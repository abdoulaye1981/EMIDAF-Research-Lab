import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.descriptive import (
    CorpusProfiler,
)


def test_profile_basic_corpus():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "J'aime les mathématiques.",
                "Beaucoup de stress avant les examens.",
                "Professeur motivant et disponible.",
            ]
        }
    )

    result = CorpusProfiler().profile(
        dataframe,
        "review_text",
    )

    assert result.n_documents == 3
    assert result.n_valid_documents == 3
    assert result.n_missing == 0
    assert result.n_empty == 0
    assert result.total_words > 0
    assert result.vocabulary_size > 0
    assert result.lexical_diversity > 0


def test_profile_handles_missing_and_empty():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Texte exploitable",
                None,
                "",
                "   ",
            ]
        }
    )

    result = CorpusProfiler().profile(
        dataframe,
        "review_text",
    )

    assert result.n_documents == 4
    assert result.n_valid_documents == 1
    assert result.n_missing == 1
    assert result.n_empty == 2


def test_profile_empty_corpus():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                None,
                "",
                " ",
            ]
        }
    )

    result = CorpusProfiler().profile(
        dataframe,
        "review_text",
    )

    assert result.n_valid_documents == 0
    assert result.total_words == 0
    assert result.vocabulary_size == 0
    assert result.lexical_diversity == 0.0


def test_unknown_text_column_rejected():
    dataframe = pd.DataFrame(
        {
            "review_text": ["Bonjour"]
        }
    )

    with pytest.raises(
        ValueError,
        match="Colonne textuelle introuvable",
    ):
        CorpusProfiler().profile(
            dataframe,
            "unknown",
        )


def test_invalid_dataframe_rejected():
    with pytest.raises(
        TypeError,
        match="DataFrame pandas",
    ):
        CorpusProfiler().profile(
            ["texte"],
            "review_text",
        )


def test_etae_engine_profiles_corpus():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Bonne ambiance en classe.",
                "Beaucoup de stress.",
            ]
        }
    )

    result = ETAEEngine().profile_corpus(
        dataframe,
        "review_text",
    )

    assert (
        result.text_column
        == "review_text"
    )
    assert result.n_documents == 2
