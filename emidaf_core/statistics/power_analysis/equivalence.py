"""
=========================================================
EMIDAF Framework
Power Analysis for Equivalence Tests
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
# EQUIVALENCE POWER ANALYSIS
# ==========================================================

class EquivalencePowerAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for
    equivalence testing.
    """

    name="Equivalence"

    # ==========================================================
# TOST
# ==========================================================

    @staticmethod

    def tost(

        effect_size,

        margin,

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

            test="TOST",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "margin":margin

            }

        )

    # ==========================================================
# EQUIVALENCE
# ==========================================================

    @staticmethod

    def equivalence(

        effect_size,

        margin,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=(

            EquivalencePowerAnalysis

            .tost(

                effect_size,

                margin,

                alpha,

                power,

                sample_size

            )

        )

        result.test="Equivalence Test"

        return result


    # ==========================================================
# NON INFERIORITY
# ==========================================================

    @staticmethod

    def non_inferiority(

        effect_size,

        margin,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=(

            EquivalencePowerAnalysis

            .tost(

                effect_size,

                margin,

                alpha,

                power,

                sample_size

            )

        )

        result.test="Non Inferiority Test"

        return result

    # ==========================================================
# SUPERIORITY
# ==========================================================

    @staticmethod

    def superiority(

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

            test="Superiority Test",

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

class EquivalencePower:

    tost=EquivalencePowerAnalysis.tost

    equivalence=EquivalencePowerAnalysis.equivalence

    non_inferiority=EquivalencePowerAnalysis.non_inferiority

    superiority=EquivalencePowerAnalysis.superiority

    solve=EquivalencePowerAnalysis.solve

    compute_sample_size=EquivalencePowerAnalysis.compute_sample_size

    compute_power=EquivalencePowerAnalysis.compute_power