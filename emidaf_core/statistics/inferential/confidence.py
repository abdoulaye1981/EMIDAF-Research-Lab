"""
=========================================================
EMIDAF Framework
Confidence Intervals
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from statsmodels.stats.proportion import (

    proportion_confint

)

from .base import (

    InferentialResult

)

# ==========================================================
# BASE
# ==========================================================

class ConfidenceInterval:
    """
    Classe utilitaire pour le calcul
    des intervalles de confiance.
    """

    # ==========================================================
# MEAN
# ==========================================================

    @staticmethod

    def mean(

        x,

        confidence=0.95,

    ):

        x=np.asarray(x)

        n=len(x)

        mean=np.mean(x)

        sem=stats.sem(x)

        alpha=1-confidence

        interval=stats.t.interval(

            confidence,

            df=n-1,

            loc=mean,

            scale=sem

        )

        return InferentialResult(

            test="Confidence Interval Mean",

            confidence_interval=interval,

            metadata={

                "mean":mean,

                "confidence":confidence

            }

        )

    # ==========================================================
# MEDIAN
# ==========================================================

    @staticmethod

    def median(

        x,

        confidence=0.95,

        n_bootstrap=5000,

    ):

        x=np.asarray(x)

        medians=[]

        for _ in range(

            n_bootstrap

        ):

            sample=np.random.choice(

                x,

                len(x),

                replace=True

            )

            medians.append(

                np.median(sample)

            )

        alpha=1-confidence

        lower=np.percentile(

            medians,

            100*alpha/2

        )

        upper=np.percentile(

            medians,

            100*(1-alpha/2)

        )

        return InferentialResult(

            test="Confidence Interval Median",

            confidence_interval=(

                float(lower),

                float(upper)

            )

        )

    # ==========================================================
# MEDIAN
# ==========================================================

    @staticmethod

    def median(

        x,

        confidence=0.95,

        n_bootstrap=5000,

    ):

        x=np.asarray(x)

        medians=[]

        for _ in range(

            n_bootstrap

        ):

            sample=np.random.choice(

                x,

                len(x),

                replace=True

            )

            medians.append(

                np.median(sample)

            )

        alpha=1-confidence

        lower=np.percentile(

            medians,

            100*alpha/2

        )

        upper=np.percentile(

            medians,

            100*(1-alpha/2)

        )

        return InferentialResult(

            test="Confidence Interval Median",

            confidence_interval=(

                float(lower),

                float(upper)

            )

        )

          # ==========================================================
    # VARIANCE
    # ==========================================================

    @staticmethod
    def variance(
        x,
        confidence=0.95,
    ):

        x = np.asarray(x)

        n = len(x)

        variance = np.var(
            x,
            ddof=1
        )

        alpha = 1 - confidence

        chi2_lower = stats.chi2.ppf(
            1 - alpha / 2,
            n - 1
        )

        chi2_upper = stats.chi2.ppf(
            alpha / 2,
            n - 1
        )

        lower = (
            (n - 1) * variance
        ) / chi2_lower

        upper = (
            (n - 1) * variance
        ) / chi2_upper

        return InferentialResult(
            test="Confidence Interval Variance",
            confidence_interval=(
                float(lower),
                float(upper)
            ),
            metadata={
                "variance": float(variance),
                "confidence": confidence
            }
        )

    # ==========================================================
# STANDARD DEVIATION
# ==========================================================

    @staticmethod

    def standard_deviation(

        x,

        confidence=0.95,

    ):

        result=ConfidenceInterval.variance(

            x,

            confidence

        )

        lower=np.sqrt(

            result.confidence_interval[0]

        )

        upper=np.sqrt(

            result.confidence_interval[1]

        )

        result.test="Confidence Interval Standard Deviation"

        result.confidence_interval=(

            float(lower),

            float(upper)

        )

        return result

    # ==========================================================
# PROPORTION
# ==========================================================

    @staticmethod

    def proportion(

        successes,

        n,

        confidence=0.95,

        method="wilson",

    ):

        alpha=1-confidence

        interval=proportion_confint(

            successes,

            n,

            alpha=alpha,

            method=method

        )

        return InferentialResult(

            test="Confidence Interval Proportion",

            confidence_interval=(

                float(interval[0]),

                float(interval[1])

            )

        )

    # ==========================================================
# DIFFERENCE OF MEANS
# ==========================================================

    @staticmethod

    def difference_means(

        x,

        y,

        confidence=0.95,

    ):

        x=np.asarray(x)

        y=np.asarray(y)

        nx=len(x)

        ny=len(y)

        mean=np.mean(x)-np.mean(y)

        sx=np.var(

            x,

            ddof=1

        )

        sy=np.var(

            y,

            ddof=1

        )

        se=np.sqrt(

            sx/nx+

            sy/ny

        )

        df=nx+ny-2

        alpha=1-confidence

        critical=stats.t.ppf(

            1-alpha/2,

            df

        )

        interval=(

            mean-critical*se,

            mean+critical*se

        )

        return InferentialResult(

            test="Confidence Interval Difference of Means",

            confidence_interval=(

                float(interval[0]),

                float(interval[1])

            )

        )

    # ==========================================================
# CORRELATION
# ==========================================================

    @staticmethod

    def correlation(

        r,

        n,

        confidence=0.95,

    ):

        z=np.arctanh(r)

        se=1/np.sqrt(n-3)

        alpha=1-confidence

        zc=stats.norm.ppf(

            1-alpha/2

        )

        lower=np.tanh(

            z-zc*se

        )

        upper=np.tanh(

            z+zc*se

        )

        return InferentialResult(

            test="Confidence Interval Correlation",

            confidence_interval=(

                float(lower),

                float(upper)

            )

        )
    
    # ==========================================================
# SERVICE
# ==========================================================

class Confidence:

    mean=ConfidenceInterval.mean

    median=ConfidenceInterval.median

    variance=ConfidenceInterval.variance

    standard_deviation=(

        ConfidenceInterval.standard_deviation

    )

    proportion=(

        ConfidenceInterval.proportion

    )

    difference_means=(

        ConfidenceInterval.difference_means

    )

    correlation=(

        ConfidenceInterval.correlation

    )
