"""
=========================================================
EMIDAF Framework
Effect Size Interpretation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from .base import EffectSizeResult

# ==========================================================
# INTERPRETATION
# ==========================================================

class EffectSizeInterpreter:

    """
    Automatic interpretation
    of effect sizes.
    """

    # ==========================================================
# COHEN D
# ==========================================================

    @staticmethod
    def cohen_d(value):

        value=abs(value)

        if value<0.20:
            return "Négligeable"

        if value<0.50:
            return "Faible"

        if value<0.80:
            return "Moyen"

        return "Grand"

    # ==========================================================
# CORRELATION
# ==========================================================

    @staticmethod
    def correlation(value):

        value=abs(value)

        if value<0.10:
            return "Négligeable"

        if value<0.30:
            return "Faible"

        if value<0.50:
            return "Modérée"

        if value<0.70:
            return "Forte"

        return "Très forte"

    # ==========================================================
# ETA SQUARED
# ==========================================================

    @staticmethod
    def eta_squared(value):

        value=abs(value)

        if value<0.01:
            return "Négligeable"

        if value<0.06:
            return "Faible"

        if value<0.14:
            return "Moyen"

        return "Grand"

    # ==========================================================
# OMEGA²
# ==========================================================

    @staticmethod
    def omega_squared(value):

        return EffectSizeInterpreter.eta_squared(
            value
        )

    # ==========================================================
# COHEN H
# ==========================================================

    @staticmethod
    def cohen_h(value):

        return EffectSizeInterpreter.cohen_d(
            value
        )

    # ==========================================================
# PHI
# ==========================================================

    @staticmethod
    def phi(value):

        return EffectSizeInterpreter.correlation(
            value
        )

    # ==========================================================
# CRAMER V
# ==========================================================

    @staticmethod
    def cramers_v(value):

        return EffectSizeInterpreter.correlation(
            value
        )

    # ==========================================================
# CLIFF DELTA
# ==========================================================

    @staticmethod
    def cliffs_delta(value):

        value=abs(value)

        if value<0.147:
            return "Négligeable"

        if value<0.33:
            return "Faible"

        if value<0.474:
            return "Moyen"

        return "Grand"

    # ==========================================================
# ODDS RATIO
# ==========================================================

    @staticmethod
    def odds_ratio(value):

        if value==1:
            return "Aucun effet"

        if value<1:
            return "Association négative"

        return "Association positive"

    # ==========================================================
# COHEN F
# ==========================================================

    @staticmethod
    def cohen_f(value):

        value=abs(value)

        if value<0.10:
            return "Faible"

        if value<0.25:
            return "Moyen"

        if value<0.40:
            return "Grand"

        return "Très grand"

    # ==========================================================
# INTERPRET
# ==========================================================

    @staticmethod
    def interpret(result):

        name=result.name.lower()

        value=result.statistic

        if "cohen d" in name:
            level=EffectSizeInterpreter.cohen_d(value)

        elif "hedges" in name:
            level=EffectSizeInterpreter.cohen_d(value)

        elif "glass" in name:
            level=EffectSizeInterpreter.cohen_d(value)

        elif "eta" in name:
            level=EffectSizeInterpreter.eta_squared(value)

        elif "omega" in name:
            level=EffectSizeInterpreter.omega_squared(value)

        elif "phi" in name:
            level=EffectSizeInterpreter.phi(value)

        elif "cramer" in name:
            level=EffectSizeInterpreter.cramers_v(value)

        elif "correlation" in name:
            level=EffectSizeInterpreter.correlation(value)

        elif "cliff" in name:
            level=EffectSizeInterpreter.cliffs_delta(value)

        elif "odds" in name:
            level=EffectSizeInterpreter.odds_ratio(value)

        elif "cohen f" in name:
            level=EffectSizeInterpreter.cohen_f(value)

        else:
            level="Interprétation indisponible"

        result.magnitude=level

        result.interpretation=(
            f"Taille d'effet : {level}."
        )

        return result

# ==========================================================
# SERVICE
# ==========================================================

class Interpretation:

    interpret=EffectSizeInterpreter.interpret