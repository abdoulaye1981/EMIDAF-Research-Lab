"""
=========================================================
EMIDAF Framework
Statistical Outlier Detection
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Détecteurs statistiques d'anomalies.

Contient

- ZScore
- ModifiedZScore
- IQR
- TukeyFence
- Percentile
- ThreeSigma
- HampelFilter

=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from scipy.stats import median_abs_deviation
from scipy.stats import zscore

from .base import BaseOutlierDetector


# ==========================================================
# Z SCORE
# ==========================================================

class ZScore(BaseOutlierDetector):

    name = "Z-Score"

    method_family = "statistical"

    score_type = "absolute_z_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        values,

        threshold: float = 3.0,

    ):

        values = cls.validate(values)

        scores = np.abs(

            zscore(

                values,

                nan_policy="omit"

            )

        )

        indices = values.index[

            scores > threshold

        ]

        return cls.build_result(

            values,

            indices,

            scores=scores,

            threshold=threshold

        )

    @classmethod
    def fit(cls, values, **kwargs):

        return cls.detect(values, **kwargs)

    @classmethod
    def fit_predict(cls, values, **kwargs):

        return cls.detect(values, **kwargs)


# ==========================================================
# MODIFIED Z SCORE
# ==========================================================

class ModifiedZScore(BaseOutlierDetector):

    name = "Modified Z-Score"

    method_family = "statistical"

    score_type = "absolute_modified_z_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(
        cls,
        values,
        threshold: float = 3.5,
    ):

        values = cls.validate(values)

        median = np.median(values)

        mad = median_abs_deviation(
            values,
            scale=1.0
        )

        if mad == 0:
            scores = np.zeros(
                len(values)
            )
        else:
            scores = (
                0.6745
                *
                np.abs(
                    values - median
                )
                /
                mad
            )

        indices = values.index[
            scores > threshold
        ]

        return cls.build_result(
            values,
            indices,
            scores=scores,
            threshold=threshold
        )

    fit = detect
    fit_predict = detect


# ==========================================================
# IQR
# ==========================================================

class IQR(BaseOutlierDetector):

    name = "IQR"

    method_family = "statistical"

    score_type = ""

    score_direction = "none"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        values,

        factor: float = 1.5,

    ):

        values = cls.validate(values)

        q1 = values.quantile(.25)

        q3 = values.quantile(.75)

        iqr = q3 - q1

        lower = q1 - factor * iqr

        upper = q3 + factor * iqr

        indices = values.index[

            (values < lower)

            |

            (values > upper)

        ]

        return cls.build_result(

            values,

            indices,

            threshold=factor,

            parameters={

                "lower_bound": lower,

                "upper_bound": upper,

                "iqr": iqr

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# TUKEY FENCE
# ==========================================================

class TukeyFence(BaseOutlierDetector):

    name = "Tukey Fence"

    method_family = "statistical"

    score_type = ""

    score_direction = "none"

    scaling_sensitive = False

    @classmethod
    def detect(
        cls,
        values,
        factor: float = 1.5,
    ):

        values = cls.validate(values)

        q1 = values.quantile(.25)
        q3 = values.quantile(.75)

        iqr = q3 - q1

        lower = q1 - factor * iqr
        upper = q3 + factor * iqr

        indices = values.index[
            (values < lower)
            |
            (values > upper)
        ]

        return cls.build_result(
            values,
            indices,
            threshold=factor,
            parameters={
                "lower_bound": lower,
                "upper_bound": upper,
                "iqr": iqr
            }
        )

    fit = detect
    fit_predict = detect


# ==========================================================
# PERCENTILE
# ==========================================================

class Percentile(BaseOutlierDetector):

    name = "Percentile"

    method_family = "statistical"

    score_type = ""

    score_direction = "none"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        values,

        lower=0.01,

        upper=0.99,

    ):

        values = cls.validate(values)

        q_low = values.quantile(lower)

        q_high = values.quantile(upper)

        indices = values.index[

            (values < q_low)

            |

            (values > q_high)

        ]

        return cls.build_result(

            values,

            indices,

            parameters={

                "lower": q_low,

                "upper": q_high

            }

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# THREE SIGMA
# ==========================================================

class ThreeSigma(BaseOutlierDetector):

    name = "Three Sigma"

    method_family = "statistical"

    score_type = "absolute_z_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(
        cls,
        values,
    ):

        values = cls.validate(values)

        threshold = 3.0

        scores = np.abs(
            zscore(
                values,
                nan_policy="omit"
            )
        )

        indices = values.index[
            scores > threshold
        ]

        return cls.build_result(
            values,
            indices,
            scores=scores,
            threshold=threshold
        )

    fit = detect
    fit_predict = detect


# ==========================================================
# HAMPEL FILTER
# ==========================================================

class HampelFilter(BaseOutlierDetector):

    name = "Hampel Filter"

    method_family = "statistical"

    score_type = "robust_deviation_score"

    score_direction = "higher_is_more_anomalous"

    scaling_sensitive = False

    @classmethod
    def detect(

        cls,

        values,

        threshold=3,

    ):

        values = cls.validate(values)

        median = np.median(values)

        mad = median_abs_deviation(

            values,

            scale="normal"

        )

        if mad == 0:

            # -------------------------------------------------
            # Degenerate robust-scale case.
            #
            # A zero MAD does not imply absence of outliers.
            # It commonly occurs when a majority of values are
            # identical. In that case, use the IQR as a robust
            # fallback instead of silently returning no outlier.
            # -------------------------------------------------

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            if iqr == 0:

                # No usable robust scale remains.
                # Values different from the median are given
                # an infinite anomaly score.
                scores = np.where(
                    values == median,
                    0.0,
                    np.inf,
                )

                indices = values.index[
                    np.isinf(scores)
                ]

            else:

                scores = (
                    np.abs(values - median)
                    / iqr
                )

                indices = values.index[
                    scores > threshold
                ]

        else:

            scores = (
                np.abs(values - median)
                / mad
            )

            indices = values.index[
                scores > threshold
            ]

        return cls.build_result(

            values,

            indices,

            scores=scores,

            threshold=threshold

        )

    fit = detect

    fit_predict = detect


# ==========================================================
# SERVICE
# ==========================================================

class StatisticalOutlierDetector:

    """
    Lance tous les détecteurs statistiques.
    """

    @staticmethod
    def compute(values):

        return {

            "zscore":

                ZScore.detect(values),

            "modified_zscore":

                ModifiedZScore.detect(values),

            "iqr":

                IQR.detect(values),

            "tukey":

                TukeyFence.detect(values),

            "percentile":

                Percentile.detect(values),

            "three_sigma":

                ThreeSigma.detect(values),

            "hampel":

                HampelFilter.detect(values)

        }
