import numpy as np
import pytest
from scipy import stats
from statsmodels.stats.oneway import (
    anova_oneway,
)

from emidaf_core.statistics.inferential.k_samples import (
    OneWayANOVA,
    WelchANOVA,
    KruskalWallisTest,
    KSamples,
)


def stat_value(result):
    return float(
        result.statistic
    )


def p_value(result):
    return float(
        result.p_value
    )


def test_one_way_anova_matches_scipy():
    g1 = np.array(
        [10, 11, 12, 13, 14],
        dtype=float,
    )

    g2 = np.array(
        [12, 13, 14, 15, 16],
        dtype=float,
    )

    g3 = np.array(
        [15, 16, 17, 18, 19],
        dtype=float,
    )

    expected = stats.f_oneway(
        g1,
        g2,
        g3,
    )

    result = OneWayANOVA().compute(
        g1,
        g2,
        g3,
    )

    assert stat_value(
        result
    ) == pytest.approx(
        expected.statistic
    )

    assert p_value(
        result
    ) == pytest.approx(
        expected.pvalue
    )

    assert (
        result.metadata[
            "number_of_groups"
        ]
        == 3
    )


def test_welch_anova_matches_statsmodels():
    g1 = np.array(
        [5, 6, 7, 8, 9, 10],
        dtype=float,
    )

    g2 = np.array(
        [10, 12, 14, 16, 18, 20],
        dtype=float,
    )

    g3 = np.array(
        [7, 20, 25, 30, 35, 45],
        dtype=float,
    )

    expected = anova_oneway(
        [g1, g2, g3],
        use_var="unequal",
        welch_correction=True,
    )

    result = WelchANOVA().compute(
        g1,
        g2,
        g3,
    )

    assert stat_value(
        result
    ) == pytest.approx(
        expected.statistic
    )

    assert p_value(
        result
    ) == pytest.approx(
        expected.pvalue
    )

    assert (
        result.metadata[
            "variance_assumption"
        ]
        == "unequal"
    )


def test_kruskal_matches_scipy():
    g1 = np.array(
        [1, 2, 2, 3, 4],
        dtype=float,
    )

    g2 = np.array(
        [4, 5, 5, 6, 7],
        dtype=float,
    )

    g3 = np.array(
        [7, 8, 9, 9, 10],
        dtype=float,
    )

    expected = stats.kruskal(
        g1,
        g2,
        g3,
    )

    result = (
        KruskalWallisTest()
        .compute(
            g1,
            g2,
            g3,
        )
    )

    assert stat_value(
        result
    ) == pytest.approx(
        expected.statistic
    )

    assert p_value(
        result
    ) == pytest.approx(
        expected.pvalue
    )


def test_k_samples_registry():
    g1 = np.array(
        [1, 2, 3, 4],
        dtype=float,
    )

    g2 = np.array(
        [2, 3, 4, 5],
        dtype=float,
    )

    g3 = np.array(
        [3, 4, 5, 6],
        dtype=float,
    )

    result = KSamples.compute(
        "welch_anova",
        g1,
        g2,
        g3,
    )

    assert (
        result.test
        == "Welch ANOVA"
    )


def test_k_samples_rejects_invalid_method():
    with pytest.raises(
        ValueError,
        match="Méthode inconnue",
    ):
        KSamples.compute(
            "unknown",
            [1, 2],
            [3, 4],
        )


def test_k_samples_requires_two_groups():
    with pytest.raises(
        ValueError,
        match="Au moins deux groupes",
    ):
        OneWayANOVA().compute(
            [1, 2, 3]
        )


def test_k_samples_requires_two_values_per_group():
    with pytest.raises(
        ValueError,
        match="Chaque groupe",
    ):
        WelchANOVA().compute(
            [1],
            [2, 3, 4],
        )


def test_k_samples_ignores_nan_values():
    g1 = np.array(
        [1, 2, np.nan, 3, 4]
    )

    g2 = np.array(
        [2, 3, 4, np.nan, 5]
    )

    g3 = np.array(
        [4, 5, 6, 7, np.nan]
    )

    result = (
        KruskalWallisTest()
        .compute(
            g1,
            g2,
            g3,
        )
    )

    assert np.isfinite(
        result.statistic
    )

    assert (
        result.metadata[
            "group_sizes"
        ]
        == [4, 4, 4]
    )
