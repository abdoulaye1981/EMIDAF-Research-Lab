"""
=========================================================
EMIDAF Framework
Power Analysis for Regression
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from scipy.stats import f, ncf
from scipy.optimize import brentq

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

    @staticmethod
    def compute_power(
        effect_size,
        predictors,
        sample_size,
        alpha=0.05,
    ):
        """
        Power of the overall multiple-regression
        F test using Cohen's f-squared.
        """

        f2 = float(effect_size)
        p = int(predictors)
        n = int(sample_size)

        if f2 < 0:
            raise ValueError(
                "effect_size must be non-negative."
            )

        if p < 1:
            raise ValueError(
                "predictors must be at least 1."
            )

        if n <= p + 1:
            raise ValueError(
                "sample_size must be greater "
                "than predictors + 1."
            )

        if not 0 < alpha < 1:
            raise ValueError(
                "alpha must be between 0 and 1."
            )

        df_num = p
        df_denom = n - p - 1

        critical = f.ppf(
            1 - alpha,
            df_num,
            df_denom,
        )

        ncp = (
            f2 * n
        )

        power = ncf.sf(
            critical,
            df_num,
            df_denom,
            ncp,
        )

        return float(power)

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    @staticmethod
    def compute_sample_size(
        effect_size,
        predictors,
        alpha=0.05,
        power=0.80,
    ):
        """
        Minimum total sample size required for
        the requested regression power.
        """

        f2 = float(effect_size)
        p = int(predictors)

        if f2 <= 0:
            raise ValueError(
                "effect_size must be positive."
            )

        if p < 1:
            raise ValueError(
                "predictors must be at least 1."
            )

        if not 0 < power < 1:
            raise ValueError(
                "power must be between 0 and 1."
            )

        low = p + 2
        high = max(
            2 * low,
            16,
        )

        while (
            RegressionPowerAnalysis.compute_power(
                f2,
                p,
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
                RegressionPowerAnalysis
                .compute_power(
                    f2,
                    p,
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
        predictors,
        sample_size,
        alpha=0.05,
        power=0.80,
    ):
        """
        Minimum Cohen f-squared detectable at
        the requested power.
        """

        p = int(predictors)
        n = int(sample_size)

        if p < 1:
            raise ValueError(
                "predictors must be at least 1."
            )

        if n <= p + 1:
            raise ValueError(
                "sample_size must be greater "
                "than predictors + 1."
            )

        if not 0 < power < 1:
            raise ValueError(
                "power must be between 0 and 1."
            )

        def objective(f2):
            return (
                RegressionPowerAnalysis
                .compute_power(
                    f2,
                    p,
                    n,
                    alpha,
                )
                - power
            )

        effect = brentq(
            objective,
            1e-12,
            100.0,
        )

        return float(effect)

    # ==========================================================
# ALPHA
# ==========================================================

    @staticmethod

    @staticmethod
    def compute_alpha(
        effect_size,
        predictors,
        sample_size,
        power=0.80,
    ):
        """
        Significance level required to obtain
        the requested regression power.
        """

        f2 = float(effect_size)
        p = int(predictors)
        n = int(sample_size)

        if f2 <= 0:
            raise ValueError(
                "effect_size must be positive."
            )

        if not 0 < power < 1:
            raise ValueError(
                "power must be between 0 and 1."
            )

        def objective(alpha):
            return (
                RegressionPowerAnalysis
                .compute_power(
                    f2,
                    p,
                    n,
                    alpha,
                )
                - power
            )

        alpha = brentq(
            objective,
            1e-10,
            0.999999,
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