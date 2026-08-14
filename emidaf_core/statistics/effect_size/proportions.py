"""
=========================================================
EMIDAF Framework
Effect Sizes for Proportions
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
# PROPORTION EFFECT SIZE
# ==========================================================

class ProportionEffectSize(

    BaseEffectSize

):

    """
    Effect sizes for proportions.
    """

    name="Proportion Effect Size"

    # ==========================================================
# COHEN H
# ==========================================================

    @staticmethod

    def cohen_h(

        p1,

        p2,

    ):

        h=(

            2*np.arcsin(

                np.sqrt(p1)

            )

            -

            2*np.arcsin(

                np.sqrt(p2)

            )

        )

        return EffectSizeResult(

            name="Cohen h",

            statistic=float(h)

        )

    # ==========================================================
# ODDS RATIO
# ==========================================================

    @staticmethod

    def odds_ratio(

        a,

        b,

        c,

        d,

    ):

        value=(

            a*d

        )/(

            b*c

        )

        return EffectSizeResult(

            name="Odds Ratio",

            statistic=float(value)

        )

    # ==========================================================
# LOG ODDS RATIO
# ==========================================================

    @staticmethod

    def log_odds_ratio(

        a,

        b,

        c,

        d,

    ):

        value=np.log(

            (

                a*d

            )/

            (

                b*c

            )

        )

        return EffectSizeResult(

            name="Log Odds Ratio",

            statistic=float(value)

        )

    # ==========================================================
# RELATIVE RISK
# ==========================================================

    @staticmethod

    def relative_risk(

        a,

        b,

        c,

        d,

    ):

        risk1=a/(a+b)

        risk2=c/(c+d)

        rr=risk1/risk2

        return EffectSizeResult(

            name="Relative Risk",

            statistic=float(rr)

        )

    # ==========================================================
# RISK DIFFERENCE
# ==========================================================

    @staticmethod

    def risk_difference(

        a,

        b,

        c,

        d,

    ):

        risk1=a/(a+b)

        risk2=c/(c+d)

        rd=risk1-risk2

        return EffectSizeResult(

            name="Risk Difference",

            statistic=float(rd)

        )

    # ==========================================================
# NNT
# ==========================================================

    @staticmethod

    def number_needed_to_treat(

        a,

        b,

        c,

        d,

    ):

        rd=(

            ProportionEffectSize

            .risk_difference(

                a,

                b,

                c,

                d

            ).statistic

        )

        if rd==0:

            value=np.inf

        else:

            value=1/abs(rd)

        return EffectSizeResult(

            name="Number Needed to Treat",

            statistic=float(value)

        )

    # ==========================================================
# ATTRIBUTABLE RISK
# ==========================================================

    @staticmethod

    def attributable_risk(

        exposed,

        unexposed,

    ):

        ar=exposed-unexposed

        return EffectSizeResult(

            name="Attributable Risk",

            statistic=float(ar)

        )

    # ==========================================================
# POPULATION ATTRIBUTABLE RISK
# ==========================================================

    @staticmethod

    def population_attributable_risk(

        population,

        unexposed,

    ):

        par=population-unexposed

        return EffectSizeResult(

            name="Population Attributable Risk",

            statistic=float(par)

        )
    
# ==========================================================
# PREVENTED FRACTION
# ==========================================================

    @staticmethod

    def prevented_fraction(

        rr,

    ):

        pf=1-rr

        return EffectSizeResult(

            name="Prevented Fraction",

            statistic=float(pf)

        )

    # ==========================================================
# SERVICE
# ==========================================================

class Proportions:

    compute=ProportionEffectSize.compute

    cohen_h=ProportionEffectSize.cohen_h

    odds_ratio=ProportionEffectSize.odds_ratio

    log_odds_ratio=ProportionEffectSize.log_odds_ratio

    relative_risk=ProportionEffectSize.relative_risk

    risk_difference=ProportionEffectSize.risk_difference

    number_needed_to_treat=ProportionEffectSize.number_needed_to_treat

    attributable_risk=ProportionEffectSize.attributable_risk

    population_attributable_risk=ProportionEffectSize.population_attributable_risk

    prevented_fraction=ProportionEffectSize.prevented_fraction