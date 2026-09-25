"""
=========================================================
EMIDAF Framework v1.0
ETAE - Text Preprocessor
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable
import re
import string

import pandas as pd


@dataclass(frozen=True)
class TextPreprocessingConfig:
    lowercase: bool = True
    remove_punctuation: bool = True
    remove_digits: bool = False
    remove_stopwords: bool = False
    preserve_negations: bool = True


@dataclass(frozen=True)
class ProcessedText:
    original_text: str
    cleaned_text: str
    tokens: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TextPreprocessor:
    """
    Prétraitement configurable du texte.

    Le texte source n'est jamais modifié.
    """

    _TOKEN_PATTERN = re.compile(
        r"\b[\wÀ-ÖØ-öø-ÿ']+\b",
        flags=re.UNICODE,
    )

    _DEFAULT_STOPWORDS = {
        "a",
        "au",
        "aux",
        "avec",
        "ce",
        "ces",
        "dans",
        "de",
        "des",
        "du",
        "elle",
        "en",
        "et",
        "eux",
        "il",
        "je",
        "la",
        "le",
        "les",
        "leur",
        "lui",
        "ma",
        "mais",
        "me",
        "mes",
        "mon",
        "ne",
        "nos",
        "notre",
        "nous",
        "on",
        "ou",
        "par",
        "pas",
        "pour",
        "que",
        "qui",
        "sa",
        "se",
        "ses",
        "son",
        "sur",
        "ta",
        "te",
        "tes",
        "toi",
        "ton",
        "tu",
        "un",
        "une",
        "vos",
        "votre",
        "vous",
    }

    _NEGATIONS = {
        "ne",
        "pas",
        "plus",
        "jamais",
        "aucun",
        "aucune",
        "ni",
        "rien",
    }

    def __init__(
        self,
        config: TextPreprocessingConfig | None = None,
        stopwords: Iterable[str] | None = None,
    ) -> None:
        self.config = (
            config
            or TextPreprocessingConfig()
        )

        self.stopwords = set(
            stopwords
            if stopwords is not None
            else self._DEFAULT_STOPWORDS
        )

        if self.config.preserve_negations:
            self.stopwords -= self._NEGATIONS

    def process_text(
        self,
        text: str,
    ) -> ProcessedText:

        original_text = str(text)

        cleaned = original_text.strip()

        if self.config.lowercase:
            cleaned = cleaned.lower()

        if self.config.remove_digits:
            cleaned = re.sub(
                r"\d+",
                " ",
                cleaned,
            )

        if self.config.remove_punctuation:
            translation = str.maketrans(
                {
                    character: " "
                    for character in string.punctuation
                    if character != "'"
                }
            )
            cleaned = cleaned.translate(
                translation
            )

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        ).strip()

        tokens = self._TOKEN_PATTERN.findall(
            cleaned
        )

        if self.config.remove_stopwords:
            tokens = [
                token
                for token in tokens
                if token.lower()
                not in self.stopwords
            ]

        cleaned_text = " ".join(
            tokens
        )

        return ProcessedText(
            original_text=original_text,
            cleaned_text=cleaned_text,
            tokens=tokens,
        )

    def process_series(
        self,
        series: pd.Series,
    ) -> list[ProcessedText]:
        """
        Prétraite une série de textes.

        Les valeurs manquantes deviennent des textes vides.
        """

        if not isinstance(
            series,
            pd.Series,
        ):
            raise TypeError(
                "series doit être une Series pandas."
            )

        results: list[ProcessedText] = []

        for value in series:
            if pd.isna(value):
                text = ""
            else:
                text = str(value)

            results.append(
                self.process_text(
                    text
                )
            )

        return results
