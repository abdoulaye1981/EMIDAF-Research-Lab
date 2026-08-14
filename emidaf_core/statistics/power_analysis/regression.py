"""
=========================================================
EMIDAF Framework
Power Analysis for Regression
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import FTestPower

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# REGRESSION POWER ANALYSIS
# ==========================================================

class RegressionPowerAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for regression.
    """

    name="Regression"


    # ==========================================================
# SIMPLE REGRESSION
# ==========================================================

    @staticmethod

    def simple(

        effect_size,

        predictors=1,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

        return PowerResult(

            test="Simple Regression",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "predictors":predictors

            }

        )

    # ==========================================================
# MULTIPLE REGRESSION
# ==========================================================

    @staticmethod

    def multiple(

        effect_size,

        predictors,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

        return PowerResult(

            test="Multiple Regression",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "predictors":predictors

            }

        )

    # ==========================================================
# HIERARCHICAL REGRESSION
# ==========================================================

    @staticmethod

    def hierarchical(

        effect_size,

        tested_predictors,

        total_predictors,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=tested_predictors,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

        return PowerResult(

            test="Hierarchical Regression",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "tested_predictors":tested_predictors,

                "total_predictors":total_predictors

            }

        )

    # ==========================================================
# POWER
# ==========================================================

    @staticmethod

    def compute_power(

        effect_size,

        predictors,

        sample_size,

        alpha=0.05,

    ):

        analysis=FTestPower()

        power=analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            alpha=alpha,

            df_denom=sample_size

        )

        return float(power)

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def compute_sample_size(

        effect_size,

        predictors,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            alpha=alpha,

            power=power

        )

        return int(round(n))

    # ==========================================================
# EFFECT SIZE
# ==========================================================

    @staticmethod

    def compute_effect_size(

        predictors,

        sample_size,

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

        return float(effect)

    # ==========================================================
# ALPHA
# ==========================================================

    @staticmethod

    def compute_alpha(

        effect_size,

        predictors,

        sample_size,

        power=0.80,

    ):

        analysis=FTestPower()

        alpha=analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            df_denom=sample_size,

            alpha=None,

            power=power

        )

        return float(alpha)

    # ==========================================================
# SOLVE
# ==========================================================

    @staticmethod

    def solve(

        effect_size=None,

        predictors=1,

        alpha=0.05,

        power=0.80,

        sample_size=None,

    ):

        analysis=FTestPower()

        return analysis.solve_power(

            effect_size=effect_size,

            df_num=predictors,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

# ==========================================================
# SERVICE
# ==========================================================

class RegressionPower:

    simple=RegressionPowerAnalysis.simple

    multiple=RegressionPowerAnalysis.multiple

    hierarchical=RegressionPowerAnalysis.hierarchical

    solve=RegressionPowerAnalysis.solve

    compute_power=RegressionPowerAnalysis.compute_power

    compute_sample_size=RegressionPowerAnalysis.compute_sample_size

    compute_effect_size=RegressionPowerAnalysis.compute_effect_size

    compute_alpha=RegressionPowerAnalysis.compute_alpha