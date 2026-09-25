import math

import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.descriptive import (
    FrequencyAnalyzer,
)
from emidaf_core.etae.preprocessing import (
    TextPreprocessingConfig,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress avant examen",
                "stress avant cours",
                "professeur motivant",
            ]
        }
    )


def test_unigram_frequency(dataframe):
    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        ngram_size=1,
        top_n=None,
    )

    counts = {
        item.term: item.count
        for item in result.items
    }

    assert counts["stress"] == 2
    assert counts["avant"] == 2
    assert counts["examen"] == 1


def test_relative_frequency(dataframe):
    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        ngram_size=1,
        top_n=None,
    )

    total_relative = sum(
        item.relative_frequency
        for item in result.items
    )

    assert math.isclose(
        total_relative,
        1.0,
        rel_tol=1e-9,
    )


def test_bigram_frequency(dataframe):
    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        ngram_size=2,
        top_n=None,
    )

    counts = {
        item.term: item.count
        for item in result.items
    }

    assert counts["stress avant"] == 2
    assert counts["avant examen"] == 1


def test_trigram_frequency():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "beaucoup de stress avant examens",
                "beaucoup de stress en classe",
            ]
        }
    )

    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        ngram_size=3,
        top_n=None,
    )

    counts = {
        item.term: item.count
        for item in result.items
    }

    assert (
        counts["beaucoup de stress"]
        == 2
    )


def test_top_n_limits_results(dataframe):
    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        top_n=2,
    )

    assert len(result.items) == 2


def test_stopword_configuration(dataframe):
    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
        config=TextPreprocessingConfig(
            remove_stopwords=True
        ),
        top_n=None,
    )

    terms = {
        item.term
        for item in result.items
    }

    assert "avant" in terms


def test_missing_and_empty_text():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "mathématiques intéressantes",
                None,
                "",
                " ",
            ]
        }
    )

    result = FrequencyAnalyzer().analyze(
        dataframe,
        "review_text",
    )

    assert result.n_documents == 1
    assert result.total_tokens == 2


def test_invalid_ngram_size(dataframe):
    with pytest.raises(
        ValueError,
        match="ngram_size",
    ):
        FrequencyAnalyzer().analyze(
            dataframe,
            "review_text",
            ngram_size=0,
        )


def test_unknown_column_rejected(dataframe):
    with pytest.raises(
        ValueError,
        match="Colonne textuelle introuvable",
    ):
        FrequencyAnalyzer().analyze(
            dataframe,
            "unknown",
        )


def test_engine_analyzes_bigrams(dataframe):
    result = (
        ETAEEngine()
        .analyze_frequencies(
            dataframe,
            "review_text",
            ngram_size=2,
            top_n=10,
        )
    )

    assert result.ngram_size == 2
    assert any(
        item.term == "stress avant"
        for item in result.items
    )
