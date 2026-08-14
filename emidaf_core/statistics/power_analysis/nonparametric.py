"""
=========================================================
EMIDAF Framework
Power Analysis for Nonparametric Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import TTestPower

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# NONPARAMETRIC POWER ANALYSIS
# ==========================================================

class NonParametricPowerAnalysis(

    BasePowerAnalysis

):

    """
    Power approximation for
    nonparametric tests.
    """

    name="Nonparametric"

    # ==========================================================
# MANN WHITNEY
# ==========================================================

    @staticmethod

    def mann_whitney(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Mann-Whitney U",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n)

        )

    # ==========================================================
# WILCOXON
# ==========================================================

    @staticmethod

    def wilcoxon(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Wilcoxon Signed Rank",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n)

        )

    # ==========================================================
# KRUSKAL WALLIS
# ==========================================================

    @staticmethod

    def kruskal(

        effect_size,

        groups,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Kruskal-Wallis",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "groups":groups

            }

        )

    # ==========================================================
# FRIEDMAN
# ==========================================================

    @staticmethod

    def friedman(

        effect_size,

        measurements,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Friedman",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "measurements":measurements

            }

        )

    # ==========================================================
# SIGN TEST
# ==========================================================

    @staticmethod

    def sign_test(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Sign Test",

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

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Spearman",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n)

        )

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

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size

        )

        return PowerResult(

            test="Kendall",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n)

        )

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def compute_sample_size(

        effect_size,

        power=0.80,

        alpha=0.05,

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

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

        sample_size,

        alpha=0.05,

    ):

        analysis=TTestPower()

        power=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            nobs=sample_size

        )

        return float(power)

    # ==========================================================
# SOLVER
# ==========================================================

    @staticmethod

    def solve(

        effect_size=None,

        sample_size=None,

        alpha=0.05,

        power=0.80,

    ):

        analysis=TTestPower()

        return analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            nobs=sample_size,

            power=power

        )

# ==========================================================
# SERVICE
# ==========================================================

class NonParametricPower:

    mann_whitney=NonParametricPowerAnalysis.mann_whitney

    wilcoxon=NonParametricPowerAnalysis.wilcoxon

    kruskal=NonParametricPowerAnalysis.kruskal

    friedman=NonParametricPowerAnalysis.friedman

    sign_test=NonParametricPowerAnalysis.sign_test

    spearman=NonParametricPowerAnalysis.spearman

    kendall=NonParametricPowerAnalysis.kendall

    solve=NonParametricPowerAnalysis.solve

    compute_sample_size=NonParametricPowerAnalysis.compute_sample_size

    compute_power=NonParametricPowerAnalysis.compute_power