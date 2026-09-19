import emidaf_core.statistics.inferential as inferential


EXPECTED_PUBLIC_API = {
    "InferentialResult",
    "BaseInferentialTest",
    "OneSample",
    "TwoSamples",
    "Paired",
    "Proportions",
    "VarianceTests",
    "Confidence",
    "Estimator",
    "Equivalence",
    "NonInferiority",
    "Superiority",
    "Bootstrap",
    "Permutation",
    "Bayes",
    "Inferential",
    "Interpretation",
    "Report",
}


def test_public_api_exact_contract():
    assert set(
        inferential.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            inferential,
            name,
        )


def test_incomplete_methods_not_public_services():
    assert (
        "fligner_policello"
        not in inferential.TwoSamples.registry
    )

    assert (
        "obrien"
        not in inferential.VarianceTests.registry
    )

    assert (
        "box_m"
        not in inferential.VarianceTests.registry
    )


def test_paired_permutation_public_service():
    assert (
        "permutation"
        in inferential.Paired.registry
    )
