import numpy as np
import pandas as pd
import pytest
from scipy import stats

from emidaf_core.statistics.correlations.linear import (
    Pearson,
    Spearman,
    Kendall,
)

from emidaf_core.statistics.correlations.categorical import (
    ChiSquare,
    PhiCoefficient,
    CramerV,
)

from emidaf_core.statistics.correlations.matrix import (
    PointBiserial,
    Biserial,
    CorrelationRatio,
)

from emidaf_core.statistics.correlations.multicollinearity import (
    VarianceInflationFactor,
)


def coef(result):
    """Extract the coefficient from an EMIDAF correlation result."""
    if hasattr(result, "coefficient"):
        return float(result.coefficient)

    if hasattr(result, "value"):
        return float(result.value)

    if isinstance(result, dict):
        for name in ("coefficient", "value"):
            if name in result:
                return float(result[name])

    raise AssertionError(
        f"Coefficient inaccessible: {result!r}"
    )


# ==========================================================
# PEARSON
# ==========================================================

def test_pearson_perfect_positive():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 4, 6, 8, 10], dtype=float)

    result = Pearson.compute(x, y)

    assert coef(result) == pytest.approx(1.0)


def test_pearson_perfect_negative():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([10, 8, 6, 4, 2], dtype=float)

    result = Pearson.compute(x, y)

    assert coef(result) == pytest.approx(-1.0)


def test_pearson_matches_scipy():
    x = np.array([1, 2, 4, 7, 9, 12], dtype=float)
    y = np.array([3, 1, 5, 8, 7, 15], dtype=float)

    expected = stats.pearsonr(x, y).statistic

    result = Pearson.compute(x, y)

    assert coef(result) == pytest.approx(expected)


# ==========================================================
# SPEARMAN
# ==========================================================

def test_spearman_monotonic_nonlinear():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([1, 4, 9, 16, 25], dtype=float)

    result = Spearman.compute(x, y)

    assert coef(result) == pytest.approx(1.0)


def test_spearman_matches_scipy():
    x = np.array([5, 1, 4, 2, 3], dtype=float)
    y = np.array([10, 3, 8, 4, 6], dtype=float)

    expected = stats.spearmanr(x, y).statistic

    result = Spearman.compute(x, y)

    assert coef(result) == pytest.approx(expected)


# ==========================================================
# KENDALL
# ==========================================================

def test_kendall_perfect_positive():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([10, 20, 30, 40, 50])

    result = Kendall.compute(x, y)

    assert coef(result) == pytest.approx(1.0)


def test_kendall_matches_scipy():
    x = np.array([1, 3, 2, 5, 4])
    y = np.array([2, 4, 1, 5, 3])

    expected = stats.kendalltau(x, y).statistic

    result = Kendall.compute(x, y)

    assert coef(result) == pytest.approx(expected)


# ==========================================================
# POINT-BISERIAL
# ==========================================================

def test_point_biserial_matches_scipy():
    x = np.array([0, 0, 0, 1, 1, 1])

    y = np.array(
        [1, 2, 3, 6, 7, 8],
        dtype=float,
    )

    expected = stats.pointbiserialr(
        x,
        y,
    ).statistic

    result = PointBiserial.compute(
        x,
        y,
    )

    assert coef(result) == pytest.approx(expected)


# ==========================================================
# BISERIAL
# ==========================================================

def test_biserial_is_positive_for_separated_groups():
    x = np.array([0, 0, 0, 1, 1, 1])

    y = np.array(
        [1, 2, 3, 6, 7, 8],
        dtype=float,
    )

    result = Biserial.compute(x, y)

    value = coef(result)

    assert np.isfinite(value)
    assert value > 0


def test_biserial_rejects_non_binary_variable():
    x = np.array([0, 1, 2, 0, 1, 2])

    y = np.array(
        [1, 2, 3, 4, 5, 6],
        dtype=float,
    )

    with pytest.raises(ValueError):
        Biserial.compute(x, y)


def test_biserial_rejects_constant_numeric_variable():
    x = np.array([0, 0, 1, 1])

    y = np.array(
        [5, 5, 5, 5],
        dtype=float,
    )

    with pytest.raises(ValueError):
        Biserial.compute(x, y)


# ==========================================================
# CORRELATION RATIO — ETA
# ==========================================================

def test_eta_perfect_group_separation():
    categories = np.array(
        ["A", "A", "A", "B", "B", "B"]
    )

    values = np.array(
        [1, 1, 1, 5, 5, 5],
        dtype=float,
    )

    result = CorrelationRatio.compute(
        categories,
        values,
    )

    assert coef(result) == pytest.approx(1.0)


def test_eta_zero_when_group_means_equal():
    categories = np.array(
        ["A", "A", "B", "B"]
    )

    values = np.array(
        [1, 3, 1, 3],
        dtype=float,
    )

    result = CorrelationRatio.compute(
        categories,
        values,
    )

    assert coef(result) == pytest.approx(0.0)


# ==========================================================
# PHI
# ==========================================================

def test_phi_perfect_binary_association():
    x = np.array([0, 0, 1, 1])
    y = np.array([0, 0, 1, 1])

    result = PhiCoefficient.compute(
        x,
        y,
    )

    assert abs(coef(result)) == pytest.approx(1.0)


# ==========================================================
# CRAMER V
# ==========================================================

def test_cramer_v_perfect_association():
    x = np.array(
        ["A", "A", "B", "B", "C", "C"]
    )

    y = np.array(
        ["X", "X", "Y", "Y", "Z", "Z"]
    )

    result = CramerV.compute(
        x,
        y,
    )

    assert coef(result) == pytest.approx(1.0)


def test_cramer_v_between_zero_and_one():
    x = np.array(
        ["A", "A", "A", "B", "B", "B", "C", "C"]
    )

    y = np.array(
        ["X", "X", "Y", "X", "Y", "Y", "X", "Y"]
    )

    result = CramerV.compute(
        x,
        y,
    )

    value = coef(result)

    assert 0.0 <= value <= 1.0


# ==========================================================
# CHI-SQUARE
# ==========================================================

def test_chi_square_returns_valid_result():
    x = np.array(
        ["A", "A", "A", "B", "B", "B"]
    )

    y = np.array(
        ["X", "X", "X", "Y", "Y", "Y"]
    )

    result = ChiSquare.compute(
        x,
        y,
    )

    assert result is not None


# ==========================================================
# VIF
# ==========================================================

def test_vif_returns_one_row_per_variable():
    df = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 6],
            "x2": [2, 5, 1, 7, 4, 9],
            "x3": [8, 3, 6, 2, 7, 4],
        }
    )

    result = VarianceInflationFactor.compute(df)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_vif_detects_perfect_multicollinearity():
    df = pd.DataFrame(
        {
            "x1": [1, 2, 3, 4, 5, 6],
            "x2": [2, 4, 6, 8, 10, 12],
            "x3": [3, 1, 8, 4, 9, 7],
        }
    )

    result = VarianceInflationFactor.compute(df)

    numeric = result.select_dtypes(
        include=[np.number]
    ).to_numpy()

    assert (
        np.isinf(numeric).any()
        or (numeric > 1e6).any()
    )
