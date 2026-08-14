"""
=========================================================
EMIDAF Framework
Hypothesis Testing
=========================================================
"""

from .base import BaseHypothesisTest
from .result import HypothesisResult

from .normality import (
    ShapiroTest,
    NormalityTest,
    AndersonTest,
    shapiro_test,
    normality_test,
    anderson_test
)

from .variance import (
    LeveneTest,
    BartlettTest,
    levene_test,
    bartlett_test
)

from .mean import (
    OneSampleTTest,
    IndependentTTest,
    PairedTTest,
    one_sample_t_test,
    independent_t_test,
    welch_t_test,
    paired_t_test
)

from .proportion import (
    OneSampleProportionTest,
    TwoSampleProportionTest,
    one_sample_proportion_test,
    two_sample_proportion_test
)

from .independence import (
    ChiSquareIndependenceTest,
    ChiSquareGoodnessOfFitTest,
    chi_square_independence_test,
    chi_square_goodness_of_fit_test,
    cramers_v
)

from .nonparametric import (
    MannWhitneyTest,
    WilcoxonTest,
    KruskalWallisTest,
    FriedmanTest,
    SpearmanTest,
    mann_whitney_test,
    wilcoxon_test,
    kruskal_wallis_test,
    friedman_test,
    spearman_test
)

from .multiple import (
    MultipleTesting,
    adjust_pvalues,
    bonferroni_correction,
    holm_correction,
    fdr_bh_correction,
    fdr_by_correction,
    sidak_correction,
    compare_methods
)

__all__ = [

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
    "compare_methods"
]
