"""
=========================================================
EMIDAF Framework
Weighted Descriptive Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""
from __future__ import annotations
import numpy as np
from .base import BaseStatistic, StatisticResult

class WeightedMean(BaseStatistic):
    name = 'Weighted Mean'

    def compute(self, x, weights):
        value = np.average(x, weights=weights)
        return StatisticResult(statistic='Weighted Mean', value=float(value))

class WeightedVariance(BaseStatistic):
    name = 'Weighted Variance'

    def compute(self, x, weights):
        mean = np.average(x, weights=weights)
        value = np.average((x - mean) ** 2, weights=weights)
        return StatisticResult(statistic='Weighted Variance', value=float(value))

class WeightedStandardDeviation(BaseStatistic):
    name = 'Weighted Standard Deviation'

    def compute(self, x, weights):
        variance = WeightedVariance().compute(x, weights).value
        value = np.sqrt(variance)
        return StatisticResult(statistic='Weighted Standard Deviation', value=float(value))

class WeightedCoefficientVariation(BaseStatistic):
    name = 'Weighted CV'

    def compute(self, x, weights):
        mean = np.average(x, weights=weights)
        variance = np.average((x - mean) ** 2, weights=weights)
        std = np.sqrt(variance)
        value = np.nan if mean == 0 else std / mean
        return StatisticResult(statistic='Weighted Coefficient of Variation', value=float(value))

class WeightedSum(BaseStatistic):
    name = 'Weighted Sum'

    def compute(self, x, weights):
        value = np.sum(x * weights)
        return StatisticResult(statistic='Weighted Sum', value=float(value))

class WeightedQuantile(BaseStatistic):
    name = 'Weighted Quantile'

    def __init__(self, q=0.5):
        self.q = q

    def compute(self, x, weights):
        sorter = np.argsort(x)
        x = x[sorter]
        weights = weights[sorter]
        cumulative = np.cumsum(weights)
        cumulative = cumulative / cumulative[-1]
        value = np.interp(self.q, cumulative, x)
        return StatisticResult(statistic='Weighted Quantile', value=float(value))

class WeightedMedian(WeightedQuantile):
    name = 'Weighted Median'

    def __init__(self):
        super().__init__(q=0.5)

class WeightedPercentiles(BaseStatistic):
    name = 'Weighted Percentiles'

    def __init__(self, percentiles=None):
        self.percentiles = percentiles or [5, 10, 25, 50, 75, 90, 95]

    def compute(self, x, weights):
        values = {}
        for p in self.percentiles:
            q = WeightedQuantile(q=p / 100)
            values[f'P{p}'] = q.compute(x, weights).value
        return StatisticResult(statistic='Weighted Percentiles', value=values)

class Weighted:
    registry = {'mean': WeightedMean, 'variance': WeightedVariance, 'std': WeightedStandardDeviation, 'cv': WeightedCoefficientVariation, 'sum': WeightedSum, 'quantile': WeightedQuantile, 'median': WeightedMedian, 'percentiles': WeightedPercentiles}

    @classmethod
    def compute(cls, method, x, weights, **kwargs):
        model = cls.registry[method](**kwargs)
        return model.compute(x, weights)

    @classmethod
    def all(cls, x, weights):
        results = {}
        for name in cls.registry:
            if name == 'quantile':
                continue
            try:
                results[name] = cls.compute(name, x, weights).value
            except Exception:
                results[name] = None
        return results
