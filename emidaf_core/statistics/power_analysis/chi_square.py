"""
=========================================================
EMIDAF Framework
Power Analysis for Chi-Square Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from statsmodels.stats.power import GofChisquarePower

from .base import (

    BasePowerAnalysis,

    PowerResult

)

# ==========================================================
# CHI-SQUARE POWER ANALYSIS
# ==========================================================

class ChiSquarePowerAnalysis(

    BasePowerAnalysis

):

    """
    Power analysis for Chi-Square tests.
    """

    name="Chi-Square"

    # ==========================================================
# GOODNESS OF FIT
# ==========================================================

    @staticmethod

    def goodness_of_fit(

        effect_size,

        categories,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        analysis=GofChisquarePower()

        n=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            n_bins=categories

        )

        return PowerResult(

            test="Chi-Square Goodness of Fit",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "categories":categories

            }

        )

    # ==========================================================
# INDEPENDENCE TEST
# ==========================================================

    @staticmethod

    def independence(

        effect_size,

        rows,

        columns,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        bins=rows*columns

        analysis=GofChisquarePower()

        n=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            n_bins=bins

        )

        return PowerResult(

            test="Chi-Square Independence",

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            sample_size=float(n),

            metadata={

                "rows":rows,

                "columns":columns

            }

        )

    # ==========================================================
# CONTINGENCY TABLE
# ==========================================================

    @staticmethod

    def contingency(

        effect_size,

        rows,

        columns,

        alpha=0.05,

        power=None,

        sample_size=None,

    ):

        result=(

            ChiSquarePowerAnalysis

            .independence(

                effect_size,

                rows,

                columns,

                alpha,

                power,

                sample_size

            )

        )

        result.test="Contingency Table"

        return result

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def compute_sample_size(

        effect_size,

        categories,

        alpha=0.05,

        power=0.80,

    ):

        analysis=GofChisquarePower()

        n=analysis.solve_power(

            effect_size=effect_size,

            alpha=alpha,

            power=power,

            n_bins=categories

        )

        return int(round(n))

    # ==========================================================
# POWER
# ==========================================================

    @staticmethod

    def compute_power(

        effect_size,

        sample_size,

        categories,

        alpha=0.05,

    ):

        analysis=GofChisquarePower()

        power=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            n_bins=categories

        )

        return float(power)

    # ==========================================================
# COHEN W
# ==========================================================

    @staticmethod

    def compute_effect_size(

        observed,

        expected,

    ):

        import numpy as np

        observed=np.asarray(observed)

        expected=np.asarray(expected)

        w=np.sqrt(

            np.sum(

                (

                    observed-

                    expected

                )**2

                /expected

            )

            /

            np.sum(expected)

        )

        return float(w)

    # ==========================================================
# ALPHA
# ==========================================================

    @staticmethod

    def compute_alpha(

        effect_size,

        sample_size,

        categories,

        power=0.80,

    ):

        analysis=GofChisquarePower()

        alpha=analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=None,

            power=power,

            n_bins=categories

        )

        return float(alpha)

    # ==========================================================
# SOLVE
# ==========================================================

    @staticmethod

    def solve(

        effect_size=None,

        sample_size=None,

        categories=2,

        alpha=0.05,

        power=0.80,

    ):

        analysis=GofChisquarePower()

        return analysis.solve_power(

            effect_size=effect_size,

            nobs=sample_size,

            alpha=alpha,

            power=power,

            n_bins=categories

        )

# ==========================================================
# SERVICE
# ==========================================================

class ChiSquarePower:

    goodness_of_fit=ChiSquarePowerAnalysis.goodness_of_fit

    independence=ChiSquarePowerAnalysis.independence

    contingency=ChiSquarePowerAnalysis.contingency

    solve=ChiSquarePowerAnalysis.solve

    compute_sample_size=ChiSquarePowerAnalysis.compute_sample_size

    compute_power=ChiSquarePowerAnalysis.compute_power

    compute_effect_size=ChiSquarePowerAnalysis.compute_effect_size

    compute_alpha=ChiSquarePowerAnalysis.compute_alpha