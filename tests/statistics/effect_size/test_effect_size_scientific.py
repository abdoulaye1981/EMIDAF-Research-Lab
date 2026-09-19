import numpy as np
import pytest
from scipy import stats

from emidaf_core.statistics.effect_size.mean_difference import (
    MeanDifferenceEffectSize,
)

from emidaf_core.statistics.effect_size.correlation import (
    CorrelationEffectSize,
)

from emidaf_core.statistics.effect_size.proportions import (
    ProportionEffectSize,
)

from emidaf_core.statistics.effect_size.contingency import (
    ContingencyEffectSize,
)

from emidaf_core.statistics.effect_size.regression import (
    RegressionEffectSize,
)

from emidaf_core.statistics.effect_size.anova import (
    AnovaEffectSize,
)

from emidaf_core.statistics.effect_size.nonparametric import (
    NonParametricEffectSize,
)


# ==========================================================
# Helpers
# ==========================================================

def value(result):
    if hasattr(result, "statistic"):
        return float(result.statistic)

    return float(result)


# ==========================================================
# MEAN DIFFERENCE
# ==========================================================

def test_pooled_sd():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 4, 6, 8, 10], dtype=float)

    n1 = len(x)
    n2 = len(y)

    expected = np.sqrt(
        (
            (n1 - 1) * np.var(x, ddof=1)
            +
            (n2 - 1) * np.var(y, ddof=1)
        )
        /
        (n1 + n2 - 2)
    )

    result = MeanDifferenceEffectSize.pooled_sd(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_cohen_d():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 3, 4, 5, 6], dtype=float)

    pooled = MeanDifferenceEffectSize.pooled_sd(
        x,
        y,
    )

    expected = (
        np.mean(x) - np.mean(y)
    ) / value(pooled)

    result = MeanDifferenceEffectSize.cohen_d(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_hedges_g_smaller_than_d_in_small_sample():
    x = np.array([1, 2, 3, 4], dtype=float)
    y = np.array([3, 4, 5, 6], dtype=float)

    d = abs(
        value(
            MeanDifferenceEffectSize.cohen_d(
                x,
                y,
            )
        )
    )

    g = abs(
        value(
            MeanDifferenceEffectSize.hedges_g(
                x,
                y,
            )
        )
    )

    assert g < d


def test_glass_delta():
    x = np.array([5, 6, 7, 8, 9], dtype=float)
    y = np.array([1, 2, 3, 4, 5], dtype=float)

    expected = (
        np.mean(x) - np.mean(y)
    ) / np.std(y, ddof=1)

    result = MeanDifferenceEffectSize.glass_delta(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_cohen_dz():
    x = np.array([10, 12, 15, 18, 20], dtype=float)
    y = np.array([9, 11, 13, 17, 18], dtype=float)

    diff = x - y

    expected = (
        np.mean(diff)
        /
        np.std(diff, ddof=1)
    )

    result = MeanDifferenceEffectSize.cohen_dz(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# CORRELATION
# ==========================================================

def test_pearson_effect_matches_scipy():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 4, 5, 4, 5], dtype=float)

    expected = stats.pearsonr(
        x,
        y,
    ).statistic

    result = CorrelationEffectSize.pearson(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_spearman_effect_matches_scipy():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([10, 20, 40, 30, 50], dtype=float)

    expected = stats.spearmanr(
        x,
        y,
    ).statistic

    result = CorrelationEffectSize.spearman(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_kendall_effect_matches_scipy():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([1, 3, 2, 5, 4], dtype=float)

    expected = stats.kendalltau(
        x,
        y,
    ).statistic

    result = CorrelationEffectSize.kendall(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_r_squared():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 4, 5, 4, 5], dtype=float)

    r = stats.pearsonr(
        x,
        y,
    ).statistic

    expected = r ** 2

    result = CorrelationEffectSize.r_squared(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_fisher_z():
    r = 0.5

    expected = np.arctanh(r)

    result = CorrelationEffectSize.fisher_z(
        r,
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# PROPORTIONS
# ==========================================================

def test_cohen_h():
    p1 = 0.60
    p2 = 0.40

    expected = (
        2 * np.arcsin(np.sqrt(p1))
        -
        2 * np.arcsin(np.sqrt(p2))
    )

    result = ProportionEffectSize.cohen_h(
        p1,
        p2,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_odds_ratio():
    a, b, c, d = 30, 20, 10, 40

    expected = (
        a * d
    ) / (
        b * c
    )

    result = ProportionEffectSize.odds_ratio(
        a,
        b,
        c,
        d,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_log_odds_ratio():
    a, b, c, d = 30, 20, 10, 40

    expected = np.log(
        (a * d) / (b * c)
    )

    result = ProportionEffectSize.log_odds_ratio(
        a,
        b,
        c,
        d,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_relative_risk():
    a, b, c, d = 30, 20, 10, 40

    risk1 = a / (a + b)
    risk2 = c / (c + d)

    expected = risk1 / risk2

    result = ProportionEffectSize.relative_risk(
        a,
        b,
        c,
        d,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_risk_difference():
    a, b, c, d = 30, 20, 10, 40

    risk1 = a / (a + b)
    risk2 = c / (c + d)

    expected = risk1 - risk2

    result = ProportionEffectSize.risk_difference(
        a,
        b,
        c,
        d,
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# CONTINGENCY
# ==========================================================

def test_phi():
    chi2 = 10.0
    n = 100

    expected = np.sqrt(
        chi2 / n
    )

    result = ContingencyEffectSize.phi(
        chi2,
        n,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_cramers_v():
    chi2 = 12.0
    n = 100
    rows = 3
    columns = 4

    expected = np.sqrt(
        chi2
        /
        (
            n
            * min(
                rows - 1,
                columns - 1,
            )
        )
    )

    result = ContingencyEffectSize.cramers_v(
        chi2,
        n,
        rows,
        columns,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_pearson_contingency():
    chi2 = 12.0
    n = 100

    expected = np.sqrt(
        chi2
        /
        (
            chi2 + n
        )
    )

    result = (
        ContingencyEffectSize
        .pearson_contingency(
            chi2,
            n,
        )
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# ANOVA
# ==========================================================

def test_eta_squared():
    ss_effect = 25.0
    ss_total = 100.0

    expected = 0.25

    result = AnovaEffectSize.eta_squared(
        ss_effect,
        ss_total,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_partial_eta_squared():
    ss_effect = 20.0
    ss_error = 80.0

    expected = (
        ss_effect
        /
        (
            ss_effect + ss_error
        )
    )

    result = (
        AnovaEffectSize
        .partial_eta_squared(
            ss_effect,
            ss_error,
        )
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_omega_squared():
    ss_effect = 30.0
    df_effect = 2
    ms_error = 5.0
    ss_total = 100.0

    expected = (
        ss_effect
        -
        df_effect * ms_error
    ) / (
        ss_total + ms_error
    )

    result = AnovaEffectSize.omega_squared(
        ss_effect,
        df_effect,
        ms_error,
        ss_total,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_cohen_f_from_eta_squared():
    eta2 = 0.20

    expected = np.sqrt(
        eta2 / (1 - eta2)
    )

    result = AnovaEffectSize.cohen_f(
        eta2,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_cohen_f2_from_eta_squared():
    eta2 = 0.20

    expected = (
        eta2 / (1 - eta2)
    )

    result = AnovaEffectSize.cohen_f2(
        eta2,
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# REGRESSION
# ==========================================================

def test_regression_r_squared():
    y_true = np.array(
        [1, 2, 3, 4, 5],
        dtype=float,
    )

    y_pred = np.array(
        [1.1, 1.9, 3.1, 3.8, 5.2],
        dtype=float,
    )

    ss_res = np.sum(
        (y_true - y_pred) ** 2
    )

    ss_tot = np.sum(
        (y_true - np.mean(y_true)) ** 2
    )

    expected = (
        1 - ss_res / ss_tot
    )

    result = RegressionEffectSize.r_squared(
        y_true,
        y_pred,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_regression_cohen_f2():
    r2 = 0.25

    expected = (
        r2 / (1 - r2)
    )

    result = RegressionEffectSize.cohen_f2(
        r2,
    )

    assert value(result) == pytest.approx(
        expected
    )


def test_regression_eta_squared():
    ss_model = 40.0
    ss_total = 100.0

    expected = 0.40

    result = RegressionEffectSize.eta_squared(
        ss_model,
        ss_total,
    )

    assert value(result) == pytest.approx(
        expected
    )


# ==========================================================
# NON PARAMETRIC
# ==========================================================

def test_cliffs_delta_complete_separation():
    x = np.array([4, 5, 6], dtype=float)
    y = np.array([1, 2, 3], dtype=float)

    result = NonParametricEffectSize.cliffs_delta(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        1.0
    )


def test_vargha_delaney_complete_separation():
    n1 = 3
    n2 = 3

    # Complete separation:
    # every observation in x exceeds every
    # observation in y, hence U = n1*n2.
    u = n1 * n2

    result = NonParametricEffectSize.vargha_delaney(
        u,
        n1,
        n2,
    )

    assert value(result) == pytest.approx(
        1.0
    )


def test_common_language_complete_separation():
    x = np.array([4, 5, 6], dtype=float)
    y = np.array([1, 2, 3], dtype=float)

    result = NonParametricEffectSize.common_language(
        x,
        y,
    )

    assert value(result) == pytest.approx(
        1.0
    )


def test_rank_biserial_bounds():
    u = 10
    n1 = 5
    n2 = 5

    expected = (
        2 * u
        /
        (n1 * n2)
    ) - 1

    result = NonParametricEffectSize.rank_biserial(
        u,
        n1,
        n2,
    )

    assert value(result) == pytest.approx(
        expected
    )

    assert -1.0 <= value(result) <= 1.0


# ==========================================================
# PUBLIC SCIENTIFIC CONTRACTS
# ==========================================================

def test_effect_size_placeholder_not_public():
    import emidaf_core.statistics.effect_size as es

    assert "EffectSize" not in es.__all__


def test_all_public_api_symbols_exist():
    import emidaf_core.statistics.effect_size as es

    for name in es.__all__:
        assert hasattr(
            es,
            name,
        )
