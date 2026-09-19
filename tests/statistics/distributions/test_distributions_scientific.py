import numpy as np
import pytest

from scipy import stats

from emidaf_core.statistics.distributions.discrete import (
    BernoulliDistribution,
    BinomialDistribution,
    PoissonDistribution,
    GeometricDistribution,
)

from emidaf_core.statistics.distributions.continuous import (
    NormalDistribution,
    ExponentialDistribution,
    GammaDistribution,
    UniformDistribution,
    StudentDistribution,
    ChiSquareDistribution,
)

from emidaf_core.statistics.distributions.multivariate import (
    MultivariateNormalDistribution,
)


# ==========================================================
# DISCRETE DISTRIBUTIONS — PARAMETER ESTIMATION
# ==========================================================

def test_bernoulli_parameter_estimation():
    data = np.array([0, 1, 1, 0, 1])

    model = BernoulliDistribution()

    params = model.estimate(data)

    assert len(params) == 1
    assert params[0] == pytest.approx(0.6)


def test_binomial_parameter_estimation():
    data = np.array([2, 4, 3, 5, 1])

    model = BinomialDistribution()

    n, p = model.estimate(data)

    assert n == 5
    assert p == pytest.approx(
        np.mean(data) / 5
    )


def test_poisson_parameter_estimation():
    data = np.array([1, 2, 3, 4, 5])

    model = PoissonDistribution()

    params = model.estimate(data)

    assert len(params) == 1
    assert params[0] == pytest.approx(3.0)


def test_geometric_parameter_estimation():
    data = np.array([1, 2, 3, 4])

    model = GeometricDistribution()

    params = model.estimate(data)

    assert len(params) == 1
    assert params[0] == pytest.approx(
        1 / 2.5
    )


# ==========================================================
# DISCRETE DISTRIBUTIONS — PMF/CDF
#
# EMIDAF utilise actuellement le nom pdf()
# pour la PMF des distributions discrètes.
# ==========================================================

def test_bernoulli_pmf():
    model = BernoulliDistribution()
    model.parameters = (0.3,)

    assert model.pdf(1) == pytest.approx(0.3)
    assert model.pdf(0) == pytest.approx(0.7)


def test_binomial_pmf():
    model = BinomialDistribution()
    model.parameters = (10, 0.5)

    result = model.pdf(5)

    expected = stats.binom.pmf(
        5,
        10,
        0.5,
    )

    assert result == pytest.approx(
        expected
    )


def test_poisson_pmf():
    model = PoissonDistribution()
    model.parameters = (3.0,)

    result = model.pdf(2)

    expected = stats.poisson.pmf(
        2,
        3.0,
    )

    assert result == pytest.approx(
        expected
    )


def test_geometric_pmf():
    model = GeometricDistribution()
    model.parameters = (0.25,)

    result = model.pdf(3)

    expected = stats.geom.pmf(
        3,
        0.25,
    )

    assert result == pytest.approx(
        expected
    )


def test_poisson_cdf():
    model = PoissonDistribution()
    model.parameters = (4.0,)

    result = model.cdf(3)

    expected = stats.poisson.cdf(
        3,
        4.0,
    )

    assert result == pytest.approx(
        expected
    )


# ==========================================================
# NORMAL DISTRIBUTION
# ==========================================================

def test_normal_pdf_standard():
    model = NormalDistribution()
    model.parameters = (
        0.0,
        1.0,
    )

    result = model.pdf(0.0)

    expected = (
        1 / np.sqrt(2 * np.pi)
    )

    assert result == pytest.approx(
        expected
    )


def test_normal_cdf_zero():
    model = NormalDistribution()
    model.parameters = (
        0.0,
        1.0,
    )

    assert model.cdf(0.0) == pytest.approx(
        0.5
    )


def test_normal_ppf_median():
    model = NormalDistribution()
    model.parameters = (
        0.0,
        1.0,
    )

    assert model.ppf(0.5) == pytest.approx(
        0.0,
        abs=1e-12,
    )


