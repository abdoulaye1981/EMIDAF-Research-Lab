import numpy as np
import pytest

from emidaf_core.statistics.power_analysis.ttest import (
    TTestAnalysis,
)

from emidaf_core.statistics.power_analysis.anova import (
    AnovaPowerAnalysis,
)

from emidaf_core.statistics.power_analysis.correlation import (
    CorrelationPowerAnalysis,
)

from emidaf_core.statistics.power_analysis.chi_square import (
    ChiSquarePowerAnalysis,
)

from emidaf_core.statistics.power_analysis.regression import (
    RegressionPowerAnalysis,
)

from emidaf_core.statistics.power_analysis.nonparametric import (
    NonParametricPowerAnalysis,
)

from emidaf_core.statistics.power_analysis.equivalence import (
    EquivalencePowerAnalysis,
)

from emidaf_core.statistics.power_analysis.sensitivity import (
    SensitivityAnalysis,
)

from emidaf_core.statistics.power_analysis.precision import (
    PrecisionAnalysis,
)


# ==========================================================
# Helpers
# ==========================================================

def get_power(result):
    if hasattr(result, "power"):
        return float(result.power)

    if isinstance(result, dict):
        return float(result["power"])

    return float(result)


def get_sample_size(result):
    if hasattr(result, "sample_size"):
        return float(result.sample_size)

    if isinstance(result, dict):
        return float(result["sample_size"])

    return float(result)


def get_effect_size(result):
    if hasattr(result, "effect_size"):
        return float(result.effect_size)

    if isinstance(result, dict):
        return float(result["effect_size"])

    return float(result)


# ==========================================================
# T TEST
# ==========================================================

