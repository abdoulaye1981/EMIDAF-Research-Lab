"""
=========================================================
EMIDAF Framework
Power Analysis for t-tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import (

    TTestPower,

    TTestIndPower

)

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# T TEST POWER ANALYSIS
# ==========================================================

class TTestAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for all t-tests.
    """

    name="T-Test"

    # ==========================================================
# ONE SAMPLE
# ==========================================================

    @staticmethod
    def one_sample(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size,

            alternative=alternative

        )

        return PowerResult(

            test="One Sample t-test",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            alternative=alternative

        )
    # ==========================================================
# PAIRED T TEST
# ==========================================================

    @staticmethod
    def paired(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs=sample_size,

            alternative=alternative

        )

        return PowerResult(

            test="Paired t-test",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            alternative=alternative

        )

    # ==========================================================
# INDEPENDENT T TEST
# ==========================================================

    @staticmethod
    def independent(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

        ratio=1.0,

        alternative="two-sided",

    ):

        analysis=TTestIndPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            nobs1=sample_size,

            ratio=ratio,

            alternative=alternative

        )

        return PowerResult(

            test="Independent t-test",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            alternative=alternative,

            metadata={

                "ratio":ratio

            }

        )
    # ==========================================================
# WELCH T TEST
# ==========================================================

    @staticmethod
    def welch(

        effect_size,

        alpha=0.05,

        power=None,

        sample_size=None,

        ratio=1.0,

        alternative="two-sided",

    ):

        result=TTestAnalysis.independent(

            effect_size,

            alpha,

            power,

            sample_size,

            ratio,

            alternative

        )

        result.test="Welch t-test"

        return result

    # ==========================================================
# COMPUTE POWER
# ==========================================================

    @staticmethod
    def compute_power(

        effect_size,

        sample_size,

        alpha=0.05,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        power=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            power=None,

            alternative=alternative

        )

        return float(power)

    # ==========================================================
# COMPUTE SAMPLE SIZE
# ==========================================================

    @staticmethod
    def compute_sample_size(

        effect_size,

        power=0.80,

        alpha=0.05,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            alternative=alternative

        )

        return int(round(n))

    # ==========================================================
# COMPUTE EFFECT SIZE
# ==========================================================

    @staticmethod
    def compute_effect_size(

        sample_size,

        power=0.80,

        alpha=0.05,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        d=analysis.solve_power(

            effect_size=None,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            alternative=alternative

        )

        return float(d)

    # ==========================================================
# COMPUTE ALPHA
# ==========================================================

    @staticmethod
    def compute_alpha(

        effect_size,

        sample_size,

        power=0.80,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        alpha=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=None,

            power=power,

            alternative=alternative

        )

        return float(alpha)

    # ==========================================================
# SOLVER
# ==========================================================

    @staticmethod
    def solve(

        effect_size=None,

        sample_size=None,

        alpha=0.05,

        power=0.80,

        alternative="two-sided",

    ):

        analysis=TTestPower()

        return analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            alternative=alternative

        )

# ==========================================================
# SERVICE
# ==========================================================

class TTest:

    one_sample=TTestAnalysis.one_sample

    paired=TTestAnalysis.paired

    independent=TTestAnalysis.independent

    welch=TTestAnalysis.welch

    solve=TTestAnalysis.solve

    compute_power=TTestAnalysis.compute_power

    compute_sample_size=TTestAnalysis.compute_sample_size

    compute_effect_size=TTestAnalysis.compute_effect_size

    compute_alpha=TTestAnalysis.compute_alpha