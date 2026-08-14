"""
=========================================================
EMIDAF Framework
Measures of Dispersion
=========================================================
"""

from __future__ import annotations

import numpy as np

from .base import (
    BaseStatistic,
    StatisticResult
)

class Variance(

    BaseStatistic

):

    name="Variance"

    def __init__(

        self,

        ddof=1,

    ):

        self.ddof=ddof

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Variance",

            value=float(

                np.var(

                    x,

                    ddof=self.ddof

                )

            )

        )

class StandardDeviation(

    BaseStatistic

):

    name="StandardDeviation"

    def __init__(

        self,

        ddof=1,

    ):

        self.ddof=ddof

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="StandardDeviation",

            value=float(

                np.std(

                    x,

                    ddof=self.ddof

                )

            )

        )

class Range(

    BaseStatistic

):

    name="Range"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Range",

            value=float(

                np.max(x)-np.min(x)

            )

        )

class InterquartileRange(

    BaseStatistic

):

    name="IQR"

    def compute(

        self,

        x,

    ):

        q1=np.percentile(x,25)

        q3=np.percentile(x,75)

        return StatisticResult(

            statistic="IQR",

            value=float(q3-q1)

        )

class MeanAbsoluteDeviation(

    BaseStatistic

):

    name="MAD"

    def compute(

        self,

        x,

    ):

        mean=np.mean(x)

        mad=np.mean(

            np.abs(

                x-mean

            )

        )

        return StatisticResult(

            statistic="Mean Absolute Deviation",

            value=float(mad)

        )

class MedianAbsoluteDeviation(

    BaseStatistic

):

    name="MedianMAD"

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

class CoefficientVariation(

    BaseStatistic

):

    name="CoefficientVariation"

    def compute(

        self,

        x,

    ):

        mean=np.mean(x)

        std=np.std(

            x,

            ddof=1

        )

        value=np.nan if mean==0 else std/mean

        return StatisticResult(

            statistic="Coefficient of Variation",

            value=float(value)

        )

class CoefficientVariation(

    BaseStatistic

):

    name="CoefficientVariation"

    def compute(

        self,

        x,

    ):

        mean=np.mean(x)

        std=np.std(

            x,

            ddof=1

        )

        value=np.nan if mean==0 else std/mean

        return StatisticResult(

            statistic="Coefficient of Variation",

            value=float(value)

        )
    
class Dispersion:

    registry={

        "variance":Variance,

        "std":StandardDeviation,

        "range":Range,

        "iqr":InterquartileRange,

        "mad":MeanAbsoluteDeviation,

        "median_mad":MedianAbsoluteDeviation,

        "cv":CoefficientVariation

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