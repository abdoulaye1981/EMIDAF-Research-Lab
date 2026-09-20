"""
=========================================================
EMIDAF Framework
EXAIE - Interpretation
=========================================================
"""

from __future__ import annotations

import pandas as pd


class ExplainabilityInterpreter:
    """
    Interprétation prudente des résultats EXAIE.
    """

    @staticmethod
    def global_importance(
        table: pd.DataFrame | None,
    ) -> str:

        if (
            table is None
            or table.empty
        ):
            return (
                "Aucune importance globale "
                "n'a pu être calculée."
            )

        top = table.iloc[0]

        feature = top["feature"]
        method = top.get(
            "method",
            "importance",
        )

        return (
            f"La variable « {feature} » présente "
            f"l'importance la plus élevée selon "
            f"la méthode « {method} ». "
            "Cette importance décrit la contribution "
            "du prédicteur au fonctionnement du modèle "
            "et ne doit pas être interprétée comme "
            "une relation causale."
        )

    @staticmethod
    def permutation(
        table: pd.DataFrame | None,
        *,
        tolerance: float = 1e-4,
    ) -> str:

        if (
            table is None
            or table.empty
        ):
            return (
                "L'importance par permutation "
                "n'est pas disponible."
            )

        meaningful = table[
            table["importance"] > tolerance
        ]

        if meaningful.empty:
            return (
                "Aucune variable ne présente une "
                "importance par permutation suffisamment "
                "marquée sur le jeu de test. Les variations "
                "mesurées sont nulles ou négligeables au "
                "seuil retenu. Il n'est donc pas justifié "
                "d'identifier une variable dominante."
            )

        top = meaningful.iloc[0]

        std = top.get(
            "std",
            None,
        )

        message = (
            f"La performance du modèle est la plus "
            f"sensible à la variable « {top['feature']} » "
            "lorsqu'elle est permutée."
        )

        if std is not None:
            message += (
                f" L'importance moyenne estimée est "
                f"{top['importance']:.6f} "
                f"(écart-type {std:.6f})."
            )

        message += (
            " Cette mesure décrit une dépendance "
            "prédictive et ne démontre pas de causalité."
        )

        return message


Interpretation = ExplainabilityInterpreter
