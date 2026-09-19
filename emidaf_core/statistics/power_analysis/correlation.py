"""
=========================================================
EMIDAF Framework
Power Analysis for Correlation
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy.stats import t, nct
from scipy.optimize import brentq

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

    @staticmethod
    def compute_power(
        effect_size,
        sample_size,
        alpha=0.05,
    ):
        """
        Power for testing a Pearson correlation
        using the noncentral t distribution.
        """

        r = float(effect_size)
        n = int(sample_size)

        if not -1 < r < 1:
            raise ValueError(
                "effect_size must be between "
                "-1 and 1."
            )

        if n < 4:
            raise ValueError(
                "sample_size must be at least 4."
            )

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha must be between 0 and 1."
            )

        df = n - 2

        ncp = (
            r
            * np.sqrt(
                df
                /
                (1 - r**2)
            )
        )

        critical = t.ppf(
            1 - alpha / 2,
            df,
        )

        power = (
            nct.cdf(
                -critical,
                df,
                ncp,
            )
            +
            nct.sf(
                critical,
                df,
                ncp,
            )
        )

        return float(power)

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    @staticmethod
    def compute_sample_size(
        effect_size,
        alpha=0.05,
        power=0.80,
    ):
        """
        Minimum integer sample size required
        for the requested correlation power.
        """

        r = float(effect_size)

        if not 0 < abs(r) < 1:
            raise ValueError(
                "abs(effect_size) must be "
                "between 0 and 1."
            )

        if not 0 < power < 1:
            raise ValueError(
                "power must be between 0 and 1."
            )

        low = 4
        high = 8

        while (
            CorrelationPowerAnalysis.compute_power(
                r,
                high,
                alpha,
            )
            < power
        ):
            high *= 2

            if high > 10_000_000:
                raise RuntimeError(
                    "Unable to determine "
                    "sample size."
                )

        while low < high:
            mid = (
                low + high
            ) // 2

            current = (
                CorrelationPowerAnalysis
                .compute_power(
                    r,
                    mid,
                    alpha,
                )
            )

            if current >= power:
                high = mid
            else:
                low = mid + 1

        return int(low)

    # ==========================================================
# EFFECT SIZE
# ==========================================================

    @staticmethod

    @staticmethod
    def compute_effect_size(
        sample_size,
        alpha=0.05,
        power=0.80,
    ):
        """
        Smallest absolute correlation detectable
        at the requested power.
        """

        n = int(sample_size)

        if n < 4:
            raise ValueError(
                "sample_size must be at least 4."
            )

        if not 0 < power < 1:
            raise ValueError(
                "power must be between 0 and 1."
            )

        def objective(r):
            return (
                CorrelationPowerAnalysis
                .compute_power(
                    r,
                    n,
                    alpha,
                )
                - power
            )

        effect = brentq(
            objective,
            1e-10,
            0.999999,
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