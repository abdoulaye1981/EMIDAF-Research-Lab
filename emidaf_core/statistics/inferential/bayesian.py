"""
=========================================================
EMIDAF Framework
Bayesian Inference
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
# BAYESIAN ENGINE
# ==========================================================

class BayesianInference:

    """
    Bayesian inference engine.
    """

    # ==========================================================
# POSTERIOR
# ==========================================================

    @staticmethod
    def posterior(
        prior,
        likelihood,
    ):
        posterior = (
            np.asarray(prior, dtype=float)
            * np.asarray(likelihood, dtype=float)
        )

        total = np.sum(posterior)

        if total == 0:
            raise ValueError(
                "La somme de la distribution posterior est nulle."
            )

        posterior = posterior / total

        return InferentialResult(
            test="Posterior Distribution",
            metadata={
                "posterior": posterior
            }
        )

    # ==========================================================
# POSTERIOR MEAN
# ==========================================================

    @staticmethod

    def posterior_mean(

        values,

        probabilities,

    ):

        value=np.sum(

            values*

            probabilities

        )

        return InferentialResult(

            test="Posterior Mean",

            statistic=float(

                value

            )

        )

    # ==========================================================
# POSTERIOR VARIANCE
# ==========================================================

    @staticmethod

    def posterior_variance(

        values,

        probabilities,

    ):

        mean=np.sum(

            values*

            probabilities

        )

        variance=np.sum(

            probabilities*

            (values-mean)**2

        )

        return InferentialResult(

            test="Posterior Variance",

            statistic=float(

                variance

            )

        )

    # ==========================================================
# MAP
# ==========================================================

    @staticmethod

    def map_estimate(

        values,

        posterior,

    ):

        index=np.argmax(

            posterior

        )

        return InferentialResult(

            test="MAP Estimate",

            statistic=float(

                values[index]

            )

        )

    # ==========================================================
# HPD
# ==========================================================

    @staticmethod

    def hpd_interval(

        samples,

        credibility=0.95,

    ):

        samples=np.sort(

            samples

        )

        n=len(samples)

        interval=int(

            credibility*n

        )

        widths=samples[

            interval:

        ]-samples[

            :n-interval

        ]

        idx=np.argmin(

            widths

        )

        lower=samples[idx]

        upper=samples[

            idx+interval

        ]

        return InferentialResult(

            test="HPD Interval",

            confidence_interval=(

                float(lower),

                float(upper)

            )

        )
    
    # ==========================================================
# POSTERIOR PREDICTIVE
# ==========================================================

    @staticmethod

    def posterior_predictive(

        distribution,

        parameters,

        size=1000,

    ):

        samples=distribution.rvs(

            *parameters,

            size=size

        )

        return InferentialResult(

            test="Posterior Predictive",

            metadata={

                "samples":

                    samples

            }

        )

    # ==========================================================
# CREDIBLE INTERVAL
# ==========================================================

    @staticmethod
    @staticmethod
    def credible_interval(
        samples,
        credibility=0.95,
    ):
        alpha = 1 - credibility

        interval = (
            np.percentile(
                samples,
                alpha / 2 * 100
            ),
            np.percentile(
                samples,
                (1 - alpha / 2) * 100
            )
        )

        return InferentialResult(
            test="Credible Interval",
            confidence_interval=(
                float(interval[0]),
                float(interval[1])
            )
        )

# SERVICE
# ==========================================================

Bayes=BayesianInference

    

    
