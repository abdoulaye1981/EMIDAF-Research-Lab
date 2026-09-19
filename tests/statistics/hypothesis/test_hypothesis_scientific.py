import numpy as np
import pandas as pd
import pytest
from scipy import stats

from emidaf_core.statistics.hypothesis import (
    ShapiroTest,
    LeveneTest,
    BartlettTest,
    OneSampleTTest,
    IndependentTTest,
    PairedTTest,
    OneSampleProportionTest,
    TwoSampleProportionTest,
    ChiSquareIndependenceTest,
    ChiSquareGoodnessOfFitTest,
    MannWhitneyTest,
    WilcoxonTest,
    KruskalWallisTest,
    FriedmanTest,
    SpearmanTest,
    MoodMedianTest,
    SignTest,
    MultipleTesting,
)


# ==========================================================
# Helpers
# ==========================================================

def statistic(result):
    if hasattr(result, "statistic"):
        return float(result.statistic)

    if isinstance(result, dict):
        for key in (
            "statistic",
            "chi2",
            "u_statistic",
            "w_statistic",
            "h_statistic",
        ):
            if key in result:
                return float(result[key])

    raise AssertionError(
        f"Statistic inaccessible: {result!r}"
    )


def pvalue(result):
    if hasattr(result, "p_value"):
        return float(result.p_value)

    if isinstance(result, dict):
        for key in (
            "p_value",
            "pvalue",
        ):
            if key in result:
                return float(result[key])

    raise AssertionError(
        f"P-value inaccessible: {result!r}"
    )


# ==========================================================
# NORMALITY
# ==========================================================

def test_shapiro_matches_scipy():
    data = np.array(
        [1.2, 1.8, 2.1, 2.4, 2.9, 3.3, 3.7, 4.1]
    )

    expected = stats.shapiro(data)

    result = ShapiroTest().test(data)

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# VARIANCE
# ==========================================================

