import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.sentiment import (
    LexiconSentimentAnalyzer,
)


def test_positive_text():
    analyzer = LexiconSentimentAnalyzer()

    result = analyzer.analyze_text(
        "Professeur motivant, disponible et encourageant."
    )

    assert result.score > 0
    assert result.label == "positive"
    assert result.matched_tokens > 0


def test_negative_text():
    analyzer = LexiconSentimentAnalyzer()

    result = analyzer.analyze_text(
        "Beaucoup de stress, peur et anxiété."
    )

    assert result.score < 0
    assert result.label == "negative"


def test_unknown_text_is_neutral():
    analyzer = LexiconSentimentAnalyzer()

    result = analyzer.analyze_text(
        "Le cours commence demain matin."
    )

    assert result.score == 0.0
    assert result.label == "neutral"
    assert result.coverage == 0.0


def test_negation_reverses_positive_term():
    analyzer = LexiconSentimentAnalyzer()

    result = analyzer.analyze_text(
        "Le cours n'est pas intéressant."
    )

    assert result.score < 0
    assert result.label == "negative"


def test_negation_reverses_negative_term():
    analyzer = LexiconSentimentAnalyzer()

    result = analyzer.analyze_text(
        "Je ne suis pas stressé."
    )

    assert result.score > 0


def test_custom_lexicon():
    analyzer = LexiconSentimentAnalyzer(
        lexicon={
            "excellent": 2.0,
            "mauvais": -2.0,
        }
    )

    positive = analyzer.analyze_text(
        "excellent"
    )

    negative = analyzer.analyze_text(
        "mauvais"
    )

    assert positive.score == 2.0
    assert negative.score == -2.0


def test_dataframe_analysis():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant et disponible",
                "Beaucoup de stress avant examen",
                "Cours demain matin",
            ]
        }
    )

    result = (
        LexiconSentimentAnalyzer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert result.n_documents == 3
    assert result.positive_count == 1
    assert result.negative_count == 1
    assert result.neutral_count == 1


def test_dataframe_preserves_indices():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant",
                "Stress examen",
            ]
        },
        index=[
            10,
            25,
        ],
    )

    result = (
        LexiconSentimentAnalyzer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert [
        item.index
        for item in result.documents
    ] == [
        10,
        25,
    ]


def test_missing_and_empty_are_excluded():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Texte motivant",
                None,
                "",
                " ",
            ]
        }
    )

    result = (
        LexiconSentimentAnalyzer()
        .analyze(
            dataframe,
            "review_text",
        )
    )

    assert result.n_documents == 1


def test_invalid_thresholds_rejected():
    with pytest.raises(
        ValueError,
        match="negative_threshold",
    ):
        LexiconSentimentAnalyzer(
            positive_threshold=-0.5,
            negative_threshold=0.5,
        )


def test_engine_exposes_sentiment():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant",
                "Stress et peur",
            ]
        }
    )

    result = (
        ETAEEngine()
        .analyze_sentiment(
            dataframe,
            "review_text",
        )
    )

    assert result.n_documents == 2
