import numpy as np
import pytest
from scipy import stats

from emidaf_core.statistics.inferential.one_sample import (
    OneSampleTTest,
    OneSampleWilcoxon,
    OneSampleSignTest,
)

from emidaf_core.statistics.inferential.two_samples import (
    WelchTTest,
    KolmogorovSmirnovTest,
    BrunnerMunzelTest,
    MoodMedianTest,
)

from emidaf_core.statistics.inferential.paired import (
    PairedStudentTTest,
    WilcoxonSignedRankTest,
    PairedSignTest,
    PairedPermutationTest,
)

from emidaf_core.statistics.inferential.variance import (
    FisherVarianceTest,
    LeveneTest,
    BartlettTest,
    FlignerKilleenTest,
    BrownForsytheTest,
)


# ==========================================================
# Helpers
# ==========================================================

def stat_value(result):
    return float(result.statistic)


def p_value(result):
    return float(result.p_value)


# ==========================================================
# ONE SAMPLE
# ==========================================================

def test_one_sample_t_matches_scipy():
    x = np.array(
        [10, 11, 9, 12, 13, 10, 11],
        dtype=float,
    )

    expected = stats.ttest_1samp(
        x,
        popmean=10,
    )

    result = OneSampleTTest().compute(
        x=x,
        mu=10,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_one_sample_wilcoxon_matches_scipy():
    x = np.array(
        [1, 2, 3, 4, 5, 6],
        dtype=float,
    )

    mu = 3.0

    expected = stats.wilcoxon(
        x - mu
    )

    result = OneSampleWilcoxon().compute(
        x=x,
        mu=mu,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_one_sample_sign_test_valid():
    x = np.array(
        [1, 2, 3, 4, 5, 6, 7],
        dtype=float,
    )

    result = OneSampleSignTest().compute(
        x=x,
        median=4,
    )

    assert np.isfinite(
        stat_value(result)
    )

    assert 0.0 <= p_value(result) <= 1.0


# ==========================================================
# TWO SAMPLES
# ==========================================================

def test_welch_matches_scipy():
    x = np.array(
        [1, 2, 3, 4, 20],
        dtype=float,
    )

    y = np.array(
        [5, 6, 7, 8, 9],
        dtype=float,
    )

    expected = stats.ttest_ind(
        x,
        y,
        equal_var=False,
        nan_policy="omit",
    )

    result = WelchTTest().compute(
        x=x,
        y=y,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_kolmogorov_smirnov_matches_scipy():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 3, 4, 5, 6])

    expected = stats.ks_2samp(
        x,
        y,
    )

    result = KolmogorovSmirnovTest().compute(
        x=x,
        y=y,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_brunner_munzel_matches_scipy():
    x = np.array(
        [1, 2, 3, 4, 5, 6],
        dtype=float,
    )

    y = np.array(
        [3, 4, 5, 6, 7, 8],
        dtype=float,
    )

    expected = stats.brunnermunzel(
        x,
        y,
    )

    result = BrunnerMunzelTest().compute(
        x=x,
        y=y,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_mood_median_matches_scipy():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([6, 7, 8, 9, 10])

    expected = stats.median_test(
        x,
        y,
    )

    result = MoodMedianTest().compute(
        x=x,
        y=y,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


# ==========================================================
# PAIRED
# ==========================================================

def test_paired_student_matches_scipy():
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

    result = PairedStudentTTest().compute(
        before=before,
        after=after,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_wilcoxon_signed_rank_matches_scipy():
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

    result = WilcoxonSignedRankTest().compute(
        before=before,
        after=after,
        alternative="two-sided",
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_paired_sign_test_valid():
    before = np.array(
        [10, 10, 10, 10, 10, 10]
    )

    after = np.array(
        [11, 12, 11, 9, 12, 11]
    )

    result = PairedSignTest().compute(
        before=before,
        after=after,
    )

    assert np.isfinite(
        stat_value(result)
    )

    assert 0.0 <= p_value(result) <= 1.0


def test_paired_permutation_reproducible():
    before = np.array(
        [10, 12, 14, 16, 18, 20],
        dtype=float,
    )

    after = np.array(
        [11, 13, 15, 18, 19, 22],
        dtype=float,
    )

    r1 = PairedPermutationTest().compute(
        before=before,
        after=after,
        n_resamples=3000,
        random_state=42,
    )

    r2 = PairedPermutationTest().compute(
        before=before,
        after=after,
        n_resamples=3000,
        random_state=42,
    )

    assert stat_value(r1) == pytest.approx(
        np.mean(after - before)
    )

    assert p_value(r1) == pytest.approx(
        p_value(r2)
    )

    assert 0.0 <= p_value(r1) <= 1.0


# ==========================================================
# VARIANCE TESTS
# ==========================================================

def test_levene_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([2, 3, 4, 5, 6])

    expected = stats.levene(
        g1,
        g2,
        center="median",
    )

    result = LeveneTest().compute(
        g1,
        g2,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_bartlett_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([2, 3, 5, 7, 9])

    expected = stats.bartlett(
        g1,
        g2,
    )

    result = BartlettTest().compute(
        g1,
        g2,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_fligner_killeen_matches_scipy():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([2, 3, 5, 7, 9])

    expected = stats.fligner(
        g1,
        g2,
    )

    result = FlignerKilleenTest().compute(
        g1,
        g2,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_brown_forsythe_matches_levene_median():
    g1 = np.array([1, 2, 3, 4, 5])
    g2 = np.array([2, 3, 5, 7, 9])
    g3 = np.array([3, 4, 5, 6, 7])

    expected = stats.levene(
        g1,
        g2,
        g3,
        center="median",
    )

    result = BrownForsytheTest().compute(
        g1,
        g2,
        g3,
    )

    assert stat_value(result) == pytest.approx(
        expected.statistic
    )

    assert p_value(result) == pytest.approx(
        expected.pvalue
    )


def test_fisher_variance_valid_result():
    x = np.array(
        [1, 2, 3, 4, 5],
        dtype=float,
    )

    y = np.array(
        [1, 3, 5, 7, 9],
        dtype=float,
    )

    result = FisherVarianceTest().compute(
        x=x,
        y=y,
    )

    assert np.isfinite(
        stat_value(result)
    )

    assert 0.0 <= p_value(result) <= 1.0


# ==========================================================
# SERVICE CONTRACTS
# ==========================================================

def test_no_incomplete_two_sample_method_exposed():
    from emidaf_core.statistics.inferential.two_samples import (
        TwoSamples,
    )

    assert "fligner_policello" not in (
        TwoSamples.registry
    )


def test_no_incomplete_variance_methods_exposed():
    from emidaf_core.statistics.inferential.variance import (
        VarianceTests,
    )

    assert "obrien" not in (
        VarianceTests.registry
    )

    assert "box_m" not in (
        VarianceTests.registry
    )


def test_paired_permutation_is_exposed():
    from emidaf_core.statistics.inferential.paired import (
        Paired,
    )

    assert "permutation" in (
        Paired.registry
    )
