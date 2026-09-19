import emidaf_core.statistics.correlations as correlations


EXPECTED_PUBLIC_API = {
    "Pearson",
    "Spearman",
    "Kendall",
    "PointBiserial",
    "Biserial",
    "CorrelationRatio",
    "ChiSquare",
    "PhiCoefficient",
    "CramerV",
    "ContingencyCoefficient",
    "MutualInformation",
    "DistanceCorrelation",
    "ConcordanceCorrelation",
    "LinearCorrelationMatrix",
    "CorrelationInterpretation",
    "VarianceInflationFactor",
    "MulticollinearityAnalyzer",
}


def test_public_api_exact_contract():
    assert set(
        correlations.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            correlations,
            name,
        )


def test_obsolete_names_not_public():
    assert (
        "EtaSquared"
        not in correlations.__all__
    )

    assert (
        "CorrelationMatrix"
        not in correlations.__all__
    )


def test_linear_correlation_matrix_is_public():
    assert (
        "LinearCorrelationMatrix"
        in correlations.__all__
    )
