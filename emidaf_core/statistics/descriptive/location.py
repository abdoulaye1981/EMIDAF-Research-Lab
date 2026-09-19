"""
=========================================================
EMIDAF Framework
Location Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Mesures de tendance centrale.

Contient :

- Mean
- Median
- Mode
- Minimum
- Maximum
- GeometricMean
- HarmonicMean
- TrimmedMean
=========================================================
"""
from __future__ import annotations
from abc import ABC
import numpy as np
import pandas as pd
from scipy.stats import gmean
from scipy.stats import hmean
from scipy.stats import trim_mean
from ..base.descriptive_statistic import DescriptiveStatistic
from .validator import StatisticsValidator
from .base import StatisticResult

class LocationStatistic(DescriptiveStatistic, ABC):
    """
    Classe de base des mesures de position.
    """
    category = 'Location'

class Mean(LocationStatistic):
    name = 'Mean'
    description = 'Arithmetic Mean'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        return StatisticResult(statistic='Mean', value=float(values.mean()))

class Median(LocationStatistic):
    name = 'Median'
    description = 'Median'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        return StatisticResult(statistic='Median', value=float(values.median()))

class Mode(LocationStatistic):
    name = 'Mode'
    description = 'Most frequent value'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.series(values)
        mode = values.mode()
        if mode.empty:
            return np.nan
        return mode.iloc[0]

class Minimum(LocationStatistic):
    name = 'Minimum'
    description = 'Minimum value'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        return float(values.min())

class Maximum(LocationStatistic):
    name = 'Maximum'
    description = 'Maximum value'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        return float(values.max())

class GeometricMean(LocationStatistic):
    name = 'Geometric Mean'
    description = 'Geometric Mean'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        if (values <= 0).any():
            return np.nan
        return float(gmean(values))

class HarmonicMean(LocationStatistic):
    name = 'Harmonic Mean'
    description = 'Harmonic Mean'

    @classmethod
    def compute(cls, values):
        values = StatisticsValidator.require_numeric(values)
        if (values <= 0).any():
            return np.nan
        return float(hmean(values))

class TrimmedMean(LocationStatistic):
    """
    Moyenne tronquée.

    Par défaut : 10 %
    """
    name = 'Trimmed Mean'
    description = 'Trimmed Mean'

    @classmethod
    def compute(cls, values, proportion: float=0.1):
        values = StatisticsValidator.require_numeric(values)
        return float(trim_mean(values, proportion))

class LocationStatistics:
    """
    Calcul de toutes les mesures de position.
    """

    @staticmethod
    def compute(values):
        return {'mean': Mean.compute(values), 'median': Median.compute(values), 'mode': Mode.compute(values), 'minimum': Minimum.compute(values), 'maximum': Maximum.compute(values), 'geometric_mean': GeometricMean.compute(values), 'harmonic_mean': HarmonicMean.compute(values), 'trimmed_mean': TrimmedMean.compute(values)}
