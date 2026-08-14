"""
=========================================================
EMIDAF Framework
Power Analysis Interpretation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

from .base import PowerResult

# ==========================================================
# INTERPRETATION
# ==========================================================

class PowerInterpreter:

    """
    Automatic interpretation
    of power analyses.
    """

    # ==========================================================
# POWER
# ==========================================================

    @staticmethod

    def power(

        value,

    ):

        if value < 0.50:

            return (

                "Puissance très faible"

            )

        if value < 0.80:

            return (

                "Puissance insuffisante"

            )

        if value < 0.90:

            return (

                "Puissance satisfaisante"

            )

        return (

            "Puissance excellente"

        )
    
    # ==========================================================
# EFFECT SIZE
# ==========================================================

    @staticmethod

    def effect_size(

        value,

    ):

        value=abs(value)

        if value < 0.20:

            return "Très faible"

        if value < 0.50:

            return "Faible"

        if value < 0.80:

            return "Moyenne"

        return "Grande"

    # ==========================================================
# SAMPLE SIZE
# ==========================================================

    @staticmethod

    def sample_size(

        value,

    ):

        if value < 30:

            return (

                "Très petit échantillon"

            )

        if value < 100:

            return (

                "Petit échantillon"

            )

        if value < 300:

            return (

                "Échantillon moyen"

            )

        if value < 1000:

            return (

                "Grand échantillon"

            )

        return (

            "Très grand échantillon"

        )

    # ==========================================================
# TYPE II ERROR
# ==========================================================

    @staticmethod

    def beta(

        power,

    ):

        beta=1-power

        return beta
    

    # ==========================================================
# RECOMMENDATION
# ==========================================================

    @staticmethod

    def recommendation(

        result,

    ):

        recommendations=[]

        if result.power is not None:

            if result.power < 0.80:

                recommendations.append(

                    "Augmenter la taille de l'échantillon."

                )

            else:

                recommendations.append(

                    "La puissance statistique est adéquate."

                )

        if result.sample_size is not None:

            if result.sample_size < 30:

                recommendations.append(

                    "Attention aux petits échantillons."

                )

        return recommendations

    # ==========================================================
# INTERPRET
# ==========================================================

    @staticmethod

    def interpret(

        result,

    ):

        interpretation={}

        if result.power is not None:

            interpretation["power"]=(
                PowerInterpreter.power(
                    result.power
                )
            )

            interpretation["beta"]=(
                PowerInterpreter.beta(
                    result.power
                )
            )

        if result.effect_size is not None:

            interpretation["effect_size"]=(
                PowerInterpreter.effect_size(
                    result.effect_size
                )
            )

        if result.sample_size is not None:

            interpretation["sample_size"]=(
                PowerInterpreter.sample_size(
                    result.sample_size
                )
            )

        interpretation["recommendations"]=(
            PowerInterpreter.recommendation(
                result
            )
        )

        return interpretation
    
# ==========================================================
# SERVICE
# ==========================================================

class Interpretation:

    interpret=PowerInterpreter.interpret