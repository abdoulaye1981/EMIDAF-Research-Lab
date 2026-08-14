"""
=========================================================
EMIDAF Framework
Distribution Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Mesures de forme de la distribution.

Contient

- Skewness
- Kurtosis
- Entropy
- Quantiles
- Percentiles
- Moments
=========================================================
"""

from __future__ import annotations

from abc import ABC

import numpy as np
import pandas as pd

from scipy.stats import entropy
from scipy.stats import moment

from ..base.descriptive_statistic import DescriptiveStatistic
from .validator import StatisticsValidator


class DistributionStatistic(DescriptiveStatistic, ABC):
    """
    Classe mère des statistiques de distribution.
    """

    category = "Distribution"


# =====================================================
# SKEWNESS
# =====================================================

class Skewness(DistributionStatistic):

    name = "Skewness"

    description = "Distribution Skewness"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        return float(

            values.skew()

        )


# =====================================================
# KURTOSIS
# =====================================================

class Kurtosis(DistributionStatistic):

    name = "Kurtosis"

    description = "Distribution Kurtosis"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        return float(

            values.kurt()

        )


# =====================================================
# ENTROPY
# =====================================================

class Entropy(DistributionStatistic):

    name = "Entropy"

    description = "Shannon Entropy"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        counts = values.value_counts()

        probabilities = counts / counts.sum()

        return float(

            entropy(probabilities)

        )


# =====================================================
# QUANTILES
# =====================================================

class Quantiles(DistributionStatistic):

    name = "Quantiles"

    description = "Quartiles"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        return {

            "q0": float(values.quantile(0.00)),

            "q1": float(values.quantile(0.25)),

            "q2": float(values.quantile(0.50)),

            "q3": float(values.quantile(0.75)),

            "q4": float(values.quantile(1.00))

        }


# =====================================================
# PERCENTILES
# =====================================================

class Percentiles(DistributionStatistic):

    name = "Percentiles"

    description = "Common Percentiles"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        return {

            "p1": float(values.quantile(0.01)),

            "p5": float(values.quantile(0.05)),

            "p10": float(values.quantile(0.10)),

            "p25": float(values.quantile(0.25)),

            "p50": float(values.quantile(0.50)),

            "p75": float(values.quantile(0.75)),

            "p90": float(values.quantile(0.90)),

            "p95": float(values.quantile(0.95)),

            "p99": float(values.quantile(0.99))

        }


# =====================================================
# MOMENTS
# =====================================================

class Moments(DistributionStatistic):

    """
    Moments statistiques.
    """

    name = "Moments"

    description = "Statistical Moments"

    @classmethod
    def compute(cls, values):

        values = StatisticsValidator.require_numeric(values)

        return {

            "first": float(

                moment(values, moment=1)

            ),

            "second": float(

                moment(values, moment=2)

            ),

            "third": float(

                moment(values, moment=3)

            ),

            "fourth": float(

                moment(values, moment=4)

            )

        }


# =====================================================
# DISTRIBUTION STATISTICS
# =====================================================

class DistributionStatistics:
    """
    Calcul de toutes les statistiques de distribution.
    """

    @staticmethod
    def compute(values):

        values = StatisticsValidator.require_numeric(values)

        return {

            "skewness":

                Skewness.compute(values),

            "kurtosis":

                Kurtosis.compute(values),

            "entropy":

                Entropy.compute(values),

            "quantiles":

                Quantiles.compute(values),

            "percentiles":

                Percentiles.compute(values),

            "moments":

                Moments.compute(values)

        }