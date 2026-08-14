"""
=========================================================
EMIDAF Framework
Distribution Fitting Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

import pandas as pd

from scipy import stats

from .base import DistributionResult

from .continuous import *

from .discrete import *

# ==========================================================
# DISTRIBUTION FITTING
# ==========================================================

class DistributionFitter:

    """
    Automatic distribution fitting.
    """

    def __init__(

        self,

        distributions=None,

    ):

        if distributions is None:

            distributions=[

                NormalDistribution,

                LogNormalDistribution,

                GammaDistribution,

                WeibullDistribution,

                ExponentialDistribution,

                BetaDistribution,

                UniformDistribution,

                LogisticDistribution,

                LaplaceDistribution,

                CauchyDistribution,

                RayleighDistribution,

                ParetoDistribution,

                GeneralizedExtremeValueDistribution

            ]

        self.distributions=distributions

    # ==========================================================
# SINGLE FIT
# ==========================================================

    def fit_distribution(

        self,

        distribution,

        data,

    ):

        model=distribution()

        result=model.fit(

            data

        )

        return model,result


    # ==========================================================
# FIT ALL
# ==========================================================

    def fit_all(

        self,

        data,

    ):

        results=[]

        for distribution in self.distributions:

            try:

                model,result=(

                    self.fit_distribution(

                        distribution,

                        data

                    )

                )

                results.append(

                    (

                        model,

                        result

                    )

                )

            except Exception:

                continue

        return results


    # ==========================================================
# RANKING
# ==========================================================

    def ranking(

        self,

        data,

        criterion="aic",

    ):

        fitted=self.fit_all(

            data

        )

        rows=[]

        for model,result in fitted:

            rows.append(

                {

                    "Distribution":

                        result.distribution,

                    "AIC":

                        result.aic,

                    "BIC":

                        result.bic,

                    "LogLikelihood":

                        result.log_likelihood,

                    "Model":

                        model

                }

            )

        table=pd.DataFrame(

            rows

        )

        table=table.sort_values(

            criterion.upper()

        )

        return table

    # ==========================================================
# BEST
# ==========================================================

    def best(

        self,

        data,

        criterion="aic",

    ):

        ranking=self.ranking(

            data,

            criterion

        )

        return ranking.iloc[0]

    # ==========================================================
# TOP N
# ==========================================================

    def top(

        self,

        data,

        n=5,

        criterion="aic",

    ):

        ranking=self.ranking(

            data,

            criterion

        )

        return ranking.head(

            n

        )


# ==========================================================
# SERVICE
# ==========================================================

class Fitting:

    @staticmethod

    def fit_best(

        data,

        criterion="aic",

    ):

        engine=DistributionFitter()

        return engine.best(

            data,

            criterion

        )

    @staticmethod

    def ranking(

        data,

        criterion="aic",

    ):

        engine=DistributionFitter()

        return engine.ranking(

            data,

            criterion

        )

    @staticmethod

    def top(

        data,

        n=5,

        criterion="aic",

    ):

        engine=DistributionFitter()

        return engine.top(

            data,

            n,

            criterion

        )