"""
=========================================================
EMIDAF Framework
Measures of Position
=========================================================
"""

from __future__ import annotations

import numpy as np

from .base import (
    BaseStatistic,
    StatisticResult
)

# ==========================================================
# MINIMUM
# ==========================================================

class Minimum(

    BaseStatistic

):

    name = "Minimum"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Minimum",

            value=float(

                np.min(x)

            )

        )

# ==========================================================
# MAXIMUM
# ==========================================================

class Maximum(

    BaseStatistic

):

    name="Maximum"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Maximum",

            value=float(

                np.max(x)

            )

        )

# ==========================================================
# Q1
# ==========================================================

class FirstQuartile(

    BaseStatistic

):

    name="Q1"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="First Quartile",

            value=float(

                np.percentile(

                    x,

                    25

                )

            )

        )

# ==========================================================
# MEDIAN
# ==========================================================

class Median(

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

                np.percentile(

                    x,

                    50

                )

            )

        )

# ==========================================================
# Q3
# ==========================================================

class ThirdQuartile(

    BaseStatistic

):

    name="Q3"

    def compute(

        self,

        x,

    ):

        return StatisticResult(

            statistic="Third Quartile",

            value=float(

                np.percentile(

                    x,

                    75

                )

            )

        )

# ==========================================================
# DECILES
# ==========================================================

class Deciles(

    BaseStatistic

):

    name="Deciles"

    def compute(

        self,

        x,

    ):

        values={

            f"D{i}":

            float(

                np.percentile(

                    x,

                    i*10

                )

            )

            for i in range(

                1,

                10

            )

        }

        return StatisticResult(

            statistic="Deciles",

            value=values

        )

# ==========================================================
# PERCENTILES
# ==========================================================

class Percentiles(

    BaseStatistic

):

    name="Percentiles"

    def __init__(

        self,

        values=None,

    ):

        if values is None:

            values=[

                1,

                5,

                10,

                25,

                50,

                75,

                90,

                95,

                99

            ]

        self.values=values

    def compute(

        self,

        x,

    ):

        result={}

        for p in self.values:

            result[f"P{p}"]=float(

                np.percentile(

                    x,

                    p

                )

            )

        return StatisticResult(

            statistic="Percentiles",

            value=result

        )

# ==========================================================
# QUANTILES
# ==========================================================

class Quantiles(

    BaseStatistic

):

    name="Quantiles"

    def __init__(

        self,

        q,

    ):

        self.q=q

    def compute(

        self,

        x,

    ):

        values=np.quantile(

            x,

            self.q

        )

        return StatisticResult(

            statistic="Quantiles",

            value=values.tolist()

        )

# ==========================================================
# SERVICE
# ==========================================================

class Position:

    registry={

        "min":Minimum,

        "max":Maximum,

        "q1":FirstQuartile,

        "median":Median,

        "q3":ThirdQuartile,

        "deciles":Deciles,

        "percentiles":Percentiles,

        "quantiles":Quantiles

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

                if name=="quantiles":

                    continue

                results[name]=(

                    cls.compute(

                        name,

                        x

                    ).value

                )

            except Exception:

                results[name]=None

        return results