# ==========================================================
# EXPONENTIAL DISTRIBUTION
# SciPy parameters: loc, scale
# ==========================================================

def test_exponential_pdf():
    model = ExponentialDistribution()

    model.parameters = (
        0.0,
        2.0,
    )

    result = model.pdf(0.0)

    expected = 1 / 2

    assert result == pytest.approx(
        expected
    )


def test_exponential_cdf():
    model = ExponentialDistribution()

    model.parameters = (
        0.0,
        2.0,
    )

    result = model.cdf(2.0)

    expected = (
        1 - np.exp(-1)
    )

    assert result == pytest.approx(
        expected
    )


# ==========================================================
# GAMMA DISTRIBUTION
# SciPy: shape, loc, scale
# ==========================================================

def test_gamma_pdf_matches_scipy():
    model = GammaDistribution()

    model.parameters = (
        2.0,
        0.0,
        3.0,
    )

    result = model.pdf(4.0)

    expected = stats.gamma.pdf(
        4.0,
        2.0,
        loc=0.0,
        scale=3.0,
    )

    assert result == pytest.approx(
        expected
    )


# ==========================================================
# UNIFORM DISTRIBUTION
# ==========================================================

def test_uniform_pdf():
    model = UniformDistribution()

    model.parameters = (
        2.0,
        4.0,
    )

    # Uniforme sur [2, 6]
    assert model.pdf(3.0) == pytest.approx(
        0.25
    )


def test_uniform_cdf():
    model = UniformDistribution()

    model.parameters = (
        2.0,
        4.0,
    )

    assert model.cdf(4.0) == pytest.approx(
        0.5
    )


# ==========================================================
# STUDENT DISTRIBUTION
# ==========================================================

def test_student_distribution_symmetry():
    model = StudentDistribution()

    model.parameters = (
        10.0,
        0.0,
        1.0,
    )

    assert model.cdf(0.0) == pytest.approx(
        0.5
    )


# ==========================================================
# CHI-SQUARE DISTRIBUTION
# ==========================================================

def test_chi_square_pdf_matches_scipy():
    model = ChiSquareDistribution()

    model.parameters = (
        4.0,
        0.0,
        1.0,
    )

    result = model.pdf(2.0)

    expected = stats.chi2.pdf(
        2.0,
        4.0,
    )

    assert result == pytest.approx(
        expected
    )


# ==========================================================
# RANDOM GENERATION
# ==========================================================

def test_normal_rvs_size():
    model = NormalDistribution()

    model.parameters = (
        0.0,
        1.0,
    )

    sample = model.rvs(
        size=100
    )

    assert len(sample) == 100
    assert np.all(
        np.isfinite(sample)
    )


def test_poisson_rvs_size():
    model = PoissonDistribution()

    model.parameters = (
        3.0,
    )

    sample = model.rvs(
        size=100
    )

    assert len(sample) == 100

    assert np.all(
        np.asarray(sample) >= 0
    )


# ==========================================================
# MULTIVARIATE NORMAL
# ==========================================================

def test_multivariate_normal_pdf_origin():
    model = MultivariateNormalDistribution()

    mean = np.array(
        [0.0, 0.0]
    )

    covariance = np.eye(2)

    model.parameters = (
        mean,
        covariance,
    )

    result = model.pdf(
        np.array(
            [0.0, 0.0]
        )
    )

    expected = (
        1 / (2 * np.pi)
    )

    assert result == pytest.approx(
        expected
    )


def test_multivariate_normal_pdf_matches_scipy():
    model = MultivariateNormalDistribution()

    mean = np.array(
        [1.0, 2.0]
    )

    covariance = np.array(
        [
            [2.0, 0.5],
            [0.5, 1.0],
        ]
    )

    point = np.array(
        [1.5, 2.5]
    )

    model.parameters = (
        mean,
        covariance,
    )

    result = model.pdf(
        point
    )

    expected = stats.multivariate_normal.pdf(
        point,
        mean=mean,
        cov=covariance,
    )

    assert result == pytest.approx(
        expected
    )
