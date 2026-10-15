from __future__ import annotations

import os

from .provider import AIProvider


class GeminiProvider(AIProvider):

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:

        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
        )

        self.model = (
            model
            or os.environ.get("GEMINI_MODEL")
            or "gemini-flash-latest"
        )

    def available(self) -> bool:

        if not self.api_key:
            return False

        try:
            from google import genai  # noqa: F401
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
                "GEMINI_API_KEY n'est pas configurée."
            )

        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "Le package google-genai n'est pas installé."
            ) from exc

        client = genai.Client(
            api_key=self.api_key
        )

        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=float(temperature),
                    max_output_tokens=int(max_output_tokens),
                ),
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini n'a retourné aucun texte."
                )

            return str(text).strip()

        finally:
            close = getattr(client, "close", None)

            if callable(close):
                close()
