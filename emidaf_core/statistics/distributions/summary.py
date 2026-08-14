"""
=========================================================
EMIDAF Framework
Distribution Summary Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from .fitting import Fitting

from .goodness_of_fit import GOF

# ==========================================================
# SUMMARY ENGINE
# ==========================================================

class DistributionSummary:

    """
    Automatic distribution analysis.
    """

    def __init__(

        self,

        data,

    ):

        self.data=np.asarray(

            data

        )

    # ==========================================================
# BEST DISTRIBUTION
# ==========================================================

    def best_distribution(

        self,

        criterion="aic",

    ):

        return Fitting.fit_best(

            self.data,

            criterion

        )

    # ==========================================================
# RANKING
# ==========================================================

    def ranking(

        self,

        criterion="aic",

    ):

        return Fitting.ranking(

            self.data,

            criterion

        )

    # ==========================================================
# TOP
# ==========================================================

    def top(

        self,

        n=5,

        criterion="aic",

    ):

        return Fitting.top(

            self.data,

            n,

            criterion

        )
    
    # ==========================================================
# GOODNESS OF FIT
# ==========================================================

    def goodness_of_fit(

        self,

    ):

        best=self.best_distribution()

        model=best["Model"]

        fit=model.fit(

            self.data

        )

        return {

            "Kolmogorov-Smirnov":

                GOF.ks(

                    self.data,

                    model.scipy_distribution.name,

                    fit.parameters

                ),

            "Shapiro":

                GOF.shapiro(

                    self.data

                ),

            "Jarque-Bera":

                GOF.jarque_bera(

                    self.data

                ),

            "D'Agostino":

                GOF.dagostino(

                    self.data

                )
        }

    # ==========================================================
# SUMMARY
# ==========================================================

    def summary(

        self,

    ):

        best=self.best_distribution()

        ranking=self.ranking()

        gof=self.goodness_of_fit()

        return {

            "best_distribution":

                best,

            "ranking":

                ranking,

            "goodness_of_fit":

                gof

        }

    # ==========================================================
# SERVICE
# ==========================================================

class DistributionAnalysis:

    @staticmethod

    def analyze(

        data,

    ):

        engine=DistributionSummary(

            data

        )

        return engine.summary()