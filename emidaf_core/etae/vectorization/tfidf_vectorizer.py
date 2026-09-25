"""
=========================================================
EMIDAF Framework v1.0
ETAE - TF-IDF Vectorizer
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)

from ..preprocessing import (
    TextPreprocessingConfig,
    TextPreprocessor,
)


@dataclass(frozen=True)
class TfidfTerm:
    term: str
    mean_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TfidfResult:
    text_column: str
    n_documents: int
    n_features: int
    sparsity: float
    feature_names: list[str]
    top_terms: list[TfidfTerm]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "n_documents": self.n_documents,
            "n_features": self.n_features,
            "sparsity": self.sparsity,
            "feature_names": self.feature_names,
            "top_terms": [
                item.to_dict()
                for item in self.top_terms
            ],
        }


class ETAETfidfVectorizer:
    """
    Vectorisation TF-IDF d'une colonne textuelle.
    """

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        max_features: int | None = 5000,
        min_df: int | float = 1,
        max_df: int | float = 1.0,
        ngram_range: tuple[int, int] = (1, 1),
        top_n: int = 20,
        config: TextPreprocessingConfig | None = None,
    ) -> TfidfResult:

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

        if top_n < 1:
            raise ValueError(
                "top_n doit être supérieur ou égal à 1."
            )

        preprocessor = TextPreprocessor(
            config=config
        )

        processed = preprocessor.process_series(
            dataframe[text_column]
        )

        documents = [
            item.cleaned_text
            for item in processed
            if item.cleaned_text
        ]

        if not documents:
            return TfidfResult(
                text_column=text_column,
                n_documents=0,
                n_features=0,
                sparsity=0.0,
                feature_names=[],
                top_terms=[],
            )

        vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            ngram_range=ngram_range,
            token_pattern=(
                r"(?u)\b[\wÀ-ÖØ-öø-ÿ']+\b"
            ),
        )

        matrix = vectorizer.fit_transform(
            documents
        )

        feature_names = list(
            vectorizer.get_feature_names_out()
        )

        n_documents, n_features = (
            matrix.shape
        )

        total_cells = (
            n_documents
            * n_features
        )

        non_zero = matrix.nnz

        sparsity = (
            1.0
            - (
                non_zero
                / total_cells
            )
            if total_cells
            else 0.0
        )

        mean_scores = (
            matrix.mean(axis=0)
        ).A1

        ranked_indices = (
            mean_scores.argsort()[::-1]
        )[:top_n]

        top_terms = [
            TfidfTerm(
                term=feature_names[index],
                mean_score=float(
                    mean_scores[index]
                ),
            )
            for index in ranked_indices
        ]

        return TfidfResult(
            text_column=text_column,
            n_documents=int(
                n_documents
            ),
            n_features=int(
                n_features
            ),
            sparsity=float(
                sparsity
            ),
            feature_names=feature_names,
            top_terms=top_terms,
        )

    def transform(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        max_features: int | None = 5000,
        min_df: int | float = 1,
        max_df: int | float = 1.0,
        ngram_range: tuple[int, int] = (1, 1),
        config: TextPreprocessingConfig | None = None,
    ):
        """
        Retourne la matrice TF-IDF, le vectorizer et
        les index correspondant aux documents non vides.
        """

        if text_column not in dataframe.columns:
            raise ValueError(
                f"Colonne textuelle introuvable : "
                f"{text_column}"
            )

        preprocessor = TextPreprocessor(
            config=config
        )

        processed = preprocessor.process_series(
            dataframe[text_column]
        )

        documents = []
        valid_indices = []

        for index, item in zip(
            dataframe.index,
            processed,
        ):
            if not item.cleaned_text:
                continue

            documents.append(
                item.cleaned_text
            )
            valid_indices.append(
                index
            )

        vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            ngram_range=ngram_range,
            token_pattern=(
                r"(?u)\b[\wÀ-ÖØ-öø-ÿ']+\b"
            ),
        )

        if not documents:
            return (
                None,
                vectorizer,
                valid_indices,
            )

        matrix = vectorizer.fit_transform(
            documents
        )

        return (
            matrix,
            vectorizer,
            valid_indices,
        )
