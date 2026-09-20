"""
=========================================================
EMIDAF Framework
EDSE - Model Assessment
=========================================================
"""

from __future__ import annotations


class DecisionAssessment:
    """
    Qualification méthodologique de la fiabilité
    d'un modèle avant son utilisation décisionnelle.
    """

    @staticmethod
    def assess(
        *,
        task: str,
        cv_mean: float | None,
        test_score: float | None,
        better_than_baseline: bool | None = None,
    ) -> dict:

        warnings = []

        if cv_mean is None:
            warnings.append(
                "La performance en validation croisée "
                "n'est pas disponible."
            )

        if test_score is None:
            warnings.append(
                "La performance sur le jeu de test "
                "n'est pas disponible."
            )

        reliable = True

        if task == "regression":

            if (
                cv_mean is not None
                and cv_mean <= 0
            ):
                reliable = False

                warnings.append(
                    "Le score de validation croisée "
                    "n'indique pas une capacité prédictive "
                    "convaincante."
                )

            if (
                test_score is not None
                and test_score <= 0
            ):
                reliable = False

                warnings.append(
                    "Le score sur le jeu de test "
                    "est nul ou négatif."
                )

        if better_than_baseline is False:
            reliable = False

            warnings.append(
                "Le modèle ne fait pas mieux que "
                "la référence naïve utilisée par EAIE."
            )

        if reliable:
            level = "acceptable"
        else:
            level = "prudence"

        return {
            "reliable": reliable,
            "level": level,
            "warnings": warnings,
        }
