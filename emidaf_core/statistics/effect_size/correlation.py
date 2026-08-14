"""
=========================================================
EMIDAF Framework
Correlation Effect Sizes
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
# CORRELATION EFFECT SIZE
# ==========================================================

class CorrelationEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for correlation analysis.
    """

    name="Correlation Effect Size"

    # ==========================================================
# PEARSON R
# ==========================================================

    @staticmethod

    def pearson(

        x,

        y,

    ):

        r,_=stats.pearsonr(

            x,

            y

        )

        return EffectSizeResult(

            name="Pearson r",

            statistic=float(r)

        )

    # ==========================================================
# SPEARMAN
# ==========================================================

    @staticmethod

    def spearman(

        x,

        y,

    ):

        rho,_=stats.spearmanr(

            x,

            y

        )

        return EffectSizeResult(

            name="Spearman rho",

            statistic=float(rho)

        )

    # ==========================================================
# KENDALL
# ==========================================================

    @staticmethod

    def kendall(

        x,

        y,

    ):

        tau,_=stats.kendalltau(

            x,

            y

        )

        return EffectSizeResult(

            name="Kendall tau",

            statistic=float(tau)

        )

    # ==========================================================
# R SQUARED
# ==========================================================

    @staticmethod

    def r_squared(

        x,

        y,

    ):

        r,_=stats.pearsonr(

            x,

            y

        )

        return EffectSizeResult(

            name="R Squared",

            statistic=float(

                r**2

            )

        )

    # ==========================================================
# ADJUSTED R SQUARED
# ==========================================================

    @staticmethod

    def adjusted_r_squared(

        r_squared,

        n,

        p,

    ):

        adjusted=(

            1-

            (

                (1-r_squared)

                *

                (n-1)

            )

            /

            (

                n-p-1

            )

        )

        return EffectSizeResult(

            name="Adjusted R²",

            statistic=float(

                adjusted

            )

        )

    # ==========================================================
# FISHER Z
# ==========================================================

    @staticmethod

    def fisher_z(

        r,

    ):

        z=0.5*np.log(

            (

                1+r

            )

            /

            (

                1-r

            )

        )

        return EffectSizeResult(

            name="Fisher Z",

            statistic=float(z)

        )

    # ==========================================================
# MULTIPLE R
# ==========================================================

    @staticmethod

    def multiple_r(

        predictions,

        observations,

    ):

        r=np.corrcoef(

            predictions,

            observations

        )[0,1]

        return EffectSizeResult(

            name="Multiple R",

            statistic=float(r)

        )

    # ==========================================================
# PARTIAL CORRELATION
# ==========================================================

    @staticmethod

    def partial_r(

        residual_x,

        residual_y,

    ):

        r,_=stats.pearsonr(

            residual_x,

            residual_y

        )

        return EffectSizeResult(

            name="Partial Correlation",

            statistic=float(r)

        )
    
    # ==========================================================
# SEMI PARTIAL
# ==========================================================

    @staticmethod

    def semi_partial_r(

        residual,

        y,

    ):

        r,_=stats.pearsonr(

            residual,

            y

        )

        return EffectSizeResult(

            name="Semi Partial Correlation",

            statistic=float(r)

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

            "pearson":

                CorrelationEffectSize.pearson,

            "spearman":

                CorrelationEffectSize.spearman,

            "kendall":

                CorrelationEffectSize.kendall,

            "r2":

                CorrelationEffectSize.r_squared,

            "adjusted_r2":

                CorrelationEffectSize.adjusted_r_squared,

            "fisher":

                CorrelationEffectSize.fisher_z,

            "multiple_r":

                CorrelationEffectSize.multiple_r,

            "partial":

                CorrelationEffectSize.partial_r,

            "semi_partial":

                CorrelationEffectSize.semi_partial_r

        }

        return methods[

            method

        ](

            *args

        )

# ==========================================================
# SERVICE
# ==========================================================

class Correlation:

    compute=CorrelationEffectSize.compute

    pearson=CorrelationEffectSize.pearson

    spearman=CorrelationEffectSize.spearman

    kendall=CorrelationEffectSize.kendall

    r_squared=CorrelationEffectSize.r_squared

    adjusted_r_squared=CorrelationEffectSize.adjusted_r_squared

    fisher_z=CorrelationEffectSize.fisher_z

    multiple_r=CorrelationEffectSize.multiple_r

    partial_r=CorrelationEffectSize.partial_r

    semi_partial_r=CorrelationEffectSize.semi_partial_r