def test_ttest_power_bounds():
    result = TTestAnalysis.compute_power(
        effect_size=0.5,
        sample_size=64,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_ttest_sample_size_positive():
    result = TTestAnalysis.compute_sample_size(
        effect_size=0.5,
        power=0.8,
        alpha=0.05,
    )

    assert get_sample_size(result) > 0


def test_ttest_power_increases_with_sample_size():
    small = TTestAnalysis.compute_power(
        effect_size=0.5,
        sample_size=20,
        alpha=0.05,
    )

    large = TTestAnalysis.compute_power(
        effect_size=0.5,
        sample_size=100,
        alpha=0.05,
    )

    assert get_power(large) > get_power(small)


def test_ttest_power_increases_with_effect_size():
    small = TTestAnalysis.compute_power(
        effect_size=0.2,
        sample_size=80,
        alpha=0.05,
    )

    large = TTestAnalysis.compute_power(
        effect_size=0.8,
        sample_size=80,
        alpha=0.05,
    )

    assert get_power(large) > get_power(small)


def test_ttest_solve_sample_size_consistency():
    result = TTestAnalysis.solve(
        effect_size=0.5,
        sample_size=None,
        alpha=0.05,
        power=0.8,
    )

    assert get_sample_size(result) > 0


# ==========================================================
# ANOVA
# ==========================================================

def test_anova_power_bounds():
    result = AnovaPowerAnalysis.compute_power(
        effect_size=0.25,
        groups=3,
        sample_size=120,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_anova_sample_size_positive():
    result = AnovaPowerAnalysis.compute_sample_size(
        effect_size=0.25,
        groups=3,
        power=0.8,
        alpha=0.05,
    )

    assert get_sample_size(result) > 0


def test_anova_power_increases_with_sample_size():
    small = AnovaPowerAnalysis.compute_power(
        effect_size=0.25,
        groups=3,
        sample_size=40,
        alpha=0.05,
    )

    large = AnovaPowerAnalysis.compute_power(
        effect_size=0.25,
        groups=3,
        sample_size=160,
        alpha=0.05,
    )

    assert get_power(large) > get_power(small)


# ==========================================================
# CORRELATION
# ==========================================================

def test_correlation_power_bounds():
    result = CorrelationPowerAnalysis.compute_power(
        effect_size=0.3,
        sample_size=100,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_correlation_sample_size_positive():
    result = CorrelationPowerAnalysis.compute_sample_size(
        effect_size=0.3,
        alpha=0.05,
        power=0.8,
    )

    assert get_sample_size(result) > 0


def test_correlation_power_increases_with_effect_size():
    small = CorrelationPowerAnalysis.compute_power(
        effect_size=0.1,
        sample_size=100,
        alpha=0.05,
    )

    large = CorrelationPowerAnalysis.compute_power(
        effect_size=0.5,
        sample_size=100,
        alpha=0.05,
    )

    assert get_power(large) > get_power(small)


# ==========================================================
# CHI-SQUARE
# ==========================================================

def test_chi_square_power_bounds():
    result = ChiSquarePowerAnalysis.compute_power(
        effect_size=0.3,
        sample_size=100,
        categories=4,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_chi_square_sample_size_positive():
    result = ChiSquarePowerAnalysis.compute_sample_size(
        effect_size=0.3,
        categories=4,
        alpha=0.05,
        power=0.8,
    )

    assert get_sample_size(result) > 0


def test_chi_square_effect_size_from_observed_expected():
    observed = np.array(
        [30, 25, 20, 25],
        dtype=float,
    )

    expected = np.array(
        [25, 25, 25, 25],
        dtype=float,
    )

    result = ChiSquarePowerAnalysis.compute_effect_size(
        observed,
        expected,
    )

    assert get_effect_size(result) >= 0


# ==========================================================
# REGRESSION
# ==========================================================

def test_regression_power_bounds():
    result = RegressionPowerAnalysis.compute_power(
        effect_size=0.15,
        predictors=3,
        sample_size=100,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_regression_sample_size_positive():
    result = RegressionPowerAnalysis.compute_sample_size(
        effect_size=0.15,
        predictors=3,
        alpha=0.05,
        power=0.8,
    )

    assert get_sample_size(result) > 0


def test_regression_power_increases_with_sample_size():
    small = RegressionPowerAnalysis.compute_power(
        effect_size=0.15,
        predictors=3,
        sample_size=40,
        alpha=0.05,
    )

    large = RegressionPowerAnalysis.compute_power(
        effect_size=0.15,
        predictors=3,
        sample_size=150,
        alpha=0.05,
    )

    assert get_power(large) > get_power(small)


# ==========================================================
# NONPARAMETRIC
# ==========================================================

def test_nonparametric_power_bounds():
    result = NonParametricPowerAnalysis.compute_power(
        effect_size=0.5,
        sample_size=60,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_nonparametric_sample_size_positive():
    result = NonParametricPowerAnalysis.compute_sample_size(
        effect_size=0.5,
        power=0.8,
        alpha=0.05,
    )

    assert get_sample_size(result) > 0


# ==========================================================
# EQUIVALENCE
# ==========================================================

def test_equivalence_power_bounds():
    result = EquivalencePowerAnalysis.compute_power(
        effect_size=0.2,
        sample_size=100,
        alpha=0.05,
    )

    power = get_power(result)

    assert 0.0 <= power <= 1.0


def test_equivalence_sample_size_positive():
    result = EquivalencePowerAnalysis.compute_sample_size(
        effect_size=0.2,
        power=0.8,
        alpha=0.05,
    )

    assert get_sample_size(result) > 0


# ==========================================================
# SENSITIVITY
# ==========================================================

def test_sensitivity_ttest_positive_effect_size():
    result = SensitivityAnalysis.ttest(
        sample_size=100,
        alpha=0.05,
        power=0.8,
    )

    assert get_effect_size(result) > 0


def test_sensitivity_anova_positive_effect_size():
    result = SensitivityAnalysis.anova(
        sample_size=120,
        groups=3,
        alpha=0.05,
        power=0.8,
    )

    assert get_effect_size(result) > 0


def test_sensitivity_regression_positive_effect_size():
    result = SensitivityAnalysis.regression(
        sample_size=120,
        predictors=3,
        alpha=0.05,
        power=0.8,
    )

    assert get_effect_size(result) > 0


# ==========================================================
# PRECISION
# ==========================================================

def test_precision_margin_of_error_positive():
    result = PrecisionAnalysis.margin_of_error(
        sample_size=100,
        standard_deviation=10,
        confidence=0.95,
    )

    assert get_sample_size(result) > 0


def test_precision_ci_width_is_twice_margin():
    margin = PrecisionAnalysis.margin_of_error(
        sample_size=100,
        standard_deviation=10,
        confidence=0.95,
    )

    width = PrecisionAnalysis.confidence_interval_width(
        sample_size=100,
        standard_deviation=10,
        confidence=0.95,
    )

    assert float(width) == pytest.approx(
        2 * float(margin)
    )


def test_precision_mean_sample_size_positive():
    result = PrecisionAnalysis.mean(
        standard_deviation=10,
        margin_error=2,
        confidence=0.95,
    )

    assert get_sample_size(result) > 0


def test_precision_proportion_sample_size_positive():
    result = PrecisionAnalysis.proportion(
        proportion=0.5,
        margin_error=0.05,
        confidence=0.95,
    )

    assert get_sample_size(result) > 0


# ==========================================================
# PACKAGE CONTRACT
# ==========================================================

def test_empty_proportion_module_not_public():
    import emidaf_core.statistics.power_analysis as p

    assert "ProportionPower" not in p.__all__


def test_placeholder_power_analysis_not_public():
    import emidaf_core.statistics.power_analysis as p

    assert "PowerAnalysis" not in p.__all__


def test_all_public_symbols_exist():
    import emidaf_core.statistics.power_analysis as p

    for name in p.__all__:
        assert hasattr(
            p,
            name,
        )
