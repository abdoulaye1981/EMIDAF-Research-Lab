"""
=========================================================
EMIDAF Framework
Effect Sizes for Contingency Tables
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
# CONTINGENCY EFFECT SIZE
# ==========================================================

class ContingencyEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for contingency tables.
    """

    name="Contingency Effect Size"

    # ==========================================================
# PHI
# ==========================================================

    @staticmethod

    def phi(

        chi2,

        n,

    ):

        phi=np.sqrt(

            chi2/n

        )

        return EffectSizeResult(

            name="Phi",

            statistic=float(phi)

        )

    # ==========================================================
# CRAMER V
# ==========================================================

    @staticmethod

    def cramers_v(

        chi2,

        n,

        rows,

        columns,

    ):

        k=min(

            rows-1,

            columns-1

        )

        value=np.sqrt(

            chi2/

            (

                n*k

            )

        )

        return EffectSizeResult(

            name="Cramer's V",

            statistic=float(value)

        )

    # ==========================================================
# TSCHUPROW T
# ==========================================================

    @staticmethod

    def tschuprow_t(

        chi2,

        n,

        rows,

        columns,

    ):

        denominator=np.sqrt(

            (

                rows-1

            )

            *

            (

                columns-1

            )

        )

        value=np.sqrt(

            chi2/

            (

                n*denominator

            )

        )

        return EffectSizeResult(

            name="Tschuprow T",

            statistic=float(value)

        )

    # ==========================================================
# PEARSON CONTINGENCY
# ==========================================================

    @staticmethod

    def pearson_contingency(

        chi2,

        n,

    ):

        coefficient=np.sqrt(

            chi2/

            (

                chi2+n

            )

        )

        return EffectSizeResult(

            name="Pearson Contingency",

            statistic=float(coefficient)

        )

    # ==========================================================
# GENERALIZED ODDS RATIO
# ==========================================================

    @staticmethod

    def generalized_odds_ratio(

        odds_ratio,

    ):

        return EffectSizeResult(

            name="Generalized Odds Ratio",

            statistic=float(

                odds_ratio

            )

        )

    # ==========================================================
# GOODMAN KRUSKAL LAMBDA
# ==========================================================

    @staticmethod
    def goodman_kruskal_lambda(
        errors_without,
        errors_with,
    ):
        value = (
            errors_without -
            errors_with
        ) / errors_without

        return EffectSizeResult(
            name="Goodman-Kruskal Lambda",
            statistic=float(value)
        )

    # ==========================================================
# GOODMAN KRUSKAL TAU
# ==========================================================

    @staticmethod

    def goodman_kruskal_tau(

        explained,

        total,

    ):

        value=explained/total

        return EffectSizeResult(

            name="Goodman-Kruskal Tau",

            statistic=float(value)

        )

    # ==========================================================
# THEIL U
# ==========================================================

    @staticmethod

    def theils_u(

        entropy_x,

        conditional_entropy,

    ):

        value = (
            entropy_x -
            conditional_entropy
        ) / entropy_x

        return EffectSizeResult(

            name="Theil U",

            statistic=float(value)

        )

    # ==========================================================
# YULE Q
# ==========================================================

    @staticmethod

    def yule_q(

        odds_ratio,

    ):

        value = (
            odds_ratio - 1
        ) / (
            odds_ratio + 1
        )

        return EffectSizeResult(

            name="Yule Q",

            statistic=float(value)

        )
    

    # ==========================================================
# YULE Y
# ==========================================================

    @staticmethod

    def yule_y(

        odds_ratio,

    ):

        root=np.sqrt(

            odds_ratio

        )

        value = (
            root - 1
        ) / (
            root + 1
        )

        return EffectSizeResult(

            name="Yule Y",

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

            "phi":

                ContingencyEffectSize.phi,

            "cramers_v":

                ContingencyEffectSize.cramers_v,

            "tschuprow":

                ContingencyEffectSize.tschuprow_t,

            "pearson":

                ContingencyEffectSize.pearson_contingency,

            "lambda":

                ContingencyEffectSize.goodman_kruskal_lambda,

            "tau":

                ContingencyEffectSize.goodman_kruskal_tau,

            "theils_u":

                ContingencyEffectSize.theils_u,

            "odds_ratio":

                ContingencyEffectSize.generalized_odds_ratio,

            "yule_q":

                ContingencyEffectSize.yule_q,

            "yule_y":

                ContingencyEffectSize.yule_y

        }

        return methods[

            method

        ](

            *args

        )

# ==========================================================
# SERVICE
# ==========================================================

class Contingency:

    compute=ContingencyEffectSize.compute

    phi=ContingencyEffectSize.phi

    cramers_v=ContingencyEffectSize.cramers_v

    tschuprow_t=ContingencyEffectSize.tschuprow_t

    pearson_contingency=ContingencyEffectSize.pearson_contingency

    goodman_kruskal_lambda=ContingencyEffectSize.goodman_kruskal_lambda

    goodman_kruskal_tau=ContingencyEffectSize.goodman_kruskal_tau

    theils_u=ContingencyEffectSize.theils_u

    generalized_odds_ratio=ContingencyEffectSize.generalized_odds_ratio

    yule_q=ContingencyEffectSize.yule_q

    yule_y=ContingencyEffectSize.yule_y
