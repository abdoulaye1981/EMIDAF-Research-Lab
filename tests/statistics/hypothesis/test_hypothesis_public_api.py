import emidaf_core.statistics.hypothesis as hypothesis


EXPECTED_PUBLIC_API = {
    "MoodMedianTest",
    "SignTest",
    "mood_median_test",
    "sign_test",
    "BaseHypothesisTest",
    "HypothesisResult",
    "ShapiroTest",
    "NormalityTest",
    "AndersonTest",
    "shapiro_test",
    "normality_test",
    "anderson_test",
    "LeveneTest",
    "BartlettTest",
    "levene_test",
    "bartlett_test",
    "OneSampleTTest",
    "IndependentTTest",
    "PairedTTest",
    "one_sample_t_test",
    "independent_t_test",
    "welch_t_test",
    "paired_t_test",
    "OneSampleProportionTest",
    "TwoSampleProportionTest",
    "one_sample_proportion_test",
    "two_sample_proportion_test",
    "ChiSquareIndependenceTest",
    "ChiSquareGoodnessOfFitTest",
    "chi_square_independence_test",
    "chi_square_goodness_of_fit_test",
    "cramers_v",
    "MannWhitneyTest",
    "WilcoxonTest",
    "KruskalWallisTest",
    "FriedmanTest",
    "SpearmanTest",
    "mann_whitney_test",
    "wilcoxon_test",
    "kruskal_wallis_test",
    "friedman_test",
    "spearman_test",
    "MultipleTesting",
    "adjust_pvalues",
    "bonferroni_correction",
    "holm_correction",
    "fdr_bh_correction",
    "fdr_by_correction",
    "sidak_correction",
    "compare_methods",
}


def test_public_api_exact_contract():
    assert set(
        hypothesis.__all__
    ) == EXPECTED_PUBLIC_API


def test_all_public_symbols_exist():
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(
            hypothesis,
            name,
        )


def test_parametric_duplicate_classes_not_public():
    assert "StudentTTest" not in hypothesis.__all__
    assert "WelchTTest" not in hypothesis.__all__
    assert "OneWayANOVA" not in hypothesis.__all__
    assert "FTest" not in hypothesis.__all__


def test_canonical_t_test_classes_are_public():
    assert "OneSampleTTest" in hypothesis.__all__
    assert "IndependentTTest" in hypothesis.__all__
    assert "PairedTTest" in hypothesis.__all__
