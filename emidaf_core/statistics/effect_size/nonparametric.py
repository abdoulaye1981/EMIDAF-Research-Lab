"""
=========================================================
EMIDAF Framework
Effect Sizes for Nonparametric Statistics
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from scipy import stats

from .base import (

    BaseEffectSize,

    EffectSizeResult

)

# ==========================================================
# NONPARAMETRIC EFFECT SIZE
# ==========================================================

class NonParametricEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for
    nonparametric statistics.
    """

    name="Non Parametric Effect Size"

    # ==========================================================
# RANK BISERIAL
# ==========================================================

    @staticmethod

    def rank_biserial(

        u,

        n1,

        n2,

    ):

        r=(

            2*u

            /

            (n1*n2)

        )-1

        return EffectSizeResult(

            name="Rank Biserial Correlation",

            statistic=float(r)

        )

    # ==========================================================
# CLIFF DELTA
# ==========================================================

    @staticmethod

    def cliffs_delta(

        x,

        y,

    ):

        x=np.asarray(x)

        y=np.asarray(y)

        greater=0

        lower=0

        for xi in x:

            greater+=np.sum(

                xi>y

            )

            lower+=np.sum(

                xi<y

            )

        delta=(

            greater-lower

        )/(

            len(x)*len(y)

        )

        return EffectSizeResult(

            name="Cliff Delta",

            statistic=float(delta)

        )

    # ==========================================================
# VARGHA DELANEY
# ==========================================================

    @staticmethod

    def vargha_delaney(

        u,

        n1,

        n2,

    ):

        a=u/(

            n1*n2

        )

        return EffectSizeResult(

            name="Vargha Delaney A",

            statistic=float(a)

        )

    # ==========================================================
# COMMON LANGUAGE EFFECT SIZE
# ==========================================================

    @staticmethod

    def common_language(

        x,

        y,

    ):

        x=np.asarray(x)

        y=np.asarray(y)

        wins=0

        for xi in x:

            wins+=np.sum(

                xi>y

            )

        cles=wins/(

            len(x)*len(y)

        )

        return EffectSizeResult(

            name="Common Language Effect Size",

            statistic=float(cles)

        )

    # ==========================================================
# ROSENTHAL R
# ==========================================================

    @staticmethod

    def rosenthal_r(

        z,

        n,

    ):

        r=z/np.sqrt(

            n

        )

        return EffectSizeResult(

            name="Rosenthal r",

            statistic=float(r)

        )

    # ==========================================================
# KENDALL W
# ==========================================================

    @staticmethod

    def kendall_w(

        chi2,

        n,

        k,

    ):

        w=chi2/(

            n*(k-1)

        )

        return EffectSizeResult(

            name="Kendall W",

            statistic=float(w)

        )

    # ==========================================================
# FREEMAN THETA
# ==========================================================

    @staticmethod

    def freeman_theta(

        statistic,

        maximum,

    ):

        theta=statistic/maximum

        return EffectSizeResult(

            name="Freeman Theta",

            statistic=float(theta)

        )

    # ==========================================================
# MATCHED PAIRS RANK BISERIAL
# ==========================================================

    @staticmethod

    def matched_rank_biserial(

        positive,

        negative,

    ):

        r=(

            positive-

            negative

        )/(

            positive+

            negative

        )

        return EffectSizeResult(

            name="Matched Rank-Biserial",

            statistic=float(r)

        )
    
    # ==========================================================
# RANK ETA²
# ==========================================================

    @staticmethod

    def rank_eta_squared(

        h,

        n,

    ):

        eta2=(

            h-1

        )/(

            n-1

        )

        return EffectSizeResult(

            name="Rank Eta Squared",

            statistic=float(eta2)

        )

    # ==========================================================
# COMPUTE
# ==========================================================

    @staticmethod

    def compute(

        method,

        *args,

    ):

        methods={

            "rank_biserial":

                NonParametricEffectSize.rank_biserial,

            "cliff":

                NonParametricEffectSize.cliffs_delta,

            "vargha":

                NonParametricEffectSize.vargha_delaney,

            "cles":

                NonParametricEffectSize.common_language,

            "rosenthal":

                NonParametricEffectSize.rosenthal_r,

            "kendall_w":

                NonParametricEffectSize.kendall_w,

            "freeman":

                NonParametricEffectSize.freeman_theta,

            "matched":

                NonParametricEffectSize.matched_rank_biserial,

            "rank_eta2":

                NonParametricEffectSize.rank_eta_squared

        }

        return methods[

            method

        ](

            *args

        )

# ==========================================================
# SERVICE
# ==========================================================

class NonParametric:

    compute=NonParametricEffectSize.compute

    rank_biserial=NonParametricEffectSize.rank_biserial

    cliffs_delta=NonParametricEffectSize.cliffs_delta

    vargha_delaney=NonParametricEffectSize.vargha_delaney

    common_language=NonParametricEffectSize.common_language

    rosenthal_r=NonParametricEffectSize.rosenthal_r

    kendall_w=NonParametricEffectSize.kendall_w

    freeman_theta=NonParametricEffectSize.freeman_theta

    matched_rank_biserial=NonParametricEffectSize.matched_rank_biserial

    rank_eta_squared=NonParametricEffectSize.rank_eta_squared