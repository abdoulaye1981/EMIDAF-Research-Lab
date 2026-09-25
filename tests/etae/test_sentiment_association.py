import pandas as pd
import pytest

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.association.sentiment_association import (
    SentimentAssociationAnalyzer,
)


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant et disponible",
                "Cours intéressant et motivant",
                "Stress peur anxiété",
                "Beaucoup de stress et difficulté",
                "Cours demain matin",
                "Examen demain matin",
            ],
            "note_maths": [
                16.0,
                15.0,
                7.0,
                8.0,
                11.0,
                10.0,
            ],
            "niveau": [
                "3e",
                "3e",
                "2nde",
                "2nde",
                "3e",
                "2nde",
            ],
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


def test_numeric_association_basic(
    dataframe,
):
    result = (
        SentimentAssociationAnalyzer()
        .analyze_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    assert result.n_documents == 6
    assert len(result.groups) == 3


def test_numeric_groups_have_statistics(
    dataframe,
):
    result = (
        SentimentAssociationAnalyzer()
        .analyze_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    labels = {
        group.sentiment
        for group in result.groups
    }

    assert labels == {
        "negative",
        "neutral",
        "positive",
    }


def test_positive_group_mean_higher(
    dataframe,
):
    result = (
        SentimentAssociationAnalyzer()
        .analyze_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    means = {
        group.sentiment: group.mean
        for group in result.groups
    }

    assert (
        means["positive"]
        > means["negative"]
    )


def test_categorical_association_basic(
    dataframe,
):
    result = (
        SentimentAssociationAnalyzer()
        .analyze_categorical(
            dataframe,
            "review_text",
            "niveau",
        )
    )

    assert result.n_documents == 6

    assert (
        "positive"
        in result.contingency_table
    )

    assert (
        "negative"
        in result.contingency_table
    )


def test_unknown_target_rejected(
    dataframe,
):
    with pytest.raises(
        ValueError,
        match="Variable cible introuvable",
    ):
        (
            SentimentAssociationAnalyzer()
            .analyze_numeric(
                dataframe,
                "review_text",
                "unknown",
            )
        )


def test_non_numeric_target_rejected(
    dataframe,
):
    with pytest.raises(
        TypeError,
        match="doit être numérique",
    ):
        (
            SentimentAssociationAnalyzer()
            .analyze_numeric(
                dataframe,
                "review_text",
                "niveau",
            )
        )


def test_missing_target_excluded():
    dataframe = pd.DataFrame(
        {
            "review_text": [
                "Professeur motivant",
                "Stress examen",
                "Cours demain",
            ],
            "note_maths": [
                15.0,
                None,
                10.0,
            ],
        }
    )

    result = (
        SentimentAssociationAnalyzer()
        .analyze_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    assert result.n_documents == 2


def test_engine_numeric_association(
    dataframe,
):
    result = (
        ETAEEngine()
        .analyze_sentiment_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    assert (
        result.target_column
        == "note_maths"
    )


def test_engine_categorical_association(
    dataframe,
):
    result = (
        ETAEEngine()
        .analyze_sentiment_categorical(
            dataframe,
            "review_text",
            "niveau",
        )
    )

    assert (
        result.target_column
        == "niveau"
    )
