"""
=========================================================
EMIDAF Framework
Effect Sizes for ANOVA
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
# ANOVA EFFECT SIZE
# ==========================================================

class AnovaEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for ANOVA.
    """

    name="ANOVA Effect Size"

    # ==========================================================
# ETA SQUARED
# ==========================================================

    @staticmethod

    def eta_squared(

        ss_effect,

        ss_total,

    ):

        eta2=ss_effect/ss_total

        return EffectSizeResult(

            name="Eta Squared",

            statistic=float(eta2)

        )

    # ==========================================================
# PARTIAL ETA²
# ==========================================================

    @staticmethod

    def partial_eta_squared(

        ss_effect,

        ss_error,

    ):

        value=ss_effect/(

            ss_effect+

            ss_error

        )

        return EffectSizeResult(

            name="Partial Eta Squared",

            statistic=float(value)

        )

    # ==========================================================
# GENERALIZED ETA²
# ==========================================================

    @staticmethod

    def generalized_eta_squared(

        ss_effect,

        ss_error,

        ss_subjects,

    ):

        value=ss_effect/(

            ss_effect+

            ss_error+

            ss_subjects

        )

        return EffectSizeResult(

            name="Generalized Eta Squared",

            statistic=float(value)

        )

    # ==========================================================
# OMEGA SQUARED
# ==========================================================

    @staticmethod

    def omega_squared(

        ss_effect,

        df_effect,

        ms_error,

        ss_total,

    ):

        value=(

            ss_effect-

            df_effect*ms_error

        )/(

            ss_total+

            ms_error

        )

        return EffectSizeResult(

            name="Omega Squared",

            statistic=float(value)

        )

    # ==========================================================
# PARTIAL OMEGA²
# ==========================================================

    @staticmethod

    def partial_omega_squared(

        ss_effect,

        df_effect,

        ms_error,

        ss_error,

    ):

        value=(

            ss_effect-

            df_effect*ms_error

        )/(

            ss_effect+

            ss_error+

            ms_error

        )

        return EffectSizeResult(

            name="Partial Omega Squared",

            statistic=float(value)

        )

    # ==========================================================
# EPSILON²
# ==========================================================

    @staticmethod

    def epsilon_squared(

        ss_effect,

        df_effect,

        ms_error,

        ss_total,

    ):

        value=(

            ss_effect-

            df_effect*ms_error

        )/ss_total

        return EffectSizeResult(

            name="Epsilon Squared",

            statistic=float(value)

        )

    # ==========================================================
# COHEN F
# ==========================================================

    @staticmethod

    def cohen_f(

        eta_squared,

    ):

        value=np.sqrt(

            eta_squared/

            (

                1-eta_squared

            )

        )

        return EffectSizeResult(

            name="Cohen f",

            statistic=float(value)

        )

    # ==========================================================
# COHEN F²
# ==========================================================

    @staticmethod

    def cohen_f2(

        eta_squared,

    ):

        value=eta_squared/(

            1-eta_squared

        )

        return EffectSizeResult(

            name="Cohen f²",

            statistic=float(value)

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

            "eta2":

                AnovaEffectSize.eta_squared,

            "partial_eta2":

                AnovaEffectSize.partial_eta_squared,

            "generalized_eta2":

                AnovaEffectSize.generalized_eta_squared,

            "omega2":

                AnovaEffectSize.omega_squared,

            "partial_omega2":

                AnovaEffectSize.partial_omega_squared,

            "epsilon2":

                AnovaEffectSize.epsilon_squared,

            "cohen_f":

                AnovaEffectSize.cohen_f,

            "cohen_f2":

                AnovaEffectSize.cohen_f2

        }

        return methods[

            method

        ](

            *args

        )
# ==========================================================
# SERVICE
# ==========================================================

class Anova:

    compute=AnovaEffectSize.compute

    eta_squared=AnovaEffectSize.eta_squared

    partial_eta_squared=AnovaEffectSize.partial_eta_squared

    generalized_eta_squared=AnovaEffectSize.generalized_eta_squared

    omega_squared=AnovaEffectSize.omega_squared

    partial_omega_squared=AnovaEffectSize.partial_omega_squared

    epsilon_squared=AnovaEffectSize.epsilon_squared

    cohen_f=AnovaEffectSize.cohen_f

    cohen_f2=AnovaEffectSize.cohen_f2