"""
=========================================================
EMIDAF Framework
Discrete Probability Distributions
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
# DISCRETE DISTRIBUTION
# ==========================================================

class DiscreteDistribution(

    BaseDistribution

):

    scipy_distribution=None

    name="Discrete Distribution"

    def __init__(

        self,

    ):

        self.parameters=None

# ==========================================================
# FIT
# ==========================================================

    def fit(

        self,

        data,

    ):

        if hasattr(

            self.scipy_distribution,

            "fit"

        ):

            self.parameters=(

                self.scipy_distribution.fit(

                    data

                )

            )

        else:

            self.parameters=self.estimate(

                data

            )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

    # ==========================================================
# PARAMETER ESTIMATION
# ==========================================================

    def estimate(

        self,

        data,

    ):

        raise NotImplementedError

    # ==========================================================
# PMF
# ==========================================================

    def pdf(

        self,

        x,

    ):

        return self.scipy_distribution.pmf(

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
# QUANTILE
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

            "parameters":

                self.parameters,

            "mean":

                float(mean),

            "variance":

                float(var)

        }


    # ==========================================================
# BERNOULLI
# ==========================================================

class BernoulliDistribution(

    DiscreteDistribution

):

    name="Bernoulli"

    scipy_distribution=stats.bernoulli

    def estimate(

        self,

        data,

    ):

        return (

            np.mean(data),

        )

# ==========================================================
# BINOMIAL
# ==========================================================

class BinomialDistribution(

    DiscreteDistribution

):

    name="Binomial"

    scipy_distribution=stats.binom

    def estimate(

        self,

        data,

    ):

        n=int(

            np.max(data)

        )

        p=np.mean(data)/n

        return (

            n,

            p

        )

# ==========================================================
# POISSON
# ==========================================================

class PoissonDistribution(

    DiscreteDistribution

):

    name="Poisson"

    scipy_distribution=stats.poisson

    def estimate(

        self,

        data,

    ):

        return (

            np.mean(data),

        )

# ==========================================================
# GEOMETRIC
# ==========================================================

class GeometricDistribution(

    DiscreteDistribution

):

    name="Geometric"

    scipy_distribution=stats.geom

    def estimate(

        self,

        data,

    ):

        return (

            1/np.mean(data),

        )

# ==========================================================
# NEGATIVE BINOMIAL
# ==========================================================

class NegativeBinomialDistribution(

    DiscreteDistribution

):

    name="Negative Binomial"

    scipy_distribution=stats.nbinom

    def estimate(

        self,

        data,

    ):

        mean=np.mean(data)

        var=np.var(

            data,

            ddof=1

        )

        p=mean/var

        r=mean*p/(1-p)

        return (

            r,

            p

        )

# ==========================================================
# HYPERGEOMETRIC
# ==========================================================

class HyperGeometricDistribution(

    DiscreteDistribution

):

    name="HyperGeometric"

    scipy_distribution=stats.hypergeom

    def estimate(

        self,

        data,

    ):

        raise NotImplementedError(

            "Population parameters required."

        )

# ==========================================================
# MULTINOMIAL
# ==========================================================

class MultinomialDistribution(

    DiscreteDistribution

):

    name="Multinomial"

    scipy_distribution=stats.multinomial

    def estimate(

        self,

        data,

    ):

        counts=np.sum(

            data,

            axis=0

        )

        probabilities=(

            counts/

            counts.sum()

        )

        n=int(

            np.sum(

                data[0]

            )

        )

        return (

            n,

            probabilities

        )

# ==========================================================
# ZIPF
# ==========================================================

class ZipfDistribution(

    DiscreteDistribution

):

    name="Zipf"

    scipy_distribution=stats.zipf

    def estimate(

        self,

        data,

    ):

        return (

            2.0,

        )

# ==========================================================
# PLANCK
# ==========================================================

class PlanckDistribution(

    DiscreteDistribution

):

    name="Planck"

    scipy_distribution=stats.planck

    def estimate(

        self,

        data,

    ):

        return (

            1.0,

        )

# ==========================================================
# SERVICE
# ==========================================================

class Discrete:

    Bernoulli=BernoulliDistribution

    Binomial=BinomialDistribution

    Poisson=PoissonDistribution

    Geometric=GeometricDistribution

    NegativeBinomial=NegativeBinomialDistribution

    HyperGeometric=HyperGeometricDistribution

    Multinomial=MultinomialDistribution

    Zipf=ZipfDistribution

    Planck=PlanckDistribution