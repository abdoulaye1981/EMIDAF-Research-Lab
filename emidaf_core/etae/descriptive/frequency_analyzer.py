"""
=========================================================
EMIDAF Framework v1.0
ETAE - Frequency Analyzer
=========================================================
"""

from __future__ import annotations

from collections import Counter

import pandas as pd

from ..preprocessing import (
    TextPreprocessingConfig,
    TextPreprocessor,
)
from ..result import (
    LexicalAnalysisResult,
    LexicalItem,
)


class FrequencyAnalyzer:
    """
    Analyse les fréquences lexicales et les n-grams
    d'une colonne textuelle.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        ngram_size: int = 1,
        top_n: int | None = 20,
        config: TextPreprocessingConfig | None = None,
    ) -> LexicalAnalysisResult:

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

        if ngram_size < 1:
            raise ValueError(
                "ngram_size doit être supérieur "
                "ou égal à 1."
            )

        if top_n is not None and top_n < 1:
            raise ValueError(
                "top_n doit être supérieur "
                "ou égal à 1."
            )

        preprocessor = TextPreprocessor(
            config=config
        )

        processed = (
            preprocessor.process_series(
                dataframe[text_column]
            )
        )

        all_ngrams: list[str] = []

        valid_documents = 0

        for document in processed:
            tokens = document.tokens

            if not tokens:
                continue

            valid_documents += 1

            document_ngrams = (
                self._build_ngrams(
                    tokens,
                    ngram_size,
                )
            )

            all_ngrams.extend(
                document_ngrams
            )

        counter = Counter(
            all_ngrams
        )

        total_tokens = int(
            sum(counter.values())
        )

        vocabulary_size = int(
            len(counter)
        )

        ranked = counter.most_common(
            top_n
        )

        items = [
            LexicalItem(
                term=term,
                count=int(count),
                relative_frequency=(
                    float(
                        count
                        / total_tokens
                    )
                    if total_tokens
                    else 0.0
                ),
            )
            for term, count in ranked
        ]

        return LexicalAnalysisResult(
            text_column=text_column,
            n_documents=valid_documents,
            total_tokens=total_tokens,
            vocabulary_size=vocabulary_size,
            ngram_size=ngram_size,
            items=items,
        )

    @staticmethod
    def _build_ngrams(
        tokens: list[str],
        n: int,
    ) -> list[str]:

        if len(tokens) < n:
            return []

        return [
            " ".join(
                tokens[index:index + n]
            )
            for index in range(
                len(tokens) - n + 1
            )
        ]
