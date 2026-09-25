"""
=========================================================
EMIDAF Framework v1.0
ETAE - Lexicon Sentiment Analysis
=========================================================

Analyse lexicale de référence pour ETAE.

Ce composant constitue un baseline interprétable.
Il ne doit pas être assimilé à une mesure définitive
du sentiment ou de l'émotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping

import pandas as pd

from ..preprocessing import (
    TextPreprocessingConfig,
    TextPreprocessor,
)


@dataclass(frozen=True)
class DocumentSentiment:
    index: Any
    score: float
    label: str
    matched_tokens: int
    total_tokens: int
    coverage: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SentimentDistribution:
    positive: int
    neutral: int
    negative: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class SentimentAnalysisResult:
    text_column: str
    method: str

    n_documents: int
    mean_score: float

    positive_count: int
    neutral_count: int
    negative_count: int

    mean_coverage: float

    documents: list[DocumentSentiment]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "method": self.method,
            "n_documents": self.n_documents,
            "mean_score": self.mean_score,
            "positive_count": self.positive_count,
            "neutral_count": self.neutral_count,
            "negative_count": self.negative_count,
            "mean_coverage": self.mean_coverage,
            "documents": [
                document.to_dict()
                for document in self.documents
            ],
        }


class LexiconSentimentAnalyzer:
    """
    Analyse de polarité lexicale.

    Le lexique peut être remplacé ou enrichi lors
    de l'instanciation.

    Le score est normalisé par le nombre de tokens
    effectivement reconnus par le lexique.
    """

    DEFAULT_LEXICON: dict[str, float] = {
        # Positif
        "aime": 1.0,
        "aimer": 1.0,
        "agréable": 1.0,
        "bien": 0.8,
        "bon": 0.8,
        "bonne": 0.8,
        "excellent": 1.5,
        "excellente": 1.5,
        "facile": 0.7,
        "intéressant": 1.0,
        "intéressante": 1.0,
        "motivant": 1.2,
        "motivante": 1.2,
        "motivé": 1.2,
        "motivée": 1.2,
        "disponible": 0.8,
        "encourage": 1.0,
        "encourageant": 1.0,
        "réussite": 1.0,
        "satisfait": 1.0,
        "satisfaite": 1.0,

        # Négatif
        "anxieux": -1.2,
        "anxieuse": -1.2,
        "anxiété": -1.3,
        "difficile": -0.9,
        "difficulté": -0.9,
        "difficultés": -0.9,
        "échec": -1.2,
        "peur": -1.2,
        "problème": -0.8,
        "problèmes": -0.8,
        "stress": -1.2,
        "stressé": -1.2,
        "stressée": -1.2,
        "chargée": -0.7,
        "surchargée": -0.9,
        "manque": -0.8,
        "insuffisant": -0.8,
        "insuffisante": -0.8,
    }

    NEGATIONS = {
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
        *,
        lexicon: Mapping[str, float] | None = None,
        positive_threshold: float = 0.05,
        negative_threshold: float = -0.05,
        negation_window: int = 3,
    ) -> None:

        self.lexicon = {
            str(term).lower(): float(score)
            for term, score in (
                lexicon
                if lexicon is not None
                else self.DEFAULT_LEXICON
            ).items()
        }

        self.positive_threshold = float(
            positive_threshold
        )

        self.negative_threshold = float(
            negative_threshold
        )

        self.negation_window = int(
            negation_window
        )

        if (
            self.negative_threshold
            >= self.positive_threshold
        ):
            raise ValueError(
                "negative_threshold doit être "
                "strictement inférieur à "
                "positive_threshold."
            )

        if self.negation_window < 0:
            raise ValueError(
                "negation_window doit être positif "
                "ou nul."
            )

    def analyze_text(
        self,
        text: str,
        *,
        index: Any = None,
    ) -> DocumentSentiment:

        preprocessor = TextPreprocessor(
            config=TextPreprocessingConfig(
                lowercase=True,
                remove_punctuation=True,
                remove_digits=False,
                remove_stopwords=False,
                preserve_negations=True,
            )
        )

        processed = preprocessor.process_text(
            text
        )

        tokens = processed.tokens

        scores: list[float] = []

        for position, token in enumerate(
            tokens
        ):
            normalized = token.lower()

            if normalized not in self.lexicon:
                continue

            score = self.lexicon[
                normalized
            ]

            start = max(
                0,
                position
                - self.negation_window,
            )

            context = {
                item.lower()
                for item in tokens[
                    start:position
                ]
            }

            if (
                context
                & self.NEGATIONS
            ):
                score *= -1.0

            scores.append(
                float(score)
            )

        matched_tokens = len(
            scores
        )

        total_tokens = len(
            tokens
        )

        if matched_tokens == 0:
            score = 0.0
        else:
            score = float(
                sum(scores)
                / matched_tokens
            )

        coverage = (
            matched_tokens
            / total_tokens
            if total_tokens
            else 0.0
        )

        label = self._label(
            score
        )

        return DocumentSentiment(
            index=index,
            score=score,
            label=label,
            matched_tokens=matched_tokens,
            total_tokens=total_tokens,
            coverage=float(
                coverage
            ),
        )

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
    ) -> SentimentAnalysisResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
            )

        if text_column not in dataframe.columns:
            raise ValueError(
                f"Colonne textuelle introuvable : "
                f"{text_column}"
            )

        documents: list[
            DocumentSentiment
        ] = []

        for index, value in (
            dataframe[text_column]
            .items()
        ):
            if pd.isna(value):
                continue

            text = str(
                value
            ).strip()

            if not text:
                continue

            documents.append(
                self.analyze_text(
                    text,
                    index=index,
                )
            )

        if not documents:
            return SentimentAnalysisResult(
                text_column=text_column,
                method="lexicon",
                n_documents=0,
                mean_score=0.0,
                positive_count=0,
                neutral_count=0,
                negative_count=0,
                mean_coverage=0.0,
                documents=[],
            )

        positive_count = sum(
            document.label == "positive"
            for document in documents
        )

        neutral_count = sum(
            document.label == "neutral"
            for document in documents
        )

        negative_count = sum(
            document.label == "negative"
            for document in documents
        )

        mean_score = sum(
            document.score
            for document in documents
        ) / len(documents)

        mean_coverage = sum(
            document.coverage
            for document in documents
        ) / len(documents)

        return SentimentAnalysisResult(
            text_column=text_column,
            method="lexicon",
            n_documents=len(
                documents
            ),
            mean_score=float(
                mean_score
            ),
            positive_count=int(
                positive_count
            ),
            neutral_count=int(
                neutral_count
            ),
            negative_count=int(
                negative_count
            ),
            mean_coverage=float(
                mean_coverage
            ),
            documents=documents,
        )

    def _label(
        self,
        score: float,
    ) -> str:

        if (
            score
            > self.positive_threshold
        ):
            return "positive"

        if (
            score
            < self.negative_threshold
        ):
            return "negative"

        return "neutral"
