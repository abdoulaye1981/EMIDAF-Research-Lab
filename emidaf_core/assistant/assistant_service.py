from __future__ import annotations

import json
from typing import Any

from .consistency_checker import ConsistencyChecker
from .context_builder import ContextBuilder
from .provider import AIProvider
from .prompts import ASSISTANT_SYSTEM_PROMPT


class AssistantService:

    VALID_LEVELS = {
        "beginner",
        "intermediate",
        "expert",
    }

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self.provider = provider
        self.last_consistency: dict[str, Any] | None = None
        self.last_regenerated = False

    def explain(
        self,
        *,
        analyses: dict[str, Any],
        question: str,
        level: str = "intermediate",
    ) -> str:

        level = str(level).strip().lower()

        if level not in self.VALID_LEVELS:
            raise ValueError(
                f"Niveau invalide : {level}"
            )

        question = str(question).strip()

        if not question:
            raise ValueError(
                "La question ne peut pas être vide."
            )

        context = ContextBuilder.build(
            analyses
        )

        prompt = self._build_prompt(
            context=context,
            question=question,
            level=level,
        )

        generated = self.provider.generate(
            prompt,
            system_instruction=ASSISTANT_SYSTEM_PROMPT,
            temperature=0.1,
            max_output_tokens=6000,
        )

        consistency = ConsistencyChecker.check(
            generated,
            context,
        )

        self.last_regenerated = False

        if not consistency["valid"]:

            correction_prompt = (
                "La réponse précédente contient des éléments "
                "qui peuvent dépasser le contexte EMIDAF.\n\n"
                "RÉPONSE À CORRIGER :\n"
                f"{generated}\n\n"
                "ANOMALIES DÉTECTÉES :\n"
                f"{json.dumps(consistency, ensure_ascii=False)}\n\n"
                "Réécris la réponse complète.\n"
                "Conserve toutes les explications, interprétations, "
                "synthèses et conclusions qui sont réellement "
                "soutenues par le contexte.\n"
                "Supprime ou reformule uniquement les valeurs, "
                "qualifications, déductions ou recommandations "
                "qui ne sont pas présentes ou soutenues.\n"
                "Ne rends pas la réponse superficielle.\n"
                "Explique toujours tous les résultats disponibles.\n"
                "Ne fais aucune conversion numérique, approximation "
                "ou arrondi.\n"
                "Conserve chaque valeur exactement comme dans le contexte.\n"
                "Supprime toute relation explicative entre modules qui "
                "n\'est pas explicitement démontrée dans le contexte.\n"
                "Tu peux comparer des résultats, mais ne prétends jamais "
                "que l\'un explique, cause, justifie ou produit l\'autre "
                "sans preuve explicite dans le contexte.\n"
                "N\'introduis aucun seuil conventionnel, benchmark, "
                "plage numérique ou valeur théorique absente.\n"
                "Même pour expliquer une métrique, n\'ajoute pas ses "
                "bornes numériques si elles ne figurent pas dans le contexte.\n"
                "Ne développe jamais un acronyme EMIDAF si son intitulé "
                "complet n\'est pas fourni dans le contexte.\n"
                "Ne déduis jamais une méthode scientifique à partir du "
                "nom ou de l\'acronyme d\'un module.\n"
                "N\'introduis aucun exemple concret absent du contexte.\n\n"
                "CONTEXTE EMIDAF :\n"
                + json.dumps(
                    context,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
            )

            generated = self.provider.generate(
                correction_prompt,
                system_instruction=ASSISTANT_SYSTEM_PROMPT,
                temperature=0.0,
                max_output_tokens=6000,
            )

            consistency = ConsistencyChecker.check(
                generated,
                context,
            )

            self.last_regenerated = True

        self.last_consistency = consistency

        return generated

    @staticmethod
    def _build_prompt(
        *,
        context: dict[str, Any],
        question: str,
        level: str,
    ) -> str:

        return (
            f"NIVEAU UTILISATEUR : {level}\n\n"
            f"QUESTION DE L'UTILISATEUR :\n"
            f"{question}\n\n"
            "CONSIGNE DE RESTITUTION :\n"
            "Explique et interprète TOUS les résultats "
            "pertinents présents dans le contexte EMIDAF.\n"
            "Ne te limite pas à répéter les valeurs.\n"
            "Développe leur signification, leurs relations, "
            "leur synthèse et les conclusions directement "
            "soutenues par les résultats.\n"
            "Lorsque cela est pertinent, structure en :\n"
            "1. observations factuelles ;\n"
            "2. explication des résultats ;\n"
            "3. interprétation ;\n"
            "4. synthèse ;\n"
            "5. conclusion ;\n"
            "6. limites et précautions.\n"
            "Exploite pleinement le contexte fourni.\n"
            "Ne sors jamais du contexte EMIDAF.\n"
            "N'invente aucun résultat, aucune valeur, "
            "aucune relation ni aucune réponse absente.\n"
            "N'effectue aucun nouveau calcul scientifique.\n"
            "Ne modifie aucune valeur EMIDAF.\n"
            "Si une information est absente, signale-le.\n\n"
            "CONTEXTE EMIDAF :\n"
            + json.dumps(
                context,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )
