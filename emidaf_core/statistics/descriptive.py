"""
=========================================================
EMIDAF Framework
Descriptive Statistics Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

Version : 1.0.0

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

import numpy as np
import pandas as pd

from scipy import stats

# ==========================================================
# RESULT
# ==========================================================

@dataclass(slots=True)

class StatisticsResult:

    variable:str=""

    statistic:str=""

    value:float=None

    interpretation:str=""

    recommendation:str=""

    metadata:dict=field(

        default_factory=dict

    )

# ==========================================================
# BASE
# ==========================================================

class BaseStatistic:

    """
    Classe mère.

    Toutes les statistiques
    héritent de cette classe.
    """

    name="Statistic"

    def compute(

        self,

        x,

    ):

        raise NotImplementedError()

# ==========================================================
# MEAN
# ==========================================================

class Mean(

    BaseStatistic

):

    name="Mean"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Mean",

            value=float(

                np.mean(x)

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

        return StatisticsResult(

            statistic="Median",

            value=float(

                np.median(x)

            )

        )
    
# ==========================================================
# MODE
# ==========================================================

class Mode(

    BaseStatistic

):

    name="Mode"

    def compute(

        self,

        x,

    ):

        mode=stats.mode(

            x,

            keepdims=False

        )

        return StatisticsResult(

            statistic="Mode",

            value=float(

                mode.mode

            )

        )

# ==========================================================
# SUM
# ==========================================================

class Sum(

    BaseStatistic

):

    name="Sum"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Sum",

            value=float(

                np.sum(x)

            )

        )

# ==========================================================
# SUM
# ==========================================================

class Sum(

    BaseStatistic

):

    name="Sum"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Sum",

            value=float(

                np.sum(x)

            )

        )

# ==========================================================
# MAX
# ==========================================================

class Maximum(

    BaseStatistic

):

    name="Maximum"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Maximum",

            value=float(

                np.max(x)

            )

        )
    
# ==========================================================
# RANGE
# ==========================================================

class Range(

    BaseStatistic

):

    name="Range"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Range",

            value=float(

                np.max(x)-np.min(x)

            )

        )
    
# ==========================================================
# VARIANCE
# ==========================================================

class Variance(

    BaseStatistic

):

    name="Variance"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="Variance",

            value=float(

                np.var(

                    x,

                    ddof=1

                )

            )

        )

# ==========================================================
# STANDARD DEVIATION
# ==========================================================

class StandardDeviation(

    BaseStatistic

):

    name="StandardDeviation"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="StandardDeviation",

            value=float(

                np.std(

                    x,

                    ddof=1

                )

            )

        )

# ==========================================================
# STANDARD DEVIATION
# ==========================================================

class StandardDeviation(

    BaseStatistic

):

    name="StandardDeviation"

    def compute(

        self,

        x,

    ):

        return StatisticsResult(

            statistic="StandardDeviation",

            value=float(

                np.std(

                    x,

                    ddof=1

                )

            )

        )

# ==========================================================
# SERVICE
# ==========================================================

class Descriptive:

    registry={

        "mean":Mean,

        "median":Median,

        "mode":Mode,

        "sum":Sum,

        "min":Minimum,

        "max":Maximum,

        "range":Range,

        "variance":Variance,

        "std":StandardDeviation,

        "cv":CoefficientVariation

    }

    @classmethod

    def compute(

        cls,

        method,

        x,

    ):

        model=cls.registry[method]()

        return model.compute(x)