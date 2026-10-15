from __future__ import annotations

from .provider import AIProvider


class FakeProvider(AIProvider):
    """
    Provider de test pour EMIDAF.

    Permet de tester l'architecture sans dépendre
    d'une API externe.
    """

    def available(self) -> bool:
        return True

    def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 4096,
    ) -> str:

        return (
            "Réponse simulée EMIDAF.\n\n"
            "Le contexte fourni a été reçu correctement. "
            "Aucun recalcul scientifique n'a été effectué."
        )
