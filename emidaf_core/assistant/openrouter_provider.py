from __future__ import annotations

import os

from .provider import AIProvider


class OpenRouterProvider(AIProvider):
    """
    Provider OpenRouter pour EMIDAF.

    Usage prévu :
    - Assistant contextuel ;
    - interprétation/synthèse de résultats EMIDAF ;
    - enrichissement rédactionnel des rapports.

    Aucun calcul scientifique ne doit être délégué au provider.
    """

    DEFAULT_MODELS = (
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "poolside/laguna-s-2.1:free",
    )

    def __init__(
        self,
        *,
        api_key: str | None = None,
        models: tuple[str, ...] | list[str] | None = None,
    ) -> None:

        self.api_key = (
            api_key
            or os.environ.get("OPENROUTER_API_KEY")
        )

        env_models = os.environ.get("OPENROUTER_MODELS")

        if models:
            self.models = tuple(models)

        elif env_models:
            self.models = tuple(
                model.strip()
                for model in env_models.split(",")
                if model.strip()
            )

        else:
            self.models = self.DEFAULT_MODELS

        self.last_model: str | None = None

    def available(self) -> bool:

        if not self.api_key:
            return False

        try:
            from openai import OpenAI  # noqa: F401
        except ImportError:
            return False

        return True

    def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 4096,
    ) -> str:

        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY n'est pas configurée."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Le package openai n'est pas installé."
            ) from exc

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=25.0,
            max_retries=0,
        )

        messages: list[dict[str, str]] = []

        if system_instruction:
            messages.append(
                {
                    "role": "system",
                    "content": system_instruction,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        errors: list[str] = []

        for model in self.models:

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=float(temperature),
                    max_tokens=int(max_output_tokens),
                )

                if not response.choices:
                    errors.append(
                        f"{model}: aucune réponse"
                    )
                    continue

                content = response.choices[0].message.content

                if not content:
                    errors.append(
                        f"{model}: contenu vide"
                    )
                    continue

                self.last_model = (
                    getattr(response, "model", None)
                    or model
                )

                return str(content).strip()

            except Exception as exc:
                errors.append(
                    f"{model}: {type(exc).__name__}"
                )

        raise RuntimeError(
            "Aucun modèle OpenRouter gratuit n'a pu répondre. "
            + " | ".join(errors)
        )
