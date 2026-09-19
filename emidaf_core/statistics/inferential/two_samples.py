"""
=========================================================
EMIDAF Framework
Two Independent Samples Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""
from __future__ import annotations
import numpy as np
from scipy import stats
from .base import BaseInferentialTest, InferentialResult

class WelchTTest(BaseInferentialTest):
    name = 'Welch Test'

    def compute(self, x, y, alpha=0.05):
        statistic, p = stats.ttest_ind(x, y, equal_var=False, nan_policy='omit')
        return InferentialResult(test=self.name, statistic=float(statistic), p_value=float(p), alpha=alpha, reject_null=p < alpha)

class KolmogorovSmirnovTest(BaseInferentialTest):
    name = 'Kolmogorov-Smirnov'

    def compute(self, x, y, alpha=0.05):
        statistic, p = stats.ks_2samp(x, y)
        return InferentialResult(test=self.name, statistic=float(statistic), p_value=float(p), alpha=alpha, reject_null=p < alpha)

class BrunnerMunzelTest(BaseInferentialTest):
    name = 'Brunner-Munzel'

    def compute(self, x, y, alpha=0.05):
        statistic, p = stats.brunnermunzel(x, y)
        return InferentialResult(test=self.name, statistic=float(statistic), p_value=float(p), alpha=alpha, reject_null=p < alpha)

class MoodMedianTest(BaseInferentialTest):
    name = 'Mood Median Test'

    def compute(self, x, y, alpha=0.05):
        statistic, p, _, _ = stats.median_test(x, y)
        return InferentialResult(test=self.name, statistic=float(statistic), p_value=float(p), alpha=alpha, reject_null=p < alpha)

class FlignerPolicelloTest(BaseInferentialTest):
    name = 'Fligner-Policello'

    def compute(self, x, y, alpha=0.05):
        raise NotImplementedError('À implémenter dans EMIDAF.')

class TwoSamples:
    registry = {'welch': WelchTTest, 'kolmogorov': KolmogorovSmirnovTest, 'brunner_munzel': BrunnerMunzelTest, 'mood': MoodMedianTest}

    @classmethod
    def compute(cls, method, **kwargs):
        if method not in cls.registry:
            raise ValueError(f'Méthode inconnue : {method}. Méthodes disponibles : {list(cls.registry.keys())}')
        model = cls.registry[method]()
        return model.compute(**kwargs)
