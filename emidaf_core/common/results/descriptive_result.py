"""
=========================================================
EMIDAF Framework
Descriptive Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat d'une analyse descriptive.

Utilisé par :

- SummaryStatistics
- NumericalAnalyzer
- DatasetProfiler
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .statistic_result import StatisticResult


@dataclass(slots=True)
class DescriptiveResult(StatisticResult):
    """
    Résultat des statistiques descriptives.
    """

    category: str = "Descriptive"

    # =====================================================
    # Position
    # =====================================================

    minimum: float | None = None

    maximum: float | None = None

    mean: float | None = None

    median: float | None = None

    mode: float | str | None = None

    geometric_mean: float | None = None

    harmonic_mean: float | None = None

    trimmed_mean: float | None = None

    # =====================================================
    # Dispersion
    # =====================================================

    variance: float | None = None

    standard_deviation: float | None = None

    coefficient_variation: float | None = None

    standard_error: float | None = None

    mean_absolute_deviation: float | None = None

    median_absolute_deviation: float | None = None

    iqr: float | None = None

    data_range: float | None = None

    # =====================================================
    # Distribution
    # =====================================================

    skewness: float | None = None

    kurtosis: float | None = None

    entropy: float | None = None

    # =====================================================
    # Fréquences
    # =====================================================

    count: int = 0

    unique: int = 0

    duplicated: int = 0

    # =====================================================
    # Quantiles
    # =====================================================

    quantiles: dict = field(default_factory=dict)

    percentiles: dict = field(default_factory=dict)

    moments: dict = field(default_factory=dict)

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Variable": self.variable,

            "Count": self.count,

            "Mean": self.mean,

            "Median": self.median,

            "Std": self.standard_deviation,

            "Min": self.minimum,

            "Max": self.maximum,

            "IQR": self.iqr,

            "Skewness": self.skewness,

            "Kurtosis": self.kurtosis

        }

    # =====================================================
    # Vérifications
    # =====================================================

    def is_normal(self):

        if self.skewness is None:

            return False

        if self.kurtosis is None:

            return False

        return (

            abs(self.skewness) < 1

            and

            abs(self.kurtosis) < 1

        )

    def has_outliers(self):

        if self.iqr is None:

            return False

        return self.iqr > 0

    # =====================================================
    # Export
    # =====================================================

    def compact(self):

        return {

            "variable": self.variable,

            "mean": self.mean,

            "std": self.standard_deviation,

            "min": self.minimum,

            "max": self.maximum

        }

    # =====================================================

    def __repr__(self):

        return (

            f"DescriptiveResult("

            f"variable='{self.variable}', "

            f"mean={self.mean}, "

            f"std={self.standard_deviation}"

            f")"

        )