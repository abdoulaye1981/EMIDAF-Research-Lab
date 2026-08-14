"""
=========================================================
EMIDAF Framework
Power Analysis for ANOVA
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import (

    FTestAnovaPower

)

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# ANOVA POWER ANALYSIS
# ==========================================================

class AnovaPowerAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for ANOVA models.
    """

    name="ANOVA"

    # ==========================================================
# ONE WAY ANOVA
# ==========================================================

    @staticmethod

    def one_way(

        effect_size,

        groups,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=FTestAnovaPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            k_groups=groups,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="One-Way ANOVA",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "groups":groups

            }

        )

    # ==========================================================
# TWO WAY ANOVA
# ==========================================================

    @staticmethod

    def two_way(

        effect_size,

        factor_a,

        factor_b,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        groups=factor_a*factor_b

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            groups,

            alpha,

            power,

            sample_size

        )

        result.test="Two-Way ANOVA"

        result.metadata.update(

            {

                "factor_a":factor_a,

                "factor_b":factor_b

            }

        )

        return result

    # ==========================================================
# FACTORIAL ANOVA
# ==========================================================

    @staticmethod

    def factorial(

        effect_size,

        groups,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            groups,

            alpha,

            power,

            sample_size

        )

        result.test="Factorial ANOVA"

        return result

    # ==========================================================
# REPEATED MEASURES
# ==========================================================

    @staticmethod

    def repeated_measures(

        effect_size,

        measurements,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            measurements,

            alpha,

            power,

            sample_size

        )

        result.test="Repeated Measures ANOVA"

        result.metadata.update(

            {

                "measurements":measurements

            }

        )

        return result

    # ==========================================================
# MIXED ANOVA
# ==========================================================

    @staticmethod

    def mixed(

        effect_size,

        between_groups,

        within_measurements,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        groups=between_groups*within_measurements

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            groups,

            alpha,

            power,

            sample_size

        )

        result.test="Mixed ANOVA"

        result.metadata.update(

            {

                "between_groups":between_groups,

                "within_measurements":within_measurements

            }

        )

        return result

    # ==========================================================
# MANOVA
# ==========================================================

    @staticmethod

    def manova(

        effect_size,

        groups,

        dependent_variables,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            groups,

            alpha,

            power,

            sample_size

        )

        result.test="MANOVA"

        result.metadata.update(

            {

                "dependent_variables":dependent_variables

            }

        )

        return result

    # ==========================================================
# ANCOVA
# ==========================================================

    @staticmethod

    def ancova(

        effect_size,

        groups,

        covariates,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=AnovaPowerAnalysis.one_way(

            effect_size,

            groups,

            alpha,

            power,

            sample_size

        )

        result.test="ANCOVA"

        result.metadata.update(

            {

                "covariates":covariates

            }

        )

        return result
    
    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def compute_sample_size(

        effect_size,

        groups,

        power=0.80,

        alpha=0.05,

    ):

        analysis=FTestAnovaPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            k_groups=groups,

            alpha=alpha,

            power=power

        )

        return int(round(n))

    # ==========================================================
# POWER
# ==========================================================

    @staticmethod

    def compute_power(

        effect_size,

        groups,

        sample_size,

        alpha=0.05,

    ):

        analysis=FTestAnovaPower()

        power=analysis.solve_power(

            effect_size=effect_size,

            k_groups=groups,

            alpha=alpha,

            nobs=sample_size

        )

        return float(power)

    # ==========================================================
# SOLVER
# ==========================================================

    @staticmethod

    def solve(

        effect_size,

        groups,

        alpha=0.05,

        power=0.80,

        sample_size=None,

    ):

        analysis=FTestAnovaPower()

        return analysis.solve_power(

            effect_size=effect_size,

            k_groups=groups,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

# ==========================================================
# SERVICE
# ==========================================================

class AnovaPower:

    one_way=AnovaPowerAnalysis.one_way

    two_way=AnovaPowerAnalysis.two_way

    factorial=AnovaPowerAnalysis.factorial

    repeated_measures=AnovaPowerAnalysis.repeated_measures

    mixed=AnovaPowerAnalysis.mixed

    manova=AnovaPowerAnalysis.manova

    ancova=AnovaPowerAnalysis.ancova

    solve=AnovaPowerAnalysis.solve

    compute_power=AnovaPowerAnalysis.compute_power

    compute_sample_size=AnovaPowerAnalysis.compute_sample_size