def test_levene_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5], dtype=float)
    g2 = np.array([2, 3, 4, 5, 6], dtype=float)

    expected = stats.levene(
        g1,
        g2,
    )

    result = LeveneTest().test(
        g1,
        g2,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


def test_bartlett_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5], dtype=float)
    g2 = np.array([2, 3, 5, 7, 9], dtype=float)

    expected = stats.bartlett(
        g1,
        g2,
    )

    result = BartlettTest().test(
        g1,
        g2,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# ONE SAMPLE T TEST
# ==========================================================

def test_one_sample_t_matches_scipy():
    data = np.array(
        [10, 11, 9, 12, 13, 10, 11],
        dtype=float,
    )

    expected = stats.ttest_1samp(
        data,
        popmean=10,
    )

    result = OneSampleTTest().test(
        data,
        population_mean=10,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# INDEPENDENT T TEST
# ==========================================================

def test_independent_student_t_matches_scipy():
    g1 = np.array(
        [10, 11, 12, 13, 14],
        dtype=float,
    )

    g2 = np.array(
        [7, 8, 9, 10, 11],
        dtype=float,
    )

    expected = stats.ttest_ind(
        g1,
        g2,
        equal_var=True,
    )

    result = IndependentTTest(
        equal_var=True
    ).test(
        g1,
        g2,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


def test_independent_welch_t_matches_scipy():
    g1 = np.array(
        [1, 2, 3, 4, 20],
        dtype=float,
    )

    g2 = np.array(
        [5, 6, 7, 8, 9],
        dtype=float,
    )

    expected = stats.ttest_ind(
        g1,
        g2,
        equal_var=False,
    )

    result = IndependentTTest(
        equal_var=False
    ).test(
        g1,
        g2,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# PAIRED T TEST
# ==========================================================

def test_paired_t_matches_scipy():
    before = np.array(
        [10, 12, 14, 16, 18],
        dtype=float,
    )

    after = np.array(
        [9, 11, 13, 14, 17],
        dtype=float,
    )

    expected = stats.ttest_rel(
        before,
        after,
    )

    result = PairedTTest().test(
        before,
        after,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# ONE SAMPLE PROPORTION
# ==========================================================

def test_one_sample_proportion_valid_pvalue():
    result = OneSampleProportionTest().test(
        successes=60,
        n=100,
        population_proportion=0.5,
    )

    assert np.isfinite(
        statistic(result)
    )

    assert 0.0 <= pvalue(result) <= 1.0


# ==========================================================
# TWO SAMPLE PROPORTIONS
# ==========================================================

def test_two_sample_proportion_valid_pvalue():
    result = TwoSampleProportionTest().test(
        successes1=60,
        n1=100,
        successes2=45,
        n2=100,
    )

    assert np.isfinite(
        statistic(result)
    )

    assert 0.0 <= pvalue(result) <= 1.0


# ==========================================================
# CHI-SQUARE INDEPENDENCE
# ==========================================================

def test_chi_square_independence_matches_scipy():
    df = pd.DataFrame(
        {
            "gender": [
                "F", "F", "F", "F",
                "M", "M", "M", "M",
            ],
            "choice": [
                "A", "A", "A", "B",
                "A", "B", "B", "B",
            ],
        }
    )

    table = pd.crosstab(
        df["gender"],
        df["choice"],
    )

    expected = stats.chi2_contingency(
        table
    )

    result = ChiSquareIndependenceTest().test(
        df,
        row="gender",
        column="choice",
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# CHI-SQUARE GOODNESS OF FIT
# ==========================================================

def test_chi_square_goodness_of_fit_uniform():
    observed = np.array(
        [20, 20, 20, 20]
    )

    result = ChiSquareGoodnessOfFitTest().test(
        observed
    )

    assert statistic(result) == pytest.approx(
        0.0
    )

    assert pvalue(result) == pytest.approx(
        1.0
    )


# ==========================================================
# MANN-WHITNEY
# ==========================================================

def test_mann_whitney_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([6, 7, 8, 9, 10])

    expected = stats.mannwhitneyu(
        g1,
        g2,
        alternative="two-sided",
    )

    result = MannWhitneyTest().test(
        g1,
        g2,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# WILCOXON
# ==========================================================

def test_wilcoxon_matches_scipy():
    before = np.array(
        [10, 12, 14, 16, 18]
    )

    after = np.array(
        [9, 11, 13, 15, 16]
    )

    expected = stats.wilcoxon(
        before,
        after,
        alternative="two-sided",
    )

    result = WilcoxonTest().test(
        before,
        after,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# KRUSKAL-WALLIS
# ==========================================================

def test_kruskal_matches_scipy():
    g1 = np.array([1, 2, 3, 4])
    g2 = np.array([5, 6, 7, 8])
    g3 = np.array([9, 10, 11, 12])

    expected = stats.kruskal(
        g1,
        g2,
        g3,
    )

    result = KruskalWallisTest().test(
        g1,
        g2,
        g3,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# FRIEDMAN
# ==========================================================

def test_friedman_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([2, 3, 4, 5, 6])
    g3 = np.array([3, 4, 5, 6, 7])

    expected = stats.friedmanchisquare(
        g1,
        g2,
        g3,
    )

    result = FriedmanTest().test(
        g1,
        g2,
        g3,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# SPEARMAN
# ==========================================================

def test_spearman_hypothesis_matches_scipy():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 4, 9, 16, 25])

    expected = stats.spearmanr(
        x,
        y,
    )

    result = SpearmanTest().test(
        x,
        y,
    )

    assert statistic(result) == pytest.approx(
        expected.statistic
    )

    assert pvalue(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# MOOD MEDIAN
# ==========================================================

def test_mood_median_valid_result():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([6, 7, 8, 9, 10])

    result = MoodMedianTest().test(
        g1,
        g2,
    )

    assert np.isfinite(
        statistic(result)
    )

    assert 0.0 <= pvalue(result) <= 1.0


# ==========================================================
# SIGN TEST
# ==========================================================

def test_sign_test_valid_result():
    before = np.array(
        [10, 10, 10, 10, 10, 10]
    )

    after = np.array(
        [11, 12, 11, 9, 12, 11]
    )

    result = SignTest().test(
        before,
        after,
    )

    assert np.isfinite(
        statistic(result)
    )

    assert 0.0 <= pvalue(result) <= 1.0


# ==========================================================
# MULTIPLE TESTING
# ==========================================================

def test_bonferroni_adjustment_bounds():
    p_values = np.array(
        [0.01, 0.02, 0.20, 0.80]
    )

    result = MultipleTesting(
        alpha=0.05
    ).adjust(
        p_values,
        method="bonferroni",
    )

    assert result is not None


def test_holm_adjustment_bounds():
    p_values = np.array(
        [0.01, 0.02, 0.20, 0.80]
    )

    result = MultipleTesting(
        alpha=0.05
    ).adjust(
        p_values,
        method="holm",
    )

    assert result is not None
