"""
=========================================================
EMIDAF Framework v1.0
ETAE - Corpus Profiler
=========================================================
"""

from __future__ import annotations

import re

import numpy as np
import pandas as pd

from ..result import CorpusProfileResult


class CorpusProfiler:
    """
    Produit le profil descriptif d'une colonne textuelle.

    Cette première version reste volontairement indépendante
    de toute bibliothèque NLP externe.
    """

    _TOKEN_PATTERN = re.compile(
        r"\b[\wÀ-ÖØ-öø-ÿ']+\b",
        flags=re.UNICODE,
    )

    def profile(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
    ) -> CorpusProfileResult:

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

        series = dataframe[text_column]

        n_documents = int(len(series))
        n_missing = int(series.isna().sum())

        non_missing = series.dropna().astype(str)

        stripped = non_missing.str.strip()

        empty_mask = stripped.eq("")
        n_empty = int(empty_mask.sum())

        valid = stripped[
            ~empty_mask
        ]

        n_valid_documents = int(len(valid))

        if n_valid_documents == 0:
            return CorpusProfileResult(
                text_column=text_column,
                n_documents=n_documents,
                n_valid_documents=0,
                n_missing=n_missing,
                n_empty=n_empty,
                total_characters=0,
                total_words=0,
                vocabulary_size=0,
                mean_characters=0.0,
                median_characters=0.0,
                mean_words=0.0,
                median_words=0.0,
                lexical_diversity=0.0,
            )

        character_counts = valid.str.len()

        tokenized = [
            self._tokenize(text)
            for text in valid
        ]

        word_counts = np.array(
            [
                len(tokens)
                for tokens in tokenized
            ],
            dtype=float,
        )

        all_tokens = [
            token.lower()
            for tokens in tokenized
            for token in tokens
        ]

        total_words = len(all_tokens)

        vocabulary = set(
            all_tokens
        )

        vocabulary_size = len(
            vocabulary
        )

        lexical_diversity = (
            vocabulary_size / total_words
            if total_words
            else 0.0
        )

        return CorpusProfileResult(
            text_column=text_column,
            n_documents=n_documents,
            n_valid_documents=n_valid_documents,
            n_missing=n_missing,
            n_empty=n_empty,
            total_characters=int(
                character_counts.sum()
            ),
            total_words=int(
                total_words
            ),
            vocabulary_size=int(
                vocabulary_size
            ),
            mean_characters=float(
                character_counts.mean()
            ),
            median_characters=float(
                character_counts.median()
            ),
            mean_words=float(
                word_counts.mean()
            ),
            median_words=float(
                np.median(word_counts)
            ),
            lexical_diversity=float(
                lexical_diversity
            ),
        )

    @classmethod
    def _tokenize(
        cls,
        text: str,
    ) -> list[str]:
        return cls._TOKEN_PATTERN.findall(
            text
        )
