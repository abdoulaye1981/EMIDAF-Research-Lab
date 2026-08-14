"""
=========================================================
EMIDAF Framework
Measures of Shape
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (
    BaseStatistic,
    StatisticResult
)

# ==========================================================
# SKEWNESS
# ==========================================================

class Skewness(

    BaseStatistic

):

    name = "Skewness"

    def __init__(

        self,

        bias=False,

    ):

        self.bias = bias

    def compute(

        self,

        x,

    ):

        value = stats.skew(

            x,

            bias=self.bias

        )

        return StatisticResult(

            statistic="Skewness",

            value=float(value)

        )

# ==========================================================
# KURTOSIS
# ==========================================================

class Kurtosis(

    BaseStatistic

):

    name="Kurtosis"

    def __init__(

        self,

        fisher=True,

        bias=False,

    ):

        self.fisher = fisher

        self.bias = bias

    def compute(

        self,

        x,

    ):

        value = stats.kurtosis(

            x,

            fisher=self.fisher,

            bias=self.bias

        )

        return StatisticResult(

            statistic="Kurtosis",

            value=float(value)

        )

# ==========================================================
# PEARSON SKEWNESS
# ==========================================================

class PearsonSkewness(

    BaseStatistic

):

    name = "Pearson Skewness"

    def compute(

        self,

        x,

    ):

        mean = np.mean(x)

        median = np.median(x)

        std = np.std(

            x,

            ddof=1

        )

        value = (

            np.nan

            if std == 0

            else

            3 * (mean - median) / std

        )

        return StatisticResult(

            statistic="Pearson Skewness",

            value=float(value)

        )

# ==========================================================
# BOWLEY
# ==========================================================

class BowleySkewness(

    BaseStatistic

):

    name="Bowley Skewness"

    def compute(

        self,

        x,

    ):

        q1 = np.percentile(x,25)

        q2 = np.percentile(x,50)

        q3 = np.percentile(x,75)

        denominator = q3-q1

        value = (

            np.nan

            if denominator==0

            else

            (q3+q1-2*q2)/denominator

        )

        return StatisticResult(

            statistic="Bowley Skewness",

            value=float(value)

        )

# ==========================================================
# YULE
# ==========================================================

class YuleCoefficient(

    BaseStatistic

):

    name="Yule Coefficient"

    def compute(

        self,

        x,

    ):

        p10=np.percentile(x,10)

        p50=np.percentile(x,50)

        p90=np.percentile(x,90)

        denominator=p90-p10

        value=(

            np.nan

            if denominator==0

            else

            (p90+p10-2*p50)/denominator

        )

        return StatisticResult(

            statistic="Yule Coefficient",

            value=float(value)

        )

# ==========================================================
# PEAKEDNESS
# ==========================================================

class Peakedness(

    BaseStatistic

):

    name="Peakedness"

    def compute(

        self,

        x,

    ):

        value = stats.kurtosis(

            x,

            fisher=False,

            bias=False

        )

        return StatisticResult(

            statistic="Peakedness",

            value=float(value)

        )

# ==========================================================
# SERVICE
# ==========================================================

class Shape:

    registry = {

        "skewness": Skewness,

        "kurtosis": Kurtosis,

        "pearson": PearsonSkewness,

        "bowley": BowleySkewness,

        "yule": YuleCoefficient,

        "peakedness": Peakedness

    }

    @classmethod

    def compute(

        cls,

        method,

        x,

        **kwargs,

    ):

        model = cls.registry[method](

            **kwargs

        )

        return model.compute(x)

    @classmethod

    def all(

        cls,

        x,

    ):

        results = {}

        for name in cls.registry:

            try:

                results[name] = (

                    cls.compute(

                        name,

                        x

                    ).value

                )

            except Exception:

                results[name] = None

        return results