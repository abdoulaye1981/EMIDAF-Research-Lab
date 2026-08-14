"""
=========================================================
EMIDAF Framework
Power Analysis for Correlation
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
# CORRELATION POWER ANALYSIS
# ==========================================================

class CorrelationPowerAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for correlations.
    """

    name="Correlation"


    # ==========================================================
# PEARSON
# ==========================================================

    @staticmethod

    def pearson(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=1,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

        return PowerResult(

            test="Pearson Correlation",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n)

        )

    # ==========================================================
# SPEARMAN
# ==========================================================

    @staticmethod

    def spearman(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=CorrelationPowerAnalysis.pearson(

            effect_size,

            alpha,

            power,

            sample_size

        )

        result.test="Spearman Correlation"

        return result

    # ==========================================================
# KENDALL
# ==========================================================

    @staticmethod

    def kendall(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=CorrelationPowerAnalysis.pearson(

            effect_size,

            alpha,

            power,

            sample_size

        )

        result.test="Kendall Correlation"

        return result

    # ==========================================================
# PARTIAL CORRELATION
# ==========================================================

    @staticmethod

    def partial(

        effect_size,

        control_variables,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=control_variables+1,

            alpha=alpha,

            power=power,

            df_denom=sample_size

        )

        return PowerResult(

            test="Partial Correlation",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "control_variables":

                    control_variables

            }

        )

    # ==========================================================
# SEMI PARTIAL
# ==========================================================

    @staticmethod

    def semi_partial(

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

            test="Semi Partial Correlation",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "predictors":

                    predictors

            }

        )

    # ==========================================================
# POWER
# ==========================================================

    @staticmethod

    def compute_power(

        effect_size,

        sample_size,

        alpha=0.05,

    ):

        analysis=FTestPower()

        power=analysis.solve_power(

            effect_size=effect_size,

            df_num=1,

            df_denom=sample_size,

            alpha=alpha

        )

        return float(power)

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def compute_sample_size(

        effect_size,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            df_num=1,

            alpha=alpha,

            power=power

        )

        return int(round(n))

    # ==========================================================
# EFFECT SIZE
# ==========================================================

    @staticmethod

    def compute_effect_size(

        sample_size,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestPower()

        effect=analysis.solve_power(

            effect_size=None,

            df_num=1,

            df_denom=sample_size,

            alpha=alpha,

            power=power

        )

        return float(effect)

    # ==========================================================
# SOLVE
# ==========================================================

    @staticmethod

    def solve(

        effect_size=None,

        sample_size=None,

        alpha=0.05,

        power=0.80,

    ):

        analysis=FTestPower()

        return analysis.solve_power(

            effect_size=effect_size,

            df_num=1,

            df_denom=sample_size,

            alpha=alpha,

            power=power

        )
    
# ==========================================================
# SERVICE
# ==========================================================

class CorrelationPower:

    pearson=CorrelationPowerAnalysis.pearson

    spearman=CorrelationPowerAnalysis.spearman

    kendall=CorrelationPowerAnalysis.kendall

    partial=CorrelationPowerAnalysis.partial

    semi_partial=CorrelationPowerAnalysis.semi_partial

    solve=CorrelationPowerAnalysis.solve

    compute_power=CorrelationPowerAnalysis.compute_power

    compute_sample_size=CorrelationPowerAnalysis.compute_sample_size

    compute_effect_size=CorrelationPowerAnalysis.compute_effect_size