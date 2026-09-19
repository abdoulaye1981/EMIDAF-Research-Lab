import emidaf_core.statistics.effect_size as effect_size


EXPECTED_PUBLIC_API = {
    "EffectSizeResult",
    "BaseEffectSize",
    "MeanDifference",
    "Correlation",
    "Proportions",
    "Contingency",
    "Regression",
    "Anova",
    "NonParametric",
    "Interpretation",
    "Summary",
    "Report",
}


def test_public_api_exact_contract():
    assert set(
        effect_size.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            effect_size,
            name,
        )


def test_placeholder_effect_size_not_public():
    assert hasattr(
        effect_size,
        "EffectSize",
    )

    assert (
        "EffectSize"
        not in effect_size.__all__
    )


def test_scientific_facades_available():
    facades = (
        effect_size.MeanDifference,
        effect_size.Correlation,
        effect_size.Proportions,
        effect_size.Contingency,
        effect_size.Regression,
        effect_size.Anova,
        effect_size.NonParametric,
    )

    assert all(
        facade is not None
        for facade in facades
    )
