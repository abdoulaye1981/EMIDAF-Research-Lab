"""
=========================================================
EMIDAF Framework
Effect Sizes for Mean Differences
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
# MEAN DIFFERENCE
# ==========================================================

class MeanDifferenceEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for mean comparison.
    """

    name="Mean Difference"

    # ==========================================================
# POOLED SD
# ==========================================================

    @staticmethod

    def pooled_sd(

        x,

        y,

    ):

        nx=len(x)

        ny=len(y)

        sx=np.var(

            x,

            ddof=1

        )

        sy=np.var(

            y,

            ddof=1

        )

        pooled = np.sqrt(
            (
                (nx - 1) * sx +
                (ny - 1) * sy
            ) / (nx + ny - 2)
        )

        return pooled

    # ==========================================================
# COHEN D
# ==========================================================

    @staticmethod

    def cohen_d(

        x,

        y,

    ):

        pooled=(

            MeanDifferenceEffectSize

            .pooled_sd(

                x,

                y

            )

        )

        d = (
            np.mean(x) -
            np.mean(y)
        ) / pooled

        return EffectSizeResult(

            name="Cohen d",

            statistic=float(d)

        )

    # ==========================================================
# HEDGES G
# ==========================================================

    @staticmethod

    def hedges_g(

        x,

        y,

    ):

        d=(

            MeanDifferenceEffectSize

            .cohen_d(

                x,

                y

            ).statistic

        )

        n=len(x)+len(y)

        correction=(

            1-

            3/(4*n-9)

        )

        g=d*correction

        return EffectSizeResult(

            name="Hedges g",

            statistic=float(g)

        )

    # ==========================================================
# GLASS DELTA
# ==========================================================

    @staticmethod

    def glass_delta(

        x,

        y,

    ):

        delta = (
            np.mean(x) -
            np.mean(y)
        ) / np.std(
            y,
            ddof=1
        )

        return EffectSizeResult(

            name="Glass Delta",

            statistic=float(delta)

        )

    # ==========================================================
# MEAN DIFFERENCE
# ==========================================================

    @staticmethod

    def mean_difference(

        x,

        y,

    ):

        md=(

            np.mean(x)-

            np.mean(y)

        )

        return EffectSizeResult(

            name="Mean Difference",

            statistic=float(md)

        )

    # ==========================================================
# STANDARDIZED MEAN DIFFERENCE
# ==========================================================

    @staticmethod

    def smd(

        x,

        y,

    ):

        return (

            MeanDifferenceEffectSize

            .cohen_d(

                x,

                y

            )

        )

    # ==========================================================
# COHEN DZ
# ==========================================================

    @staticmethod

    def cohen_dz(

        before,

        after,

    ):

        difference=np.asarray(

            before

        )-np.asarray(

            after

        )

        dz = (
            np.mean(difference)
            / np.std(
                difference,
                ddof=1
            )
        )


        return EffectSizeResult(

            name="Cohen dz",

            statistic=float(dz)

        )

    # ==========================================================
# COHEN DAV
# ==========================================================

    @staticmethod

    def cohen_dav(

        before,

        after,

    ):

        sd=np.sqrt(

            (

                np.var(

                    before,

                    ddof=1

                )+

                np.var(

                    after,

                    ddof=1

                )

            )/2

        )

        d = (
            np.mean(before) -
            np.mean(after)
        ) / sd

        return EffectSizeResult(

            name="Cohen dav",

            statistic=float(d)

        )

    # ==========================================================
# SRM
# ==========================================================

    @staticmethod

    def srm(

        before,

        after,

    ):

        difference=np.asarray(

            before

        )-np.asarray(

            after

        )

        srm = (
            np.mean(difference)
            / np.std(
                difference,
                ddof=1
            )
        )

        return EffectSizeResult(

            name="SRM",

            statistic=float(srm)

        )

    # ==========================================================
# COMPUTE
# ==========================================================

    @staticmethod

    def compute(

        method,

        x,

        y,

    ):

        methods={

            "cohen":

                MeanDifferenceEffectSize.cohen_d,

            "hedges":

                MeanDifferenceEffectSize.hedges_g,

            "glass":

                MeanDifferenceEffectSize.glass_delta,

            "md":

                MeanDifferenceEffectSize.mean_difference,

            "smd":

                MeanDifferenceEffectSize.smd,

            "cohen_dz":

                MeanDifferenceEffectSize.cohen_dz,

            "cohen_dav":

                MeanDifferenceEffectSize.cohen_dav,

            "srm":

                MeanDifferenceEffectSize.srm

        }

        return methods[

            method

        ](

            x,

            y

        )

# ==========================================================
# SERVICE
# ==========================================================

class MeanDifference:

    compute=MeanDifferenceEffectSize.compute

    cohen_d=MeanDifferenceEffectSize.cohen_d

    hedges_g=MeanDifferenceEffectSize.hedges_g

    glass_delta=MeanDifferenceEffectSize.glass_delta

    mean_difference=MeanDifferenceEffectSize.mean_difference

    smd=MeanDifferenceEffectSize.smd

    cohen_dz=MeanDifferenceEffectSize.cohen_dz

    cohen_dav=MeanDifferenceEffectSize.cohen_dav

    srm=MeanDifferenceEffectSize.srm
