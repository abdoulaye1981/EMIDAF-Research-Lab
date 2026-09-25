"""
=========================================================
EMIDAF Framework v1.0
ETAE Result Objects
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class CorpusProfileResult:
    """
    Résultat du profil descriptif d'un corpus textuel.
    """

    text_column: str

    n_documents: int
    n_valid_documents: int
    n_missing: int
    n_empty: int

    total_characters: int
    total_words: int
    vocabulary_size: int

    mean_characters: float
    median_characters: float

    mean_words: float
    median_words: float

    lexical_diversity: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LexicalItem:
    """
    Élément lexical et sa fréquence dans le corpus.
    """

    term: str
    count: int
    relative_frequency: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LexicalAnalysisResult:
    """
    Résultat d'une analyse de fréquences lexicales.
    """

    text_column: str
    n_documents: int
    total_tokens: int
    vocabulary_size: int
    ngram_size: int
    items: list[LexicalItem]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "n_documents": self.n_documents,
            "total_tokens": self.total_tokens,
            "vocabulary_size": self.vocabulary_size,
            "ngram_size": self.ngram_size,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }
