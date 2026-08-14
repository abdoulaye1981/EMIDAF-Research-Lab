"""
=========================================================
EMIDAF Framework
Inferential Interpretation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

# ==========================================================
# INTERPRETATION ENGINE
# ==========================================================

class InferentialInterpreter:

    """
    Automatic scientific interpretation
    of inferential statistical results.
    """

    def __init__(

        self,

        result,

    ):

        self.result=result

    # ==========================================================
# DECISION
# ==========================================================

    def decision(

        self,

    ):

        if self.result.reject_null:

            return (

                "L'hypothèse nulle est rejetée."

            )

        return (

            "Les données ne permettent pas de rejeter l'hypothèse nulle."

        )

    # ==========================================================
# SIGNIFICANCE
# ==========================================================

    def significance(

        self,

    ):

        p=self.result.p_value

        if p is None:

            return (

                "Aucune p-value disponible."

            )

        if p<0.001:

            return (

                "Résultat extrêmement significatif."

            )

        elif p<0.01:

            return (

                "Résultat très significatif."

            )

        elif p<0.05:

            return (

                "Résultat statistiquement significatif."

            )

        elif p<0.10:

            return (

                "Résultat marginalement significatif."

            )

        return (

            "Résultat non significatif."

        )

    # ==========================================================
# CONFIDENCE INTERVAL
# ==========================================================

    def confidence_interval(

        self,

    ):

        ci=self.result.confidence_interval

        if ci is None:

            return (

                "Intervalle de confiance non disponible."

            )

        return (

            f"IC : [{ci[0]:.4f} ; {ci[1]:.4f}]"

        )

    # ==========================================================
# EFFECT SIZE
# ==========================================================

    def effect_size(

        self,

    ):

        effect=self.result.effect_size

        if effect is None:

            return (

                "Taille d'effet non calculée."

            )

        value=abs(effect)

        if value<0.20:

            level="négligeable"

        elif value<0.50:

            level="faible"

        elif value<0.80:

            level="modérée"

        else:

            level="importante"

        return (

            f"Taille d'effet {level} "

            f"({effect:.3f})."

        )
    
    # ==========================================================
# POWER
# ==========================================================

    def power(

        self,

    ):

        power=self.result.power

        if power is None:

            return (

                "Puissance statistique non disponible."

            )

        if power>=0.80:

            return (

                "La puissance statistique est satisfaisante."

            )

        return (

            "La puissance statistique est faible."

        )

    # ==========================================================
# RECOMMENDATIONS
# ==========================================================

    def recommendations(

        self,

    ):

        advice=[]

        if self.result.p_value is not None:

            if self.result.p_value>0.05:

                advice.append(

                    "Augmenter éventuellement la taille de l'échantillon."

                )

        if self.result.effect_size is not None:

            if abs(self.result.effect_size)<0.20:

                advice.append(

                    "L'effet observé est très faible."

                )

        if self.result.power is not None:

            if self.result.power<0.80:

                advice.append(

                    "Envisager une analyse de puissance."

                )

        if len(advice)==0:

            advice.append(

                "Aucune recommandation particulière."

            )

        return advice

    # ==========================================================
# REPORT
# ==========================================================

    def report(

        self,

    ):

        return {

            "decision":

                self.decision(),

            "significance":

                self.significance(),

            "confidence_interval":

                self.confidence_interval(),

            "effect_size":

                self.effect_size(),

            "power":

                self.power(),

            "recommendations":

                self.recommendations()

        }

# ==========================================================
# SERVICE
# ==========================================================

class Interpretation:

    @staticmethod

    def interpret(

        result,

    ):

        engine=InferentialInterpreter(

            result

        )

        return engine.report()