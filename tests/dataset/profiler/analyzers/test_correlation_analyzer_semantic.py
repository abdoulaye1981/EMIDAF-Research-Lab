import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import (
    DatasetProfiler,
)


def test_spearman_is_default_correlation_method():

    df = pd.DataFrame(
        {
            "variable_x": [
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
            ],
            "variable_y": [
                2, 4, 6, 8, 10,
                12, 14, 16, 18, 20,
            ],
        }
    )

    profile = DatasetProfiler().profile(
        df
    )

    result = profile.correlations

    assert result[
        "default_method"
    ] == "spearman"

    assert (
        result["correlation_matrix"]
        ==
        result["spearman_matrix"]
    )

    assert result["pairs"]

    for pair in result["pairs"]:
        assert pair["method"] == "spearman"


def test_ordinal_pair_uses_spearman():

    df = pd.DataFrame(
        {
            "interet_maths": [
                1, 2, 3, 4, 5,
                1, 2, 3, 4, 5,
            ],
            "note_maths": [
                8.0, 9.0, 10.0, 11.0, 12.0,
                13.0, 14.0, 15.0, 16.0, 17.0,
            ],
        }
    )

    profile = DatasetProfiler().profile(
        df
    )

    result = profile.correlations

    pair = next(
        item
        for item in result["adaptive_pairs"]
        if {
            item["variable_1"],
            item["variable_2"],
        }
        == {
            "interet_maths",
            "note_maths",
        }
    )

    assert pair["method"] == "spearman"
    assert pair["reason"] == "ordinal_variable"


def test_adaptive_pairs_have_method_and_reason():

    df = pd.DataFrame(
        {
            "variable_a": [
                10.1, 10.4, 10.8, 11.0, 11.2,
                11.5, 11.9, 12.1, 12.4, 12.8,
                13.0, 13.2, 13.5, 13.8, 14.0,
                14.3, 14.5, 14.8, 15.0, 15.3,
            ],
            "variable_b": [
                20.2, 20.7, 21.1, 21.5, 21.8,
                22.0, 22.4, 22.7, 23.0, 23.3,
                23.7, 24.0, 24.2, 24.5, 24.8,
                25.0, 25.4, 25.7, 26.0, 26.2,
            ],
        }
    )

    profile = DatasetProfiler().profile(
        df
    )

    result = profile.correlations

    assert result["adaptive_pairs"]

    for pair in result["adaptive_pairs"]:

        assert pair["method"] in {
            "spearman",
            "pearson",
        }

        assert "reason" in pair
