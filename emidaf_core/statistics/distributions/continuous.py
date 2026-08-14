"""
=========================================================
EMIDAF Framework
Continuous Probability Distributions
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
# CONTINUOUS DISTRIBUTION
# ==========================================================

class ContinuousDistribution(

    BaseDistribution

):

    scipy_distribution=None

    name="Continuous Distribution"

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

        self.parameters=self.scipy_distribution.fit(

            data

        )

        loglikelihood=np.sum(

            self.scipy_distribution.logpdf(

                data,

                *self.parameters

            )

        )

        k=len(self.parameters)

        n=len(data)

        aic=2*k-2*loglikelihood

        bic=np.log(n)*k-2*loglikelihood

        return DistributionResult(

            distribution=self.name,

            parameters=self.parameters,

            log_likelihood=float(

                loglikelihood

            ),

            aic=float(aic),

            bic=float(bic)

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
# RANDOM SAMPLE
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

        mean,var,skew,kurt=(

            self.scipy_distribution.stats(

                *self.parameters,

                moments="mvsk"

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

                float(var),

            "skewness":

                float(skew),

            "kurtosis":

                float(kurt)

        }

    # ==========================================================
# NORMAL
# ==========================================================

class NormalDistribution(

    ContinuousDistribution

):

    name="Normal"

    scipy_distribution=stats.norm


# ==========================================================
# LOGNORMAL
# ==========================================================

class LogNormalDistribution(

    ContinuousDistribution

):

    name="LogNormal"

    scipy_distribution=stats.lognorm


# ==========================================================
# EXPONENTIAL
# ==========================================================

class ExponentialDistribution(

    ContinuousDistribution

):

    name="Exponential"

    scipy_distribution=stats.expon


# ==========================================================
# GAMMA
# ==========================================================

class GammaDistribution(

    ContinuousDistribution

):

    name="Gamma"

    scipy_distribution=stats.gamma

# ==========================================================
# WEIBULL
# ==========================================================

class WeibullDistribution(

    ContinuousDistribution

):

    name="Weibull"

    scipy_distribution=stats.weibull_min


# ==========================================================
# BETA
# ==========================================================

class BetaDistribution(

    ContinuousDistribution

):

    name="Beta"

    scipy_distribution=stats.beta

# ==========================================================
# UNIFORM
# ==========================================================

class UniformDistribution(

    ContinuousDistribution

):

    name="Uniform"

    scipy_distribution=stats.uniform

# ==========================================================
# STUDENT
# ==========================================================

class StudentDistribution(

    ContinuousDistribution

):

    name="Student"

    scipy_distribution=stats.t

# ==========================================================
# CHI SQUARE
# ==========================================================

class ChiSquareDistribution(

    ContinuousDistribution

):

    name="Chi Square"

    scipy_distribution=stats.chi2

# ==========================================================
# F
# ==========================================================

class FisherDistribution(

    ContinuousDistribution

):

    name="F Distribution"

    scipy_distribution=stats.f

# ==========================================================
# CAUCHY
# ==========================================================

class CauchyDistribution(

    ContinuousDistribution

):

    name="Cauchy"

    scipy_distribution=stats.cauchy

# ==========================================================
# LAPLACE
# ==========================================================

class LaplaceDistribution(

    ContinuousDistribution

):

    name="Laplace"

    scipy_distribution=stats.laplace

# ==========================================================
# LOGISTIC
# ==========================================================

class LogisticDistribution(

    ContinuousDistribution

):

    name="Logistic"

    scipy_distribution=stats.logistic

# ==========================================================
# GENERALIZED EXTREME VALUE
# ==========================================================

class GeneralizedExtremeValueDistribution(

    ContinuousDistribution

):

    name="Generalized Extreme Value"

    scipy_distribution=stats.genextreme

# ==========================================================
# PARETO
# ==========================================================

class ParetoDistribution(

    ContinuousDistribution

):

    name="Pareto"

    scipy_distribution=stats.pareto

# ==========================================================
# RAYLEIGH
# ==========================================================

class RayleighDistribution(

    ContinuousDistribution

):

    name="Rayleigh"

    scipy_distribution=stats.rayleigh

# ==========================================================
# SERVICE
# ==========================================================

class Continuous:

    Normal=NormalDistribution

    LogNormal=LogNormalDistribution

    Exponential=ExponentialDistribution

    Gamma=GammaDistribution

    Weibull=WeibullDistribution

    Beta=BetaDistribution

    Uniform=UniformDistribution

    Student=StudentDistribution

    ChiSquare=ChiSquareDistribution

    Fisher=FisherDistribution

    Cauchy=CauchyDistribution

    Laplace=LaplaceDistribution

    Logistic=LogisticDistribution

    GEV=GeneralizedExtremeValueDistribution

    Pareto=ParetoDistribution

    Rayleigh=RayleighDistribution