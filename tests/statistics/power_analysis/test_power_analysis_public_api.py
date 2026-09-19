import emidaf_core.statistics.power_analysis as power_analysis


EXPECTED_PUBLIC_API = {
    "PowerResult",
    "BasePowerAnalysis",
    "TTest",
    "AnovaPower",
    "RegressionPower",
    "CorrelationPower",
    "ChiSquarePower",
    "NonParametricPower",
    "EquivalencePower",
    "Sensitivity",
    "Precision",
    "Interpretation",
    "Summary",
    "Report",
}


def test_public_api_exact_contract():
    assert set(
        power_analysis.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            power_analysis,
            name,
        )


def test_placeholder_power_analysis_not_public():
    assert hasattr(
        power_analysis,
        "PowerAnalysis",
    )

    assert (
        "PowerAnalysis"
        not in power_analysis.__all__
    )


def test_unimplemented_proportion_power_not_public():
    assert (
        "ProportionPower"
        not in power_analysis.__all__
    )
