import pandas as pd

from emidaf_core.etae import ETAEEngine
from emidaf_core.etae.association import (
    SentimentAssociationAnalyzer,
    TopicTargetAnalyzer,
)
from emidaf_core.etae.interpretation import (
    AssociationInterpreter,
)


def make_dataframe():
    return pd.DataFrame(
        {
            "review_text": [
                "stress examen peur anxiété",
                "stress contrôle peur examen",
                "professeur motivant aide disponible",
                "enseignant motivant explication aide",
                "classe chargée effectif élevé",
                "classe surchargée difficile suivre",
            ],
            "note_maths": [
                7.0,
                8.0,
                15.0,
                14.0,
                9.0,
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
        }
    )


def test_interpret_topic_target():
    dataframe = make_dataframe()

    result = TopicTargetAnalyzer().analyze(
        dataframe,
        "review_text",
        "note_maths",
        n_topics=3,
    )

    interpretation = (
        AssociationInterpreter()
        .interpret_topic_target(
            result
        )
    )

    assert interpretation.statements
    assert (
        "note_maths"
        in interpretation.title
    )


def test_interpret_sentiment_numeric():
    dataframe = make_dataframe()

    result = (
        SentimentAssociationAnalyzer()
        .analyze_numeric(
            dataframe,
            "review_text",
            "note_maths",
        )
    )

    interpretation = (
        AssociationInterpreter()
        .interpret_sentiment_numeric(
            result
        )
    )

    assert interpretation.statements


def test_interpret_sentiment_categorical():
    dataframe = make_dataframe()

    result = (
        SentimentAssociationAnalyzer()
        .analyze_categorical(
            dataframe,
            "review_text",
            "niveau",
        )
    )

    interpretation = (
        AssociationInterpreter()
        .interpret_sentiment_categorical(
            result
        )
    )

    assert interpretation.statements


def test_engine_exposes_interpretation():
    dataframe = make_dataframe()

    engine = ETAEEngine()

    result = engine.analyze_sentiment_numeric(
        dataframe,
        "review_text",
        "note_maths",
    )

    interpretation = (
        engine.interpret_sentiment_numeric(
            result
        )
    )

    assert interpretation.statements
