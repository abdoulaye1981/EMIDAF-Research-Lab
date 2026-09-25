import pandas as pd
import pytest

from emidaf_core.etae.engine import ETAEEngine
from emidaf_core.etae.preprocessing import (
    TextPreprocessingConfig,
    TextPreprocessor,
)


def test_lowercase_and_punctuation_removal():
    preprocessor = TextPreprocessor()

    result = preprocessor.process_text(
        "Bonjour, Les Mathématiques !"
    )

    assert (
        result.cleaned_text
        == "bonjour les mathématiques"
    )


def test_digits_can_be_preserved():
    preprocessor = TextPreprocessor(
        TextPreprocessingConfig(
            remove_digits=False
        )
    )

    result = preprocessor.process_text(
        "J'ai 15 sur 20."
    )

    assert "15" in result.tokens
    assert "20" in result.tokens


def test_digits_can_be_removed():
    preprocessor = TextPreprocessor(
        TextPreprocessingConfig(
            remove_digits=True
        )
    )

    result = preprocessor.process_text(
        "J'ai 15 sur 20."
    )

    assert "15" not in result.tokens
    assert "20" not in result.tokens


def test_stopwords_can_be_removed():
    preprocessor = TextPreprocessor(
        TextPreprocessingConfig(
            remove_stopwords=True
        )
    )

    result = preprocessor.process_text(
        "Le professeur est dans la classe"
    )

    assert "le" not in result.tokens
    assert "la" not in result.tokens


def test_negation_is_preserved():
    preprocessor = TextPreprocessor(
        TextPreprocessingConfig(
            remove_stopwords=True,
            preserve_negations=True,
        )
    )

    result = preprocessor.process_text(
        "Je ne comprends pas le cours"
    )

    assert "ne" in result.tokens
    assert "pas" in result.tokens


def test_original_text_is_preserved():
    text = (
        "Beaucoup de stress avant les examens."
    )

    result = (
        TextPreprocessor()
        .process_text(
            text
        )
    )

    assert result.original_text == text


def test_missing_values_become_empty_text():
    series = pd.Series(
        [
            "Bonjour",
            None,
        ]
    )

    results = (
        TextPreprocessor()
        .process_series(
            series
        )
    )

    assert len(results) == 2
    assert results[1].original_text == ""
    assert results[1].tokens == []


def test_process_series_rejects_non_series():
    with pytest.raises(
        TypeError,
        match="Series pandas",
    ):
        TextPreprocessor().process_series(
            ["Bonjour"]
        )


def test_engine_preprocesses_text_column():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant.",
                "Beaucoup de stress.",
            ]
        }
    )

    results = (
        ETAEEngine()
        .preprocess_text_column(
            dataframe,
            "review_text",
        )
    )

    assert len(results) == 2
    assert (
        results[0].cleaned_text
        == "professeur motivant"
    )


def test_engine_preserves_dataframe():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Texte ORIGINAL."
            ]
        }
    )

    original = dataframe.copy(
        deep=True
    )

    ETAEEngine().preprocess_text_column(
        dataframe,
        "review_text",
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )
