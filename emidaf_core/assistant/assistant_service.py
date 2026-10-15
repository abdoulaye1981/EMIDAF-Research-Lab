from __future__ import annotations

import json
from typing import Any

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

        prompt = (
            f"NIVEAU UTILISATEUR : {level}\n\n"
            f"QUESTION DE L'UTILISATEUR :\n{question}\n\n"
            "CONSIGNE DE RESTITUTION :\n"
            "Analyse uniquement les résultats présents dans le contexte.\n"
            "Lorsque cela est pertinent, présente :\n"
            "1. les observations factuelles ;\n"
            "2. leur interprétation ;\n"
            "3. une conclusion soutenue par les résultats ;\n"
            "4. les limites et précautions.\n"
            "Ne calcule rien.\n"
            "N'invente aucun résultat.\n"
            "Ne modifie aucune valeur.\n"
            "Ne sors pas du contexte EMIDAF.\n\n"
            "CONTEXTE EMIDAF :\n"
            + json.dumps(
                context,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return self.provider.generate(
            prompt,
            system_instruction=ASSISTANT_SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=2500,
        )
