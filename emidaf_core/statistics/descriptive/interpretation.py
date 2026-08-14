"""
=========================================================
EMIDAF Framework
Descriptive Statistics Interpretation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP

=========================================================
"""

from __future__ import annotations

import numpy as np

# ==========================================================
# INTERPRETER
# ==========================================================

class DescriptiveInterpreter:

    """
    Interprète automatiquement
    les statistiques descriptives.
    """

    def __init__(

        self,

        summary,

    ):

        self.summary = summary

    # ==========================================================
# SKEWNESS
# ==========================================================

    def skewness(

        self,

    ):

        value = self.summary["shape"]["skewness"]

        if value < -1:

            return (

                "Distribution fortement asymétrique "

                "vers la gauche."

            )

        elif value < -0.5:

            return (

                "Distribution modérément "

                "asymétrique vers la gauche."

            )

        elif value <= 0.5:

            return (

                "Distribution approximativement "

                "symétrique."

            )

        elif value <= 1:

            return (

                "Distribution modérément "

                "asymétrique vers la droite."

            )

        else:

            return (

                "Distribution fortement "

                "asymétrique vers la droite."

            )
        
    # ==========================================================
# KURTOSIS
# ==========================================================

    def kurtosis(

        self,

    ):

        value = self.summary["shape"]["kurtosis"]

        if value < 0:

            return "Distribution platykurtique."

        elif value < 1:

            return "Distribution proche de la normale."

        else:

            return "Distribution leptokurtique."

    # ==========================================================
# COEFFICIENT OF VARIATION
# ==========================================================

    def coefficient_variation(

        self,

    ):

        cv = self.summary["dispersion"]["cv"]

        if cv < 0.15:

            return "Très faible dispersion."

        elif cv < 0.30:

            return "Dispersion faible."

        elif cv < 0.50:

            return "Dispersion modérée."

        else:

            return "Dispersion importante."
        
    # ==========================================================
# OUTLIERS
# ==========================================================

    def outliers(

        self,

    ):

        median = self.summary["central"]["median"]

        mean = self.summary["central"]["mean"]

        std = self.summary["dispersion"]["std"]

        if abs(

            mean-median

        ) > std:

            return (

                "Présence probable "

                "de valeurs aberrantes."

            )

        return (

            "Aucune anomalie "

            "majeure détectée."

        )
    
    # ==========================================================
# CONCLUSION
# ==========================================================

    def conclusion(

        self,

    ):

        return {

            "symmetry":

                self.skewness(),

            "kurtosis":

                self.kurtosis(),

            "dispersion":

                self.coefficient_variation(),

            "outliers":

                self.outliers()

        }

    # ==========================================================
# RECOMMENDATIONS
# ==========================================================

    def recommendations(

        self,

    ):

        advice = []

        skew = self.summary["shape"]["skewness"]

        if abs(skew) > 1:

            advice.append(

                "Envisager une transformation logarithmique ou Box-Cox."

            )

        cv = self.summary["dispersion"]["cv"]

        if cv > 0.50:

            advice.append(

                "Analyser les causes de la forte variabilité."

            )

        if abs(

            self.summary["central"]["mean"]

            -

            self.summary["central"]["median"]

        ) > self.summary["dispersion"]["std"]:

            advice.append(

                "Examiner les valeurs aberrantes."

            )

        if len(advice) == 0:

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

            "interpretation":

                self.conclusion(),

            "recommendations":

                self.recommendations()

        }

    # ==========================================================
# SERVICE
# ==========================================================

class Interpretation:

    @staticmethod

    def interpret(

        summary,

    ):

        engine = DescriptiveInterpreter(

            summary

        )

        return engine.report()