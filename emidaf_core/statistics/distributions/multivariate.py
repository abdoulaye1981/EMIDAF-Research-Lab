"""
=========================================================
EMIDAF Framework
Multivariate Probability Distributions
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
# MULTIVARIATE DISTRIBUTION
# ==========================================================

class MultivariateDistribution(

    BaseDistribution

):

    scipy_distribution=None

    name="Multivariate Distribution"

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

        data=np.asarray(data)

        mean=np.mean(

            data,

            axis=0

        )

        covariance=np.cov(

            data,

            rowvar=False

        )

        self.parameters=(

            mean,

            covariance

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

        if hasattr(

            self.scipy_distribution,

            "cdf"

        ):

            return self.scipy_distribution.cdf(

                x,

                *self.parameters

            )

        raise NotImplementedError(

            "CDF indisponible."

        )

    # ==========================================================
# RANDOM SAMPLE
# ==========================================================


    # ==========================================================
    # PPF
    # ==========================================================

    def ppf(
        self,
        q,
    ):
        """
        Quantile function.

        A scalar PPF is generally not defined
        for multivariate distributions.
        """
        raise NotImplementedError(
            f"PPF is not defined for {self.name}."
        )

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

        return {

            "distribution":

                self.name,

            "mean":

                self.parameters[0],

            "covariance":

                self.parameters[1]

        }

# ==========================================================
# MULTIVARIATE NORMAL
# ==========================================================

class MultivariateNormalDistribution(

    MultivariateDistribution

):

    name="Multivariate Normal"

    scipy_distribution=stats.multivariate_normal

# ==========================================================
# DIRICHLET
# ==========================================================

class DirichletDistribution(

    MultivariateDistribution

):

    name="Dirichlet"

    scipy_distribution=stats.dirichlet

    def fit(

        self,

        data,

    ):

        alpha=np.mean(

            data,

            axis=0

        )

        self.parameters=(

            alpha,

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

    # ==========================================================
# WISHART
# ==========================================================

class WishartDistribution(

    MultivariateDistribution

):

    name="Wishart"

    scipy_distribution=stats.wishart

    def fit(

        self,

        data,

    ):

        covariance=np.cov(

            data,

            rowvar=False

        )

        df=len(data)

        self.parameters=(

            df,

            covariance

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )
    
# ==========================================================
# INVERSE WISHART
# ==========================================================

class InverseWishartDistribution(

    MultivariateDistribution

):

    name="Inverse Wishart"

    scipy_distribution=stats.invwishart

    def fit(

        self,

        data,

    ):

        covariance=np.cov(

            data,

            rowvar=False

        )

        df=len(data)

        self.parameters=(

            df,

            covariance

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

# ==========================================================
# FROZEN MULTIVARIATE NORMAL
# ==========================================================

class FrozenMultivariateNormal(

    MultivariateDistribution

):

    name="Frozen Multivariate Normal"

    scipy_distribution=stats.multivariate_normal

    def fit(

        self,

        data,

    ):

        mean=np.mean(

            data,

            axis=0

        )

        covariance=np.cov(

            data,

            rowvar=False

        )

        frozen=stats.multivariate_normal(

            mean=mean,

            cov=covariance

        )

        self.parameters=(

            frozen,

        )

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters

        )

    def pdf(

        self,

        x,

    ):

        return self.parameters[0].pdf(

            x

        )

    def rvs(

        self,

        size,

    ):

        return self.parameters[0].rvs(

            size=size

        )

# ==========================================================
# SERVICE
# ==========================================================

class Multivariate:

    Normal=MultivariateNormalDistribution

    Dirichlet=DirichletDistribution

    Wishart=WishartDistribution

    InverseWishart=InverseWishartDistribution

    FrozenNormal=FrozenMultivariateNormal