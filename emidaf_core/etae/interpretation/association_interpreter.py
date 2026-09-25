"""
=========================================================
EMIDAF Framework v1.0
ETAE - Association Interpreter
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class InterpretationStatement:
    level: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "message": self.message,
        }


@dataclass(frozen=True)
class InterpretationResult:
    title: str
    statements: list[InterpretationStatement]

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "statements": [
                statement.to_dict()
                for statement in self.statements
            ],
        }


class AssociationInterpreter:
    """
    Produit des interprétations scientifiques prudentes
    à partir des résultats ETAE.
    """

    @staticmethod
    def interpret_topic_target(
        result,
    ) -> InterpretationResult:

        statements = []

        if not result.groups:
            return InterpretationResult(
                title=(
                    "Association thèmes / "
                    f"{result.target_column}"
                ),
                statements=[
                    InterpretationStatement(
                        level="warning",
                        message=(
                            "Aucune observation exploitable "
                            "n'est disponible pour cette analyse."
                        ),
                    )
                ],
            )

        means = {
            group.topic: group.mean
            for group in result.groups
        }

        min_topic = min(
            means,
            key=means.get,
        )

        max_topic = max(
            means,
            key=means.get,
        )

        statements.append(
            InterpretationStatement(
                level="descriptive",
                message=(
                    f"La moyenne de {result.target_column} "
                    f"est la plus élevée pour le thème "
                    f"{max_topic} "
                    f"({means[max_topic]:.3f}) et la plus "
                    f"faible pour le thème {min_topic} "
                    f"({means[min_topic]:.3f})."
                ),
            )
        )

        inference = result.inference

        if inference is None:
            statements.append(
                InterpretationStatement(
                    level="warning",
                    message=(
                        "Aucun test inférentiel exploitable "
                        "n'a été calculé."
                    ),
                )
            )

            return InterpretationResult(
                title=(
                    "Association thèmes / "
                    f"{result.target_column}"
                ),
                statements=statements,
            )

        recommended = (
            inference.recommended_test
        )

        if recommended is not None:
            statements.append(
                InterpretationStatement(
                    level="diagnostic",
                    message=(
                        "Le test recommandé à partir du "
                        "diagnostic d'homogénéité des "
                        f"variances est : {recommended}."
                    ),
                )
            )

        selected = None

        if recommended == "ANOVA":
            selected = inference.anova

        elif recommended == "Welch ANOVA":
            selected = inference.welch_anova

        if selected is not None:
            if (
                selected.p_value is not None
                and selected.significant is True
            ):
                statements.append(
                    InterpretationStatement(
                        level="inference",
                        message=(
                            "Le test global indique une "
                            "différence statistiquement "
                            "significative entre au moins "
                            "deux groupes de thèmes "
                            f"(p={selected.p_value:.4g}). "
                            "Ce résultat ne permet pas à lui "
                            "seul d'identifier les groupes qui "
                            "diffèrent ni d'établir une relation "
                            "causale."
                        ),
                    )
                )

            elif selected.p_value is not None:
                statements.append(
                    InterpretationStatement(
                        level="inference",
                        message=(
                            "Le test global ne met pas en "
                            "évidence de différence "
                            "statistiquement significative "
                            "entre les groupes de thèmes "
                            f"(p={selected.p_value:.4g})."
                        ),
                    )
                )

        eta = (
            inference
            .eta_squared
            .value
        )

        omega = (
            inference
            .omega_squared
            .value
        )

        epsilon = (
            inference
            .epsilon_squared
            .value
        )

        if eta is not None:
            statements.append(
                InterpretationStatement(
                    level="effect_size",
                    message=(
                        "La taille d'effet "
                        f"η² est estimée à {eta:.3f}."
                    ),
                )
            )

        if omega is not None:
            statements.append(
                InterpretationStatement(
                    level="effect_size",
                    message=(
                        "La taille d'effet ajustée "
                        f"ω² est estimée à {omega:.3f}."
                    ),
                )
            )

        if epsilon is not None:
            statements.append(
                InterpretationStatement(
                    level="effect_size",
                    message=(
                        "La taille d'effet non paramétrique "
                        f"ε² est estimée à {epsilon:.3f}."
                    ),
                )
            )

        statements.append(
            InterpretationStatement(
                level="caution",
                message=(
                    "Les thèmes ont été obtenus par une "
                    "méthode algorithmique de topic modeling. "
                    "Ils doivent être interprétés à partir de "
                    "leurs termes caractéristiques et, lorsque "
                    "possible, validés qualitativement."
                ),
            )
        )

        return InterpretationResult(
            title=(
                "Association thèmes / "
                f"{result.target_column}"
            ),
            statements=statements,
        )

    @staticmethod
    def interpret_sentiment_numeric(
        result,
    ) -> InterpretationResult:

        statements = []

        if not result.groups:
            return InterpretationResult(
                title=(
                    "Association sentiment / "
                    f"{result.target_column}"
                ),
                statements=[
                    InterpretationStatement(
                        level="warning",
                        message=(
                            "Aucune observation exploitable "
                            "n'est disponible."
                        ),
                    )
                ],
            )

        means = {
            group.sentiment: group.mean
            for group in result.groups
        }

        max_group = max(
            means,
            key=means.get,
        )

        min_group = min(
            means,
            key=means.get,
        )

        statements.append(
            InterpretationStatement(
                level="descriptive",
                message=(
                    f"La moyenne de {result.target_column} "
                    f"est la plus élevée pour la polarité "
                    f"'{max_group}' ({means[max_group]:.3f}) "
                    f"et la plus faible pour la polarité "
                    f"'{min_group}' ({means[min_group]:.3f})."
                ),
            )
        )

        if (
            result.anova_p_value
            is not None
        ):
            if result.anova_p_value < 0.05:
                message = (
                    "L'ANOVA met en évidence une "
                    "différence statistiquement "
                    "significative entre les groupes "
                    f"(p={result.anova_p_value:.4g})."
                )
            else:
                message = (
                    "L'ANOVA ne met pas en évidence "
                    "de différence statistiquement "
                    "significative entre les groupes "
                    f"(p={result.anova_p_value:.4g})."
                )

            statements.append(
                InterpretationStatement(
                    level="inference",
                    message=message,
                )
            )

        if (
            result.kruskal_p_value
            is not None
        ):
            statements.append(
                InterpretationStatement(
                    level="inference",
                    message=(
                        "Le test de Kruskal-Wallis donne "
                        f"p={result.kruskal_p_value:.4g}."
                    ),
                )
            )

        statements.append(
            InterpretationStatement(
                level="caution",
                message=(
                    "La polarité est issue d'un analyseur "
                    "lexical de référence. Elle ne doit pas "
                    "être assimilée à une mesure exhaustive "
                    "du sentiment ou de l'état émotionnel."
                ),
            )
        )

        return InterpretationResult(
            title=(
                "Association sentiment / "
                f"{result.target_column}"
            ),
            statements=statements,
        )

    @staticmethod
    def interpret_sentiment_categorical(
        result,
    ) -> InterpretationResult:

        statements = []

        if not result.contingency_table:
            return InterpretationResult(
                title=(
                    "Association sentiment / "
                    f"{result.target_column}"
                ),
                statements=[
                    InterpretationStatement(
                        level="warning",
                        message=(
                            "Aucune table de contingence "
                            "exploitable n'a été produite."
                        ),
                    )
                ],
            )

        if result.p_value is not None:
            if result.p_value < 0.05:
                message = (
                    "Le test du Khi² indique une "
                    "association statistiquement "
                    "significative entre la polarité "
                    f"et {result.target_column} "
                    f"(p={result.p_value:.4g})."
                )
            else:
                message = (
                    "Le test du Khi² ne met pas en "
                    "évidence d'association statistiquement "
                    "significative entre la polarité "
                    f"et {result.target_column} "
                    f"(p={result.p_value:.4g})."
                )

            statements.append(
                InterpretationStatement(
                    level="inference",
                    message=message,
                )
            )

        statements.append(
            InterpretationStatement(
                level="caution",
                message=(
                    "Une association statistique ne permet "
                    "pas d'établir une relation causale."
                ),
            )
        )

        return InterpretationResult(
            title=(
                "Association sentiment / "
                f"{result.target_column}"
            ),
            statements=statements,
        )
