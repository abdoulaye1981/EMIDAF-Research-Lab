"""
=========================================================
EMIDAF Framework
Circular Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy.stats import circmean
from scipy.stats import circstd
from scipy.stats import circvar

from .base import (
    BaseStatistic,
    StatisticResult
)

# ==========================================================
# CIRCULAR MEAN
# ==========================================================

class CircularMean(

    BaseStatistic

):

    name="Circular Mean"

    def __init__(

        self,

        low=0,

        high=2*np.pi,

    ):

        self.low=low

        self.high=high

    def compute(

        self,

        x,

    ):

        value=circmean(

            x,

            low=self.low,

            high=self.high

        )

        return StatisticResult(

            statistic="Circular Mean",

            value=float(value)

        )

# ==========================================================
# CIRCULAR VARIANCE
# ==========================================================

class CircularVariance(

    BaseStatistic

):

    name="Circular Variance"

    def __init__(

        self,

        low=0,

        high=2*np.pi,

    ):

        self.low=low

        self.high=high

    def compute(

        self,

        x,

    ):

        value=circvar(

            x,

            low=self.low,

            high=self.high

        )

        return StatisticResult(

            statistic="Circular Variance",

            value=float(value)

        )

# ==========================================================
# CIRCULAR STANDARD DEVIATION
# ==========================================================

class CircularStandardDeviation(

    BaseStatistic

):

    name="Circular Standard Deviation"

    def __init__(

        self,

        low=0,

        high=2*np.pi,

    ):

        self.low=low

        self.high=high

    def compute(

        self,

        x,

    ):

        value=circstd(

            x,

            low=self.low,

            high=self.high

        )

        return StatisticResult(

            statistic="Circular Standard Deviation",

            value=float(value)

        )

# ==========================================================
# MEAN RESULTANT LENGTH
# ==========================================================

class MeanResultantLength(

    BaseStatistic

):

    name="Mean Resultant Length"

    def compute(

        self,

        x,

    ):

        sin_mean=np.mean(

            np.sin(x)

        )

        cos_mean=np.mean(

            np.cos(x)

        )

        value=np.sqrt(

            sin_mean**2+

            cos_mean**2

        )

        return StatisticResult(

            statistic="Mean Resultant Length",

            value=float(value)

        )

# ==========================================================
# MEAN DIRECTION
# ==========================================================

class MeanDirection(

    BaseStatistic

):

    name="Mean Direction"

    def compute(

        self,

        x,

    ):

        sin_mean=np.mean(

            np.sin(x)

        )

        cos_mean=np.mean(

            np.cos(x)

        )

        direction=np.arctan2(

            sin_mean,

            cos_mean

        )

        if direction<0:

            direction+=2*np.pi

        return StatisticResult(

            statistic="Mean Direction",

            value=float(direction)

        )

# ==========================================================
# MEAN DIRECTION
# ==========================================================

class MeanDirection(

    BaseStatistic

):

    name="Mean Direction"

    def compute(

        self,

        x,

    ):

        sin_mean=np.mean(

            np.sin(x)

        )

        cos_mean=np.mean(

            np.cos(x)

        )

        direction=np.arctan2(

            sin_mean,

            cos_mean

        )

        if direction<0:

            direction+=2*np.pi

        return StatisticResult(

            statistic="Mean Direction",

            value=float(direction)

        )

# ==========================================================
# SERVICE
# ==========================================================

class Circular:

    registry={

        "mean":

            CircularMean,

        "variance":

            CircularVariance,

        "std":

            CircularStandardDeviation,

        "direction":

            MeanDirection,

        "resultant":

            MeanResultantLength,

        "kappa":

            VonMisesConcentration

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