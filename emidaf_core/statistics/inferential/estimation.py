"""
=========================================================
EMIDAF Framework
Statistical Estimation
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import optimize

from scipy import stats

from .base import InferentialResult

# ==========================================================
# ESTIMATION
# ==========================================================

class Estimation:
    """
    Méthodes générales d'estimation.
    """

    # ==========================================================
# SAMPLE MEAN
# ==========================================================

    @staticmethod

    def mean(

        x,

    ):

        return InferentialResult(

            test="Mean Estimator",

            statistic=float(

                np.mean(x)

            )

        )

    # ==========================================================
# SAMPLE MEAN
# ==========================================================

    @staticmethod

    def mean(

        x,

    ):

        return InferentialResult(

            test="Mean Estimator",

            statistic=float(

                np.mean(x)

            )

        )

    # ==========================================================
# VARIANCE
# ==========================================================

    @staticmethod

    def variance(

        x,

        unbiased=True,

    ):

        ddof=1 if unbiased else 0

        return InferentialResult(

            test="Variance Estimator",

            statistic=float(

                np.var(

                    x,

                    ddof=ddof

                )

            )

        )
    # ==========================================================
# METHOD OF MOMENTS
# ==========================================================

    @staticmethod

    def method_of_moments(

        data,

    ):

        mean=np.mean(data)

        variance=np.var(

            data,

            ddof=1

        )

        return InferentialResult(

            test="Method of Moments",

            metadata={

                "mean":mean,

                "variance":variance

            }

        )

    # ==========================================================
# BOOTSTRAP
# ==========================================================

    @staticmethod

    def bootstrap(

        data,

        estimator=np.mean,

        n_bootstrap=5000,

    ):

        estimates=[]

        n=len(data)

        for _ in range(

            n_bootstrap

        ):

            sample=np.random.choice(

                data,

                n,

                replace=True

            )

            estimates.append(

                estimator(

                    sample

                )

            )

        return InferentialResult(

            test="Bootstrap",

            statistic=float(

                np.mean(

                    estimates

                )

            ),

            metadata={

                "bootstrap_std":

                    float(

                        np.std(

                            estimates,

                            ddof=1

                        )

                    ),

                "bootstrap_distribution":

                    estimates

            }

        )

    # ==========================================================
# JACKKNIFE
# ==========================================================

    @staticmethod

    def jackknife(

        data,

        estimator=np.mean,

    ):

        estimates=[]

        n=len(data)

        for i in range(n):

            sample=np.delete(

                data,

                i

            )

            estimates.append(

                estimator(

                    sample

                )

            )

        return InferentialResult(

            test="Jackknife",

            statistic=float(

                np.mean(

                    estimates

                )

            ),

            metadata={

                "jackknife_std":

                    float(

                        np.std(

                            estimates,

                            ddof=1

                        )

                    )

            }

        )

    # ==========================================================
# ROBUST
# ==========================================================

    @staticmethod

    def robust_location(

        data,

    ):

        return InferentialResult(

            test="Robust Location",

            statistic=float(

                np.median(

                    data

                )

            )

        )
    

    # ==========================================================
# ROBUST SCALE
# ==========================================================

    @staticmethod

    def robust_scale(

        data,

    ):

        median=np.median(

            data

        )

        mad=np.median(

            np.abs(

                data-median

            )

        )

        return InferentialResult(

            test="Robust Scale",

            statistic=float(

                1.4826*mad

            )

        )

    # ==========================================================
# MAP ESTIMATOR
# ==========================================================

    @staticmethod

    def map_estimator(

        negative_log_posterior,

        initial_guess,

    ):

        result=optimize.minimize(

            negative_log_posterior,

            initial_guess

        )

        return InferentialResult(

            test="MAP Estimator",

            metadata={

                "estimate":

                    result.x,

                "success":

                    result.success

            }

        )

    # ==========================================================
# BAYES ESTIMATOR
# ==========================================================

    @staticmethod

    def posterior_mean(

        samples,

    ):

        return InferentialResult(

            test="Posterior Mean",

            statistic=float(

                np.mean(

                    samples

                )

            )

        )
# ==========================================================
# SERVICE
# ==========================================================

Estimator=Estimation