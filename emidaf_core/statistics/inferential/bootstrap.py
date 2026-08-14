"""
=========================================================
EMIDAF Framework
Bootstrap Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    InferentialResult

)

# ==========================================================
# ENGINE
# ==========================================================

class BootstrapEngine:

    """
    Generic Bootstrap Engine.
    """

    def __init__(

        self,

        estimator=np.mean,

        n_resamples=5000,

        confidence=0.95,

        random_state=None,

    ):

        self.estimator=estimator

        self.n_resamples=n_resamples

        self.confidence=confidence

        self.random_state=random_state

        self.rng=np.random.default_rng(

            random_state

        )

    # ==========================================================
# RESAMPLE
# ==========================================================

    def resample(

        self,

        data,

    ):

        n=len(data)

        return self.rng.choice(

            data,

            n,

            replace=True

        )

    # ==========================================================
# DISTRIBUTION
# ==========================================================

    def distribution(

        self,

        data,

    ):

        estimates=[]

        for _ in range(

            self.n_resamples

        ):

            sample=self.resample(

                data

            )

            estimates.append(

                self.estimator(

                    sample

                )

            )

        return np.asarray(

            estimates

        )

    # ==========================================================
# DISTRIBUTION
# ==========================================================

    def distribution(

        self,

        data,

    ):

        estimates=[]

        for _ in range(

            self.n_resamples

        ):

            sample=self.resample(

                data

            )

            estimates.append(

                self.estimator(

                    sample

                )

            )

        return np.asarray(

            estimates

        )

    # ==========================================================
# BASIC CI
# ==========================================================

    def basic_interval(

        self,

        original,

        estimates,

    ):

        alpha=1-self.confidence

        l=np.percentile(

            estimates,

            (1-alpha/2)*100

        )

        u=np.percentile(

            estimates,

            alpha/2*100

        )

        return (

            float(

                2*original-l

            ),

            float(

                2*original-u

            )

        )
    
    # ==========================================================
# BIAS
# ==========================================================

    def bias(

        self,

        original,

        estimates,

    ):

        return float(

            np.mean(

                estimates

            )-original

        )

    # ==========================================================
# BIAS
# ==========================================================

    def bias(

        self,

        original,

        estimates,

    ):

        return float(

            np.mean(

                estimates

            )-original

        )

    # ==========================================================
# COMPUTE
# ==========================================================

    def compute(

        self,

        data,

    ):

        original=self.estimator(

            data

        )

        estimates=self.distribution(

            data

        )

        return InferentialResult(

            test="Bootstrap",

            statistic=float(original),

            confidence_interval=

                self.percentile_interval(

                    estimates

                ),

            metadata={

                "bootstrap_distribution":

                    estimates,

                "standard_error":

                    self.standard_error(

                        estimates

                    ),

                "bias":

                    self.bias(

                        original,

                        estimates

                    ),

                "confidence":

                    self.confidence,

                "resamples":

                    self.n_resamples

            }

        )

# ==========================================================
# TWO SAMPLE
# ==========================================================

class BootstrapDifference:

    """
    Bootstrap difference
    between two samples.
    """

    def __init__(

        self,

        estimator=np.mean,

        n_resamples=5000,

    ):

        self.estimator=estimator

        self.n_resamples=n_resamples

    def compute(

        self,

        x,

        y,

    ):

        rng=np.random.default_rng()

        nx=len(x)

        ny=len(y)

        estimates=[]

        for _ in range(

            self.n_resamples

        ):

            sx=rng.choice(

                x,

                nx,

                replace=True

            )

            sy=rng.choice(

                y,

                ny,

                replace=True

            )

            estimates.append(

                self.estimator(

                    sx

                )

                -

                self.estimator(

                    sy

                )

            )

        estimates=np.asarray(

            estimates

        )

        return InferentialResult(

            test="Bootstrap Difference",

            statistic=float(

                np.mean(

                    estimates

                )

            ),

            confidence_interval=(

                float(

                    np.percentile(

                        estimates,

                        2.5

                    )

                ),

                float(

                    np.percentile(

                        estimates,

                        97.5

                    )

                )

            )

        )

# ==========================================================
# CORRELATION
# ==========================================================

class BootstrapCorrelation:

    """
    Bootstrap Pearson correlation.
    """

    def __init__(
        self,
        n_resamples=5000,
    ):

        self.n_resamples = n_resamples

    def compute(
        self,
        x,
        y,
    ):

        x = np.asarray(x)
        y = np.asarray(y)

        if len(x) != len(y):
            raise ValueError(
                "x and y must have the same length."
            )

        if len(x) < 3:
            raise ValueError(
                "At least 3 observations are required."
            )

        rng = np.random.default_rng()

        n = len(x)

        estimates = []

        for _ in range(
            self.n_resamples
        ):

            idx = rng.choice(
                n,
                n,
                replace=True
            )

            sx = x[idx]
            sy = y[idx]

            if (
                np.std(sx, ddof=1) == 0
                or
                np.std(sy, ddof=1) == 0
            ):
                continue

            correlation = np.corrcoef(
                sx,
                sy
            )[0, 1]

            if np.isfinite(correlation):

                estimates.append(
                    correlation
                )

        estimates = np.asarray(
            estimates
        )

        if len(estimates) == 0:
            raise ValueError(
                "No valid bootstrap correlations were obtained."
            )

        return InferentialResult(

            test="Bootstrap Correlation",

            statistic=float(
                np.mean(estimates)
            ),

            confidence_interval=(

                float(
                    np.percentile(
                        estimates,
                        2.5
                    )
                ),

                float(
                    np.percentile(
                        estimates,
                        97.5
                    )
                )

            )
        )
  
           
# ==========================================================
# SERVICE
# ==========================================================

class Bootstrap:

    Engine=BootstrapEngine

    Difference=BootstrapDifference

    Correlation=BootstrapCorrelation

