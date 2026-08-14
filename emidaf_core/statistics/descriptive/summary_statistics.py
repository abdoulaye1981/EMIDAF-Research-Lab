"""
=========================================================
EMIDAF Framework
Summary Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Calcul optimisé des statistiques descriptives.

Toutes les statistiques sont calculées à partir
d'une seule validation des données.

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import entropy
from scipy.stats import gmean
from scipy.stats import hmean
from scipy.stats import median_abs_deviation
from scipy.stats import moment
from scipy.stats import trim_mean

from .validator import StatisticsValidator


class SummaryStatistics:
    """
    Calcul complet des statistiques descriptives.

    Cette classe est le coeur du moteur descriptif
    d'EMIDAF.
    """

    @staticmethod
    def compute(values) -> dict:

        # ==========================================
        # Validation
        # ==========================================

        values = StatisticsValidator.require_numeric(values)

        n = len(values)

        if n == 0:

            raise ValueError(
                "Empty Series."
            )

        # ==========================================
        # Pré-calcul
        # ==========================================

        minimum = float(values.min())

        maximum = float(values.max())

        mean = float(values.mean())

        median = float(values.median())

        std = float(values.std(ddof=1))

        variance = float(values.var(ddof=1))

        q1 = float(values.quantile(.25))

        q2 = float(values.quantile(.50))

        q3 = float(values.quantile(.75))

        data_range = maximum - minimum

        iqr = q3 - q1

        mad = float(

            np.mean(

                np.abs(values - mean)

            )

        )

        median_mad = float(

            median_abs_deviation(

                values,

                scale="normal"

            )

        )

        standard_error = std / np.sqrt(n)

        cv = np.nan

        if mean != 0:

            cv = std / mean * 100

        skewness = float(

            values.skew()

        )

        kurtosis = float(

            values.kurt()

        )

        counts = values.value_counts()

        probabilities = counts / counts.sum()

        shannon_entropy = float(

            entropy(probabilities)

        )

        # ==========================================
        # Moyennes spéciales
        # ==========================================

        geometric = np.nan

        harmonic = np.nan

        if (values > 0).all():

            geometric = float(

                gmean(values)

            )

            harmonic = float(

                hmean(values)

            )

        trimmed = float(

            trim_mean(

                values,

                0.10

            )

        )

        # ==========================================
        # Moments
        # ==========================================

        moments = {

            "first": float(

                moment(values, 1)

            ),

            "second": float(

                moment(values, 2)

            ),

            "third": float(

                moment(values, 3)

            ),

            "fourth": float(

                moment(values, 4)

            )

        }

        # ==========================================
        # Quantiles
        # ==========================================

        quantiles = {

            "0%": minimum,

            "25%": q1,

            "50%": q2,

            "75%": q3,

            "100%": maximum

        }

        # ==========================================
        # Percentiles
        # ==========================================

        percentiles = {

            "P1": float(values.quantile(.01)),

            "P5": float(values.quantile(.05)),

            "P10": float(values.quantile(.10)),

            "P90": float(values.quantile(.90)),

            "P95": float(values.quantile(.95)),

            "P99": float(values.quantile(.99))

        }

        # ==========================================
        # Mode
        # ==========================================

        mode = values.mode()

        if mode.empty:

            mode_value = np.nan

        else:

            mode_value = mode.iloc[0]

        # ==========================================
        # Résultat
        # ==========================================

        return {

            "count": n,

            "missing": int(values.isna().sum()),

            "unique": int(values.nunique()),

            "minimum": minimum,

            "maximum": maximum,

            "range": data_range,

            "mean": mean,

            "median": median,

            "mode": mode_value,

            "variance": variance,

            "standard_deviation": std,

            "coefficient_variation": cv,

            "standard_error": standard_error,

            "mean_absolute_deviation": mad,

            "median_absolute_deviation": median_mad,

            "iqr": iqr,

            "skewness": skewness,

            "kurtosis": kurtosis,

            "entropy": shannon_entropy,

            "geometric_mean": geometric,

            "harmonic_mean": harmonic,

            "trimmed_mean": trimmed,

            "quantiles": quantiles,

            "percentiles": percentiles,

            "moments": moments

        }