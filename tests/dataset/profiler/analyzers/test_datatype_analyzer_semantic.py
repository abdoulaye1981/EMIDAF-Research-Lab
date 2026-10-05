import pandas as pd

from emidaf_core.dataset.profiler.analyzers.datatype_analyzer import (
    DatatypeAnalyzer,
)
from emidaf_core.dataset.profiler.profile_context import (
    ProfileContext,
)


def build_result():
    df = pd.DataFrame(
        {
            "id_eleve": [
                "ELEVE_1",
                "ELEVE_2",
                "ELEVE_3",
                "ELEVE_4",
            ],
            "cycle": [
                "Moyen",
                "Secondaire",
                "Moyen",
                "Secondaire",
            ],
            "niveau": [
                "5e",
                "1ere",
                "4e",
                "2nde",
            ],
            "interet_maths": [
                1,
                2,
                4,
                5,
            ],
            "stress": [
                5,
                3,
                2,
                1,
            ],
            "usage_tice_maison": [
                0,
                1,
                1,
                0,
            ],
            "formation_continue": [
                1,
                1,
                0,
                0,
            ],
            "note_maths": [
                8.5,
                12.0,
                15.5,
                10.0,
            ],
            "genre": [
                "F",
                "M",
                "F",
                "M",
            ],
            "review_text": [
                (
                    "Je rencontre beaucoup de difficultés "
                    "en mathématiques."
                ),
                (
                    "Le professeur explique bien les "
                    "notions étudiées."
                ),
                (
                    "Je travaille régulièrement mes "
                    "exercices à la maison."
                ),
                (
                    "Le stress avant les évaluations "
                    "me pose problème."
                ),
            ],
        }
    )

    context = ProfileContext(
        dataframe=df
    )

    return DatatypeAnalyzer().analyze(
        context
    )


def test_detects_identifier_columns():
    result = build_result()

    assert result["identifier"] == [
        "id_eleve"
    ]

    assert result["semantic"]["identifier"] == [
        "id_eleve"
    ]


def test_detects_categorical_and_ordinal_columns():
    result = build_result()

    assert "cycle" in result["categorical"]
    assert "niveau" in result["categorical"]
    assert "genre" in result["categorical"]

    assert "niveau" in result["semantic"]["ordinal"]
    assert "interet_maths" in result["semantic"]["ordinal"]
    assert "stress" in result["semantic"]["ordinal"]


def test_detects_binary_numeric_columns():
    result = build_result()

    assert "usage_tice_maison" in result["boolean"]
    assert "formation_continue" in result["boolean"]

    assert "usage_tice_maison" not in result["numeric"]
    assert "formation_continue" not in result["numeric"]


def test_detects_free_text_columns():
    result = build_result()

    assert result["text"] == [
        "review_text"
    ]

    assert result["semantic"]["free_text"] == [
        "review_text"
    ]

    assert "review_text" not in result["categorical"]


def test_classification_is_exhaustive_and_exclusive():
    result = build_result()

    total = sum(
        result["count"].values()
    )

    assert total == 10

    groups = [
        result["numeric"],
        result["categorical"],
        result["boolean"],
        result["datetime"],
        result["text"],
        result["identifier"],
        result["unknown"],
    ]

    flattened = [
        column
        for group in groups
        for column in group
    ]

    assert len(flattened) == len(set(flattened))
