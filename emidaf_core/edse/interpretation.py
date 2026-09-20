"""
=========================================================
EMIDAF Framework
EDSE - Decision Interpretation
=========================================================
"""

from __future__ import annotations


class DecisionInterpreter:

    @staticmethod
    def scenario(
        summary: dict,
        *,
        threshold,
        task: str,
        direction: str | None = None,
    ) -> str:

        rate = (
            summary["selected_rate"]
            * 100
        )

        if task == "classification":

            return (
                f"Avec le seuil choisi de "
                f"{threshold:.2f}, "
                f"{summary['selected']} observations "
                f"sur {summary['observations']} "
                f"({rate:.1f} %) satisfont le "
                "critère défini. "
                "Ce résultat constitue un scénario "
                "d'aide à la décision et non une "
                "décision automatique."
            )

        relation = (
            "supérieure ou égale"
            if direction == "above"
            else "inférieure ou égale"
        )

        return (
            f"Avec un seuil de {threshold:.4f}, "
            f"{summary['selected']} observations "
            f"sur {summary['observations']} "
            f"({rate:.1f} %) présentent une prédiction "
            f"{relation} au seuil. "
            "Le seuil doit être justifié par le "
            "contexte métier ou scientifique."
        )

    @staticmethod
    def reliability(
        assessment: dict,
    ) -> str:

        if assessment["reliable"]:

            return (
                "Les performances disponibles ne "
                "signalent pas de limitation majeure "
                "pour une utilisation exploratoire "
                "en aide à la décision. Une validation "
                "métier reste néanmoins nécessaire."
            )

        return (
            "Les performances du modèle imposent une "
            "interprétation prudente. Les scénarios "
            "EDSE doivent être considérés comme "
            "exploratoires et ne doivent pas être "
            "utilisés seuls pour prendre une décision."
        )


Interpretation = DecisionInterpreter
