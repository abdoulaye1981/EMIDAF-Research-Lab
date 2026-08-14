"""
=========================================================
EMIDAF Framework
Truncated Probability Distributions
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    BaseDistribution,

    DistributionResult

)

# ==========================================================
# TRUNCATED DISTRIBUTION
# ==========================================================

class TruncatedDistribution(

    BaseDistribution

):

    scipy_distribution=None

    name="Truncated Distribution"

    def __init__(

        self,

        lower,

        upper,

    ):

        self.lower=lower

        self.upper=upper

        self.parameters=None

    # ==========================================================
# FIT
# ==========================================================

    def fit(

        self,

        data,

    ):

        mean=np.mean(data)

        std=np.std(

            data,

            ddof=1

        )

        a=(

            self.lower-mean

        )/std

        b=(

            self.upper-mean

        )/std

        self.parameters=(

            a,

            b,

            mean,

            std

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

    # ==========================================================
# PDF
# ==========================================================

    def pdf(

        self,

        x,

    ):

        return self.scipy_distribution.pdf(

            x,

            *self.parameters

        )

    # ==========================================================
# CDF
# ==========================================================

    def cdf(

        self,

        x,

    ):

        return self.scipy_distribution.cdf(

            x,

            *self.parameters

        )

    # ==========================================================
# PPF
# ==========================================================

    def ppf(

        self,

        q,

    ):

        return self.scipy_distribution.ppf(

            q,

            *self.parameters

        )

    # ==========================================================
# RANDOM
# ==========================================================

    def rvs(

        self,

        size,

    ):

        return self.scipy_distribution.rvs(

            *self.parameters,

            size=size

        )

    # ==========================================================
# SUMMARY
# ==========================================================

    def summary(

        self,

    ):

        mean,var=(

            self.scipy_distribution.stats(

                *self.parameters,

                moments="mv"

            )

        )

        return {

            "distribution":

                self.name,

            "lower":

                self.lower,

            "upper":

                self.upper,

            "mean":

                float(mean),

            "variance":

                float(var)

        }

    # ==========================================================
# TRUNCATED NORMAL
# ==========================================================

class TruncatedNormal(

    TruncatedDistribution

):

    name="Truncated Normal"

    scipy_distribution=stats.truncnorm

# ==========================================================
# TRUNCATED EXPONENTIAL
# ==========================================================

class TruncatedExponential(

    TruncatedDistribution

):

    name="Truncated Exponential"

    scipy_distribution=stats.truncexpon

    def fit(

        self,

        data,

    ):

        scale=np.mean(data)

        b=self.upper/scale

        self.parameters=(

            b,

            0,

            scale

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

# ==========================================================
# TRUNCATED PARETO
# ==========================================================

class TruncatedPareto(

    TruncatedDistribution

):

    name="Truncated Pareto"

    scipy_distribution=stats.truncpareto

    def fit(

        self,

        data,

    ):

        shape=2.0

        self.parameters=(

            shape,

            self.lower,

            self.upper

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

# ==========================================================
# SERVICE
# ==========================================================

class Truncated:

    Normal=TruncatedNormal

    Exponential=TruncatedExponential

    Pareto=TruncatedPareto