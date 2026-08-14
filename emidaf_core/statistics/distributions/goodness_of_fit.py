"""
=========================================================
EMIDAF Framework
Goodness of Fit Tests
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from statsmodels.stats.diagnostic import lilliefors

from .base import DistributionResult

# ==========================================================
# GOODNESS OF FIT
# ==========================================================

class GoodnessOfFit:

    """
    Goodness-of-fit engine.
    """

    # ==========================================================
# KOLMOGOROV-SMIRNOV
# ==========================================================

    @staticmethod

    def kolmogorov_smirnov(

        data,

        distribution,

        parameters,

    ):

        statistic,p=stats.kstest(

            data,

            distribution,

            args=parameters

        )

        return DistributionResult(

            distribution=distribution,

            statistic=float(statistic),

            p_value=float(p)

        )

    # ==========================================================
# ANDERSON-DARLING
# ==========================================================

    @staticmethod

    def anderson(

        data,

        distribution="norm",

    ):

        result=stats.anderson(

            data,

            dist=distribution

        )

        return DistributionResult(

            distribution=distribution,

            statistic=float(

                result.statistic

            ),

            metadata={

                "critical_values":

                    result.critical_values,

                "significance":

                    result.significance_level

            }

        )

    # ==========================================================
# SHAPIRO
# ==========================================================

    @staticmethod

    def shapiro(

        data,

    ):

        statistic,p=stats.shapiro(

            data

        )

        return DistributionResult(

            distribution="Normal",

            statistic=float(statistic),

            p_value=float(p)

        )

    # ==========================================================
# JARQUE-BERA
# ==========================================================

    @staticmethod

    def jarque_bera(

        data,

    ):

        statistic,p=stats.jarque_bera(

            data

        )

        return DistributionResult(

            distribution="Normal",

            statistic=float(statistic),

            p_value=float(p)

        )

    # ==========================================================
# D'AGOSTINO
# ==========================================================

    @staticmethod

    def dagostino(

        data,

    ):

        statistic,p=stats.normaltest(

            data

        )

        return DistributionResult(

            distribution="Normal",

            statistic=float(statistic),

            p_value=float(p)

        )

    # ==========================================================
# CRAMER-VON MISES
# ==========================================================

    @staticmethod

    def cramervonmises(

        data,

        distribution,

        parameters,

    ):

        result=stats.cramervonmises(

            data,

            distribution,

            args=parameters

        )

        return DistributionResult(

            distribution=distribution,

            statistic=float(

                result.statistic

            ),

            p_value=float(

                result.pvalue

            )

        )

    # ==========================================================
# LILLIEFORS
# ==========================================================

    @staticmethod

    def lilliefors(

        data,

    ):

        statistic,p=lilliefors(

            data

        )

        return DistributionResult(

            distribution="Normal",

            statistic=float(statistic),

            p_value=float(p)

        )

    # ==========================================================
# CHI SQUARE
# ==========================================================

    @staticmethod

    def chi_square(

        observed,

        expected,

    ):

        statistic,p=stats.chisquare(

            observed,

            expected

        )

        return DistributionResult(

            distribution="Chi Square",

            statistic=float(statistic),

            p_value=float(p)

        )


# ==========================================================
# SERVICE
# ==========================================================

class GOF:

    ks=GoodnessOfFit.kolmogorov_smirnov

    anderson=GoodnessOfFit.anderson

    shapiro=GoodnessOfFit.shapiro

    jarque_bera=GoodnessOfFit.jarque_bera

    dagostino=GoodnessOfFit.dagostino

    cramervonmises=GoodnessOfFit.cramervonmises

    lilliefors=GoodnessOfFit.lilliefors

    chi_square=GoodnessOfFit.chi_square