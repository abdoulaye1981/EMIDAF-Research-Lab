import emidaf_core.statistics.distributions as distributions


EXPECTED_PUBLIC_API = {
    "DistributionResult",
    "BaseDistribution",
    "Continuous",
    "Discrete",
    "Multivariate",
    "Truncated",
    "Mixture",
    "Fitting",
    "GOF",
    "RandomSampling",
    "DistributionAnalysis",
    "Interpretation",
    "Report",
}


def test_public_api_exact_contract():
    assert set(distributions.__all__) == EXPECTED_PUBLIC_API


def test_public_api_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(distributions, name)


def test_obsolete_sampling_name_not_public():
    assert "Sampling" not in distributions.__all__


def test_random_sampling_is_public():
    assert "RandomSampling" in distributions.__all__
