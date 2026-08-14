"""
=========================================================
EMIDAF Framework
Robust Descriptive Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats
from scipy.stats.mstats import winsorize

from .base import (
    BaseStatistic,
    StatisticResult
)

# ==========================================================
# MEDIAN
# ==========================================================

class RobustMedian(

    BaseStatistic

):

    name="Median"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Median",

            value=float(

                np.median(x)

            )

        )

# ==========================================================
# TRIMMED MEAN
# ==========================================================

class TrimmedMean(

    BaseStatistic

):

    name="Trimmed Mean"

    def __init__(

        self,

        proportion=0.10,

    ):

        self.proportion=proportion

    def compute(

        self,

        x,

    ):

        value=stats.trim_mean(

            x,

            self.proportion

        )

        return StatisticResult(

            statistic="Trimmed Mean",

            value=float(value)

        )
    
# ==========================================================
# WINSORIZED MEAN
# ==========================================================

class WinsorizedMean(

    BaseStatistic

):

    name="Winsorized Mean"

    def __init__(

        self,

        limits=(0.05,0.05),

    ):

        self.limits=limits

    def compute(

        self,

        x,

    ):

        w=winsorize(

            x,

            limits=self.limits

        )

        return StatisticResult(

            statistic="Winsorized Mean",

            value=float(

                np.mean(w)

            )

        )

# ==========================================================
# WINSORIZED VARIANCE
# ==========================================================

class WinsorizedVariance(

    BaseStatistic

):

    name="Winsorized Variance"

    def __init__(

        self,

        limits=(0.05,0.05),

    ):

        self.limits=limits

    def compute(

        self,

        x,

    ):

        w=winsorize(

            x,

            limits=self.limits

        )

        return StatisticResult(

            statistic="Winsorized Variance",

            value=float(

                np.var(

                    w,

                    ddof=1

                )

            )

        )

# ==========================================================
# MEDIAN ABSOLUTE DEVIATION
# ==========================================================

class MedianAbsoluteDeviation(

    BaseStatistic

):

    name="MAD"

    def compute(

        self,

        x,

    ):

        median=np.median(x)

        mad=np.median(

            np.abs(

                x-median

            )

        )

        return StatisticResult(

            statistic="Median Absolute Deviation",

            value=float(mad)

        )

# ==========================================================
# ROBUST STANDARD DEVIATION
# ==========================================================

class RobustStandardDeviation(

    BaseStatistic

):

    name="Robust Standard Deviation"

    def compute(

        self,

        x,

    ):

        median=np.median(x)

        mad=np.median(

            np.abs(

                x-median

            )

        )

        sigma=1.4826*mad

        return StatisticResult(

            statistic="Robust Standard Deviation",

            value=float(sigma)

        )

# ==========================================================
# MIDHINGE
# ==========================================================

class Midhinge(

    BaseStatistic

):

    name="Midhinge"

    def compute(

        self,

        x,

    ):

        q1=np.percentile(x,25)

        q3=np.percentile(x,75)

        value=(q1+q3)/2

        return StatisticResult(

            statistic="Midhinge",

            value=float(value)

        )

# ==========================================================
# TUKEY TRIMEAN
# ==========================================================

class TukeyTrimean(

    BaseStatistic

):

    name="Tukey Trimean"

    def compute(

        self,

        x,

    ):

        q1=np.percentile(x,25)

        q2=np.percentile(x,50)

        q3=np.percentile(x,75)

        value=(

            q1+

            2*q2+

            q3

        )/4

        return StatisticResult(

            statistic="Tukey Trimean",

            value=float(value)

        )

# ==========================================================
# ROBUST MIDRANGE
# ==========================================================

class RobustMidrange(

    BaseStatistic

):

    name="Robust Midrange"

    def compute(

        self,

        x,

    ):

        p5=np.percentile(x,5)

        p95=np.percentile(x,95)

        value=(

            p5+p95

        )/2

        return StatisticResult(

            statistic="Robust Midrange",

            value=float(value)

        )

# ==========================================================
# SERVICE
# ==========================================================

class Robust:

    registry={

        "median":

            RobustMedian,

        "trimmed_mean":

            TrimmedMean,

        "winsorized_mean":

            WinsorizedMean,

        "winsorized_variance":

            WinsorizedVariance,

        "mad":

            MedianAbsoluteDeviation,

        "robust_std":

            RobustStandardDeviation,

        "midhinge":

            Midhinge,

        "trimean":

            TukeyTrimean,

        "robust_midrange":

            RobustMidrange

    }

    @classmethod

    def compute(

        cls,

        method,

        x,

        **kwargs,

    ):

        model=cls.registry[method](

            **kwargs

        )

        return model.compute(x)

    @classmethod

    def all(

        cls,

        x,

    ):

        results={}

        for name in cls.registry:

            try:

                results[name]=(

                    cls.compute(

                        name,

                        x

                    ).value

                )

            except Exception:

                results[name]=None

        return results