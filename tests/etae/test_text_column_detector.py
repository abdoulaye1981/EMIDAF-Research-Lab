import pandas as pd
import pytest

from emidaf_core.etae import (
    ETAEEngine,
    TextColumnDetector,
)


def make_dataframe():
    return pd.DataFrame(
        {
            "id_eleve": [
                1,
                2,
                3,
                4,
            ],
            "genre": [
                "F",
                "M",
                "F",
                "M",
            ],
            "region": [
                "Dakar",
                "Thiès",
                "Dakar",
                "Kaolack",
            ],
            "cycle": [
                "Moyen",
                "Secondaire",
                "Moyen",
                "Secondaire",
            ],
            "review_text": [
                (
                    "Bonne ambiance en classe "
                    "et professeur disponible."
                ),
                (
                    "Beaucoup de stress avant "
                    "les examens de mathématiques."
                ),
                (
                    "La classe est trop chargée "
                    "et il est difficile de suivre."
                ),
                (
                    "Le professeur explique bien "
                    "et encourage les élèves."
                ),
            ],
        }
    )


def test_detects_free_text_column():
    dataframe = make_dataframe()

    detector = TextColumnDetector()

    columns = detector.text_columns(
        dataframe
    )

    assert "review_text" in columns


def test_does_not_detect_categories_as_free_text():
    dataframe = make_dataframe()

    columns = (
        TextColumnDetector()
        .text_columns(
            dataframe
        )
    )

    assert "genre" not in columns
    assert "region" not in columns
    assert "cycle" not in columns


def test_does_not_detect_numeric_column():
    dataframe = make_dataframe()

    columns = (
        TextColumnDetector()
        .text_columns(
            dataframe
        )
    )

    assert "id_eleve" not in columns


def test_candidate_diagnostics_available():
    dataframe = make_dataframe()

    candidates = (
        TextColumnDetector()
        .detect(
            dataframe
        )
    )

    review = next(
        candidate
        for candidate in candidates
        if candidate.column
        == "review_text"
    )

    assert review.is_text is True
    assert review.mean_characters > 20
    assert review.mean_words >= 3
    assert review.space_ratio > 0


def test_empty_string_column_not_text():
    dataframe = pd.DataFrame(
        {
            "empty_text": [
                "",
                " ",
                None,
            ]
        }
    )

    columns = (
        TextColumnDetector()
        .text_columns(
            dataframe
        )
    )

    assert columns == []


def test_invalid_dataframe_rejected():
    with pytest.raises(
        TypeError,
        match="DataFrame pandas",
    ):
        TextColumnDetector().detect(
            ["texte"]
        )


def test_engine_detects_text_columns():
    dataframe = make_dataframe()

    engine = ETAEEngine()

    columns = (
        engine.detect_text_columns(
            dataframe
        )
    )

    assert columns == [
        "review_text"
    ]
