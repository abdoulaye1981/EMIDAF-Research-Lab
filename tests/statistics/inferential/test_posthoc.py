import numpy as np
import pytest

from statsmodels.stats.multicomp import (
    pairwise_tukeyhsd,
)

from emidaf_core.statistics.inferential.posthoc import (
    TukeyHSD,
    GamesHowell,
    DunnHolm,
    AdaptivePostHoc,
)


def _example_groups():
    g1 = np.array(
        [10, 11, 12, 13, 14],
        dtype=float,
    )

    g2 = np.array(
        [10, 14, 18, 22, 26],
        dtype=float,
    )

    g3 = np.array(
        [15, 20, 25, 30, 35],
        dtype=float,
    )

    return g1, g2, g3


def _flatten(groups, labels):
    values = np.concatenate(
        groups
    )

    categories = np.concatenate(
        [
            np.repeat(
                label,
                len(group),
            )
            for label, group
            in zip(
                labels,
                groups,
            )
        ]
    )

    return values, categories


def test_tukey_matches_statsmodels():
    groups = _example_groups()

    labels = [
        "A",
        "B",
        "C",
    ]

    values, categories = (
        _flatten(
            groups,
            labels,
        )
    )

    expected = pairwise_tukeyhsd(
        values,
        categories,
        alpha=0.05,
        use_var="equal",
    )

    result = TukeyHSD().compute(
        *groups,
        labels=labels,
    )

    assert (
        result["method"]
        == "Tukey HSD"
    )

    assert (
        len(
            result[
                "comparisons"
            ]
        )
        == 3
    )

    for index, comparison in enumerate(
        result["comparisons"]
    ):
        assert (
            comparison[
                "p_value_adjusted"
            ]
            == pytest.approx(
                expected.pvalues[
                    index
                ]
            )
        )


def test_games_howell_matches_statsmodels():
    groups = _example_groups()

    labels = [
        "A",
        "B",
        "C",
    ]

    values, categories = (
        _flatten(
            groups,
            labels,
        )
    )

    expected = pairwise_tukeyhsd(
        values,
        categories,
        alpha=0.05,
        use_var="unequal",
    )

    result = GamesHowell().compute(
        *groups,
        labels=labels,
    )

    assert (
        result["method"]
        == "Games-Howell"
    )

    for index, comparison in enumerate(
        result["comparisons"]
    ):
        assert (
            comparison[
                "p_value_adjusted"
            ]
            == pytest.approx(
                expected.pvalues[
                    index
                ]
            )
        )


def test_dunn_holm_returns_all_pairs():
    g1 = np.array(
        [1, 1, 2, 2, 3],
        dtype=float,
    )

    g2 = np.array(
        [3, 4, 4, 5, 5],
        dtype=float,
    )

    g3 = np.array(
        [6, 7, 7, 8, 9],
        dtype=float,
    )

    result = DunnHolm().compute(
        g1,
        g2,
        g3,
        labels=[
            "A",
            "B",
            "C",
        ],
    )

    assert (
        result["method"]
        == "Dunn-Holm"
    )

    assert (
        result["correction"]
        == "Holm"
    )

    assert (
        len(
            result[
                "comparisons"
            ]
        )
        == 3
    )

    for comparison in result[
        "comparisons"
    ]:
        assert (
            0.0
            <= comparison[
                "p_value_adjusted"
            ]
            <= 1.0
        )


def test_dunn_holm_adjusted_p_not_below_raw_when_holm():
    g1 = np.array(
        [1, 2, 2, 3, 3],
        dtype=float,
    )

    g2 = np.array(
        [4, 5, 5, 6, 6],
        dtype=float,
    )

    g3 = np.array(
        [7, 8, 8, 9, 10],
        dtype=float,
    )

    result = DunnHolm().compute(
        g1,
        g2,
        g3,
    )

    for comparison in result[
        "comparisons"
    ]:
        assert (
            comparison[
                "p_value_adjusted"
            ]
            + 1e-15
            >=
            comparison[
                "p_value"
            ]
        )


def test_adaptive_posthoc_skips_two_groups():
    class DummyResult:
        reject_null = True

    selection = {
        "selected_test":
            "welch",
        "alpha":
            0.05,
        "result":
            DummyResult(),
    }

    output = AdaptivePostHoc.compute(
        selection,
        [1, 2, 3],
        [4, 5, 6],
    )

    assert (
        output["performed"]
        is False
    )

    assert (
        output["reason"]
        ==
        "two_groups_no_posthoc"
    )


def test_adaptive_posthoc_skips_non_significant_global_test():
    class DummyResult:
        reject_null = False

    selection = {
        "selected_test":
            "anova",
        "alpha":
            0.05,
        "result":
            DummyResult(),
    }

    output = AdaptivePostHoc.compute(
        selection,
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5],
    )

    assert (
        output["performed"]
        is False
    )

    assert (
        output["reason"]
        ==
        "global_test_not_significant"
    )


def test_adaptive_posthoc_uses_expected_method():
    class DummyResult:
        reject_null = True

    groups = _example_groups()

    cases = [
        (
            "anova",
            "Tukey HSD",
        ),
        (
            "welch_anova",
            "Games-Howell",
        ),
        (
            "kruskal",
            "Dunn-Holm",
        ),
    ]

    for selected, expected in cases:

        selection = {
            "selected_test":
                selected,
            "alpha":
                0.05,
            "result":
                DummyResult(),
        }

        output = AdaptivePostHoc.compute(
            selection,
            *groups,
            labels=[
                "A",
                "B",
                "C",
            ],
        )

        assert (
            output["performed"]
            is True
        )

        assert (
            output["method"]
            == expected
        )
