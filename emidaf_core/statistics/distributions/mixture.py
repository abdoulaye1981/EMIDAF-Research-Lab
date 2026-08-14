"""
=========================================================
EMIDAF Framework
Mixture Probability Distributions
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from sklearn.mixture import GaussianMixture

from .base import (

    BaseDistribution,

    DistributionResult

)

# ==========================================================
# MIXTURE DISTRIBUTION
# ==========================================================

class MixtureDistribution(

    BaseDistribution

):

    name="Mixture Distribution"

    def __init__(

        self,

        n_components=2,

        random_state=None,

    ):

        self.n_components=n_components

        self.random_state=random_state

        self.model=None

    # ==========================================================
# FIT
# ==========================================================

    def fit(

        self,

        data,

    ):

        data=np.asarray(data).reshape(

            -1,

            1

        )

        self.model=GaussianMixture(

            n_components=self.n_components,

            random_state=self.random_state

        )

        self.model.fit(

            data

        )

        return DistributionResult(

            distribution=self.name,

            parameters={

                "weights":

                    self.model.weights_,

                "means":

                    self.model.means_,

                "covariances":

                    self.model.covariances_

            },

            log_likelihood=float(

                self.model.score(

                    data

                )*len(data)

            ),

            aic=float(

                self.model.aic(

                    data

                )

            ),

            bic=float(

                self.model.bic(

                    data

                )

            )

        )

    # ==========================================================
# PDF
# ==========================================================

    def pdf(

        self,

        x,

    ):

        x=np.asarray(x).reshape(

            -1,

            1

        )

        return np.exp(

            self.model.score_samples(

                x

            )

        )

    # ==========================================================
# LOG PDF
# ==========================================================

    def logpdf(

        self,

        x,

    ):

        x=np.asarray(x).reshape(

            -1,

            1

        )

        return self.model.score_samples(

            x

        )

    # ==========================================================
# POSTERIOR PROBABILITIES
# ==========================================================

    def posterior(

        self,

        x,

    ):

        x=np.asarray(x).reshape(

            -1,

            1

        )

        return self.model.predict_proba(

            x

        )

    # ==========================================================
# PREDICT COMPONENT
# ==========================================================

    def predict(

        self,

        x,

    ):

        x=np.asarray(x).reshape(

            -1,

            1

        )

        return self.model.predict(

            x

        )

    # ==========================================================
# RANDOM SAMPLE
# ==========================================================

    def rvs(

        self,

        size,

    ):

        samples,_=self.model.sample(

            size

        )

        return samples.ravel()

    # ==========================================================
# SUMMARY
# ==========================================================

    def summary(

        self,

    ):

        return {

            "distribution":

                self.name,

            "components":

                self.n_components,

            "weights":

                self.model.weights_,

            "means":

                self.model.means_.ravel(),

            "covariances":

                self.model.covariances_

        }

# ==========================================================
# GAUSSIAN MIXTURE
# ==========================================================

class GaussianMixtureDistribution(

    MixtureDistribution

):

    name="Gaussian Mixture"


# ==========================================================
# BAYESIAN GAUSSIAN MIXTURE
# ==========================================================

from sklearn.mixture import BayesianGaussianMixture

class BayesianGaussianMixtureDistribution(

    MixtureDistribution

):

    name="Bayesian Gaussian Mixture"

    def fit(

        self,

        data,

    ):

        data=np.asarray(data).reshape(

            -1,

            1

        )

        self.model=BayesianGaussianMixture(

            n_components=self.n_components,

            random_state=self.random_state

        )

        self.model.fit(

            data

        )

        return DistributionResult(

            distribution=self.name,

            parameters={

                "weights":

                    self.model.weights_,

                "means":

                    self.model.means_,

                "covariances":

                    self.model.covariances_

            }

        )

# ==========================================================
# SERVICE
# ==========================================================

class Mixture:

    Gaussian=GaussianMixtureDistribution

    BayesianGaussian=BayesianGaussianMixtureDistribution