import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import (
    DatasetProfiler,
)


def test_normality_skips_semantic_ordinal_variables():
    df = pd.DataFrame(
        {
            "interet_maths": [
                1, 2, 3, 4, 5,
                1, 2, 3, 4, 5,
            ],
            "stress": [
                5, 4, 3, 2, 1,
                5, 4, 3, 2, 1,
            ],
            "note_maths": [
                8.0, 9.0, 10.0, 11.0, 12.0,
                13.0, 14.0, 15.0, 16.0, 17.0,
            ],
        }
    )

    result = DatasetProfiler().profile(
        df
    )

    normality = result.normality

    assert "interet_maths" not in normality["columns"]
    assert "stress" not in normality["columns"]
    assert "note_maths" in normality["columns"]

    assert set(
        normality["skipped"]["ordinal"]
    ) == {
        "interet_maths",
        "stress",
    }


def test_outlier_skips_semantic_ordinal_variables():
    df = pd.DataFrame(
        {
            "motivation": [
                1, 2, 3, 4, 5,
                1, 2, 3, 4, 5,
            ],
            "feedback_prof": [
                1, 1, 2, 2, 3,
                3, 4, 4, 5, 5,
            ],
            "note_maths": [
                0.0, 8.0, 9.0, 10.0, 11.0,
                12.0, 13.0, 14.0, 15.0, 20.0,
            ],
        }
    )

    result = DatasetProfiler().profile(
        df
    )

    outliers = result.outliers

    assert "motivation" not in outliers["columns"]
    assert "feedback_prof" not in outliers["columns"]
    assert "note_maths" in outliers["columns"]

    assert set(
        outliers["skipped"]["ordinal"]
    ) == {
        "motivation",
        "feedback_prof",
    }
