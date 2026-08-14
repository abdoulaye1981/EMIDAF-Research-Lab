"""
=========================================================
EMIDAF Framework
Distribution Interpretation Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
=========================================================
"""

from __future__ import annotations

import numpy as np

# ==========================================================
# INTERPRETATION
# ==========================================================

class DistributionInterpreter:

    """
    Automatic interpretation of
    probability distributions.
    """

    def __init__(

        self,

        summary,

    ):

        self.summary=summary

    # ==========================================================
# BEST DISTRIBUTION
# ==========================================================

    def best_distribution(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        return (

            f"La meilleure distribution est "

            f"{best['Distribution']}."

        )

    # ==========================================================
# RANKING
# ==========================================================

    def ranking(

        self,

    ):

        ranking=self.summary[

            "ranking"

        ]

        return (

            f"{len(ranking)} distributions "

            "ont été comparées."

        )

    # ==========================================================
# GOODNESS OF FIT
# ==========================================================

    def goodness_of_fit(

        self,

    ):

        gof=self.summary[

            "goodness_of_fit"

        ]

        messages=[]

        for name,result in gof.items():

            if result.p_value is None:

                continue

            if result.p_value>0.05:

                messages.append(

                    f"{name} : ajustement acceptable."

                )

            else:

                messages.append(

                    f"{name} : ajustement rejeté."

                )

        return messages


    # ==========================================================
# AIC
# ==========================================================

    def aic(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        return (

            f"AIC minimal : "

            f"{best['AIC']:.3f}."

        )

    # ==========================================================
# BIC
# ==========================================================

    def bic(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        return (

            f"BIC minimal : "

            f"{best['BIC']:.3f}."

        )

    # ==========================================================
# RECOMMENDATIONS
# ==========================================================

    def recommendations(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        recommendations=[]

        if best["Distribution"]=="Normal":

            recommendations.append(

                "Les méthodes paramétriques sont appropriées."

            )

        else:

            recommendations.append(

                "Vérifier les hypothèses avant d'utiliser des tests paramétriques."

            )

            recommendations.append(

                "Les approches bootstrap ou non paramétriques peuvent être envisagées."

            )

        return recommendations


    # ==========================================================
# CONCLUSION
# ==========================================================

    def conclusion(

        self,

    ):

        best=self.summary[

            "best_distribution"

        ]

        return (

            f"Les données sont mieux décrites "

            f"par une distribution "

            f"{best['Distribution']}."

        )

    # ==========================================================
# REPORT
# ==========================================================

    def report(

        self,

    ):

        return {

            "best_distribution":

                self.best_distribution(),

            "ranking":

                self.ranking(),

            "aic":

                self.aic(),

            "bic":

                self.bic(),

            "goodness_of_fit":

                self.goodness_of_fit(),

            "recommendations":

                self.recommendations(),

            "conclusion":

                self.conclusion()

        }

# ==========================================================
# SERVICE
# ==========================================================

class Interpretation:

    @staticmethod

    def interpret(

        summary,

    ):

        engine=DistributionInterpreter(

            summary

        )

        return engine.report()