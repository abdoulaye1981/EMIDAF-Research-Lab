"""
=========================================================
EMIDAF Framework
Equivalence Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    BaseInferentialTest,

    InferentialResult

)

# ==========================================================
# TOST
# ==========================================================

class TOSTTest(
    BaseInferentialTest
):

    name = "TOST"

    def compute(
        self,
        x,
        y,
        low,
        high,
        alpha=0.05,
    ):

        x = np.asarray(x)
        y = np.asarray(y)

        diff = np.mean(x) - np.mean(y)

        nx = len(x)
        ny = len(y)

        vx = np.var(
            x,
            ddof=1
        )

        vy = np.var(
            y,
            ddof=1
        )

        se = np.sqrt(
            vx / nx +
            vy / ny
        )

        df = nx + ny - 2

        t1 = (
            diff - low
        ) / se

        p1 = 1 - stats.t.cdf(
            t1,
            df
        )

        t2 = (
            diff - high
        ) / se

        p2 = stats.t.cdf(
            t2,
            df
        )

        reject = (
            p1 < alpha
            and
            p2 < alpha
        )

        return InferentialResult(
            test=self.name,
            statistic=float(diff),
            p_value=float(
                max(p1, p2)
            ),
            alpha=alpha,
            reject_null=reject,
            metadata={
                "lower_test": p1,
                "upper_test": p2,
                "equivalence_margin": (
                    low,
                    high
                )
            }
        )                   

# ==========================================================
# VARIANCE EQUIVALENCE
# ==========================================================

class VarianceEquivalence(

    BaseInferentialTest

):

    name="Variance Equivalence"

    def compute(

        self,

        x,

        y,

        tolerance=0.10,

    ):

        vx=np.var(

            x,

            ddof=1

        )

        vy=np.var(

            y,

            ddof=1

        )

        ratio=vx/vy

        equivalent=(

            abs(

                ratio-1

            )

            <=

            tolerance

        )

        return InferentialResult(

            test=self.name,

            statistic=float(

                ratio

            ),

            reject_null=equivalent

        )

# ==========================================================
# CORRELATION EQUIVALENCE
# ==========================================================

class CorrelationEquivalence(

    BaseInferentialTest

):

    name="Correlation Equivalence"

    def compute(

        self,

        r1,

        r2,

        tolerance=0.05,

    ):

        equivalent=(

            abs(

                r1-r2

            )

            <=

            tolerance

        )

        return InferentialResult(

            test=self.name,

            statistic=float(

                r1-r2

            ),

            reject_null=equivalent

        )

# ==========================================================
# SERVICE
# ==========================================================

class Equivalence:

    registry={

        "tost":

            TOSTTest,

        "variance":

            VarianceEquivalence,

        "correlation":

            CorrelationEquivalence

    }

    @classmethod

    def compute(

        cls,

        method,

        **kwargs,

    ):

        model=cls.registry[method]()

        return model.compute(

            **kwargs

        )
