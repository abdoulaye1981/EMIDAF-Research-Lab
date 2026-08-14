"""
=========================================================
EMIDAF Framework
Sensitivity Analysis
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import (

    TTestPower,

    TTestIndPower,

    FTestAnovaPower,

    GofChisquarePower,

    FTestPower

)

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# SENSITIVITY ANALYSIS
# ==========================================================

class SensitivityAnalysis(

    BasePowerAnalysis

):

    """
    Minimum detectable
    effect size analysis.
    """

    name="Sensitivity"

    # ==========================================================
# T TEST
# ==========================================================

    @staticmethod

    def ttest(

        sample_size,

        alpha=0.05,

        power=0.80,

    ):

        analysis=TTestPower()

        effect=analysis.solve_power(

            effect_size=None,

            nobs=sample_size,

            alpha=alpha,

            power=power

        )

        return PowerResult(

            test="Sensitivity t-test",

            effect_size=float(effect),

            alpha=alpha,

            power=power,

            sample_size=sample_size

        )

    # ==========================================================
# INDEPENDENT T TEST
# ==========================================================

    @staticmethod

    def independent_ttest(

        sample_size,

        alpha=0.05,

        power=0.80,

        ratio=1.0,

    ):

        analysis=TTestIndPower()

        effect=analysis.solve_power(

            effect_size=None,

            nobs1=sample_size,

            alpha=alpha,

            power=power,

            ratio=ratio

        )

        return PowerResult(

            test="Sensitivity Independent t-test",

            effect_size=float(effect),

            alpha=alpha,

            power=power,

            sample_size=sample_size,

            metadata={

                "ratio":ratio

            }

        )

    # ==========================================================
# ANOVA
# ==========================================================

    @staticmethod

    def anova(

        sample_size,

        groups,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestAnovaPower()

        effect=analysis.solve_power(

            effect_size=None,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            k_groups=groups

        )

        return PowerResult(

            test="Sensitivity ANOVA",

            effect_size=float(effect),

            alpha=alpha,

            power=power,

            sample_size=sample_size,

            metadata={

                "groups":groups

            }

        )
    
    # ==========================================================
# REGRESSION
# ==========================================================

    @staticmethod

    def regression(

        sample_size,

        predictors,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestPower()

        effect=analysis.solve_power(

            effect_size=None,

            df_num=predictors,

            df_denom=sample_size,

            alpha=alpha,

            power=power

        )

        return PowerResult(

            test="Sensitivity Regression",

            effect_size=float(effect),

            alpha=alpha,

            power=power,

            sample_size=sample_size,

            metadata={

                "predictors":predictors

            }

        )
    # ==========================================================
# CHI SQUARE
# ==========================================================

    @staticmethod

    def chi_square(

        sample_size,

        categories,

        alpha=0.05,

        power=0.80,

    ):

        analysis=GofChisquarePower()

        effect=analysis.solve_power(

            effect_size=None,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            n_bins=categories

        )

        return PowerResult(

            test="Sensitivity Chi-Square",

            effect_size=float(effect),

            alpha=alpha,

            power=power,

            sample_size=sample_size,

            metadata={

                "categories":categories

            }

        )

    # ==========================================================
# SOLVER
# ==========================================================

    @staticmethod

    def solve(

        method,

        **kwargs,

    ):

        methods={

            "ttest":

                SensitivityAnalysis.ttest,

            "independent_ttest":

                SensitivityAnalysis.independent_ttest,

            "anova":

                SensitivityAnalysis.anova,

            "regression":

                SensitivityAnalysis.regression,

            "chi_square":

                SensitivityAnalysis.chi_square

        }

        return methods[

            method

        ](

            **kwargs

        )

# ==========================================================
# SERVICE
# ==========================================================

class Sensitivity:

    ttest=SensitivityAnalysis.ttest

    independent_ttest=SensitivityAnalysis.independent_ttest

    anova=SensitivityAnalysis.anova

    regression=SensitivityAnalysis.regression

    chi_square=SensitivityAnalysis.chi_square

    solve=SensitivityAnalysis.solve