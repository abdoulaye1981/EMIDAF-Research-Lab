"""
=========================================================
EMIDAF Framework
Effect Sizes for Regression
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

from .base import (

    BaseEffectSize,

    EffectSizeResult

)

# ==========================================================
# REGRESSION EFFECT SIZE
# ==========================================================

class RegressionEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for regression models.
    """

    name="Regression Effect Size"

    # ==========================================================
# MULTIPLE R
# ==========================================================

    @staticmethod

    def multiple_r(

        y_true,

        y_pred,

    ):

        r=np.corrcoef(

            y_true,

            y_pred

        )[0,1]

        return EffectSizeResult(

            name="Multiple R",

            statistic=float(r)

        )

    # ==========================================================
# R SQUARED
# ==========================================================

    @staticmethod

    def r_squared(

        y_true,

        y_pred,

    ):

        ss_res=np.sum(

            (y_true-y_pred)**2

        )

        ss_tot=np.sum(

            (

                y_true-

                np.mean(y_true)

            )**2

        )

        r2=1-ss_res/ss_tot

        return EffectSizeResult(

            name="R²",

            statistic=float(r2)

        )

    # ==========================================================
# ADJUSTED R²
# ==========================================================

    @staticmethod

    def adjusted_r_squared(

        r2,

        n,

        p,

    ):

        adjusted=(

            1-

            (

                (1-r2)

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

            statistic=float(adjusted)

        )

    # ==========================================================
# COHEN F²
# ==========================================================

    @staticmethod

    def cohen_f2(

        r2,

    ):

        f2=r2/(1-r2)

        return EffectSizeResult(

            name="Cohen f²",

            statistic=float(f2)

        )

    # ==========================================================
# PARTIAL R
# ==========================================================

    @staticmethod

    def partial_r(

        t,

        df,

    ):

        r=np.sqrt(

            (

                t**2

            )

            /

            (

                t**2+df

            )

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

        partial_r,

        r2,

    ):

        value=np.sqrt(

            partial_r**2*

            (

                1-r2

            )

        )

        return EffectSizeResult(

            name="Semi Partial Correlation",

            statistic=float(value)

        )

    # ==========================================================
# ETA SQUARED
# ==========================================================

    @staticmethod

    def eta_squared(

        ss_model,

        ss_total,

    ):

        eta2=ss_model/ss_total

        return EffectSizeResult(

            name="Eta Squared",

            statistic=float(eta2)

        )

    # ==========================================================
# OMEGA SQUARED
# ==========================================================

    @staticmethod

    def omega_squared(

        ss_model,

        df_model,

        ms_error,

        ss_total,

    ):

        omega = (
            ss_model -
            df_model * ms_error
        ) / (
            ss_total +
            ms_error
        )

        return EffectSizeResult(

            name="Omega Squared",

            statistic=float(omega)

        )

    # ==========================================================
# COHEN Q
# ==========================================================

    @staticmethod

    def cohen_q(

        r1,

        r2,

    ):

        z1=0.5*np.log(

            (

                1+r1

            )

            /

            (

                1-r1

            )

        )

        z2=0.5*np.log(

            (

                1+r2

            )

            /

            (

                1-r2

            )

        )

        q=z1-z2

        return EffectSizeResult(

            name="Cohen q",

            statistic=float(q)

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

            "multiple_r":

                RegressionEffectSize.multiple_r,

            "r2":

                RegressionEffectSize.r_squared,

            "adjusted_r2":

                RegressionEffectSize.adjusted_r_squared,

            "cohen_f2":

                RegressionEffectSize.cohen_f2,

            "partial":

                RegressionEffectSize.partial_r,

            "semi_partial":

                RegressionEffectSize.semi_partial_r,

            "eta2":

                RegressionEffectSize.eta_squared,

            "omega2":

                RegressionEffectSize.omega_squared,

            "cohen_q":

                RegressionEffectSize.cohen_q

        }

        return methods[

            method

        ](

            *args

        )

# ==========================================================
# SERVICE
# ==========================================================

class Regression:

    compute=RegressionEffectSize.compute

    multiple_r=RegressionEffectSize.multiple_r

    r_squared=RegressionEffectSize.r_squared

    adjusted_r_squared=RegressionEffectSize.adjusted_r_squared

    cohen_f2=RegressionEffectSize.cohen_f2

    partial_r=RegressionEffectSize.partial_r

    semi_partial_r=RegressionEffectSize.semi_partial_r

    eta_squared=RegressionEffectSize.eta_squared

    omega_squared=RegressionEffectSize.omega_squared

    cohen_q=RegressionEffectSize.cohen_q
