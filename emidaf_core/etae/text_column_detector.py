"""
=========================================================
EMIDAF Framework v1.0
ETAE - Text Column Detector
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class TextColumnCandidate:
    """
    Diagnostic d'une colonne candidate à l'analyse textuelle.
    """

    column: str
    is_text: bool
    n_non_missing: int
    n_unique: int
    unique_ratio: float
    mean_characters: float
    max_characters: int
    mean_words: float
    space_ratio: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "column": self.column,
            "is_text": self.is_text,
            "n_non_missing": self.n_non_missing,
            "n_unique": self.n_unique,
            "unique_ratio": self.unique_ratio,
            "mean_characters": self.mean_characters,
            "max_characters": self.max_characters,
            "mean_words": self.mean_words,
            "space_ratio": self.space_ratio,
        }


class TextColumnDetector:
    """
    Détecte les colonnes contenant vraisemblablement
    du texte libre.

    Le détecteur distingue notamment :
    - texte libre ;
    - variables catégorielles textuelles ;
    - identifiants ou variables numériques.
    """

    def __init__(
        self,
        *,
        min_mean_characters: float = 20.0,
        min_mean_words: float = 3.0,
        min_space_ratio: float = 0.50,
        min_unique_ratio: float = 0.05,
    ) -> None:
        self.min_mean_characters = float(
            min_mean_characters
        )
        self.min_mean_words = float(
            min_mean_words
        )
        self.min_space_ratio = float(
            min_space_ratio
        )
        self.min_unique_ratio = float(
            min_unique_ratio
        )

    def detect(
        self,
        dataframe: pd.DataFrame,
    ) -> list[TextColumnCandidate]:
        """
        Analyse les colonnes compatibles avec du texte.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
            )

        candidates: list[
            TextColumnCandidate
        ] = []

        for column in dataframe.columns:
            series = dataframe[column]

            if not self._is_string_like(
                series
            ):
                continue

            candidate = self._evaluate(
                column,
                series,
            )

            candidates.append(
                candidate
            )

        return candidates

    def text_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> list[str]:
        """
        Retourne uniquement les colonnes détectées
        comme texte libre.
        """

        return [
            candidate.column
            for candidate in self.detect(
                dataframe
            )
            if candidate.is_text
        ]

    def _evaluate(
        self,
        column: str,
        series: pd.Series,
    ) -> TextColumnCandidate:

        non_missing = (
            series
            .dropna()
            .astype(str)
            .str.strip()
        )

        non_missing = non_missing[
            non_missing.ne("")
        ]

        n_non_missing = int(
            len(non_missing)
        )

        if n_non_missing == 0:
            return TextColumnCandidate(
                column=column,
                is_text=False,
                n_non_missing=0,
                n_unique=0,
                unique_ratio=0.0,
                mean_characters=0.0,
                max_characters=0,
                mean_words=0.0,
                space_ratio=0.0,
            )

        character_counts = (
            non_missing.str.len()
        )

        word_counts = (
            non_missing
            .str.split()
            .str.len()
        )

        n_unique = int(
            non_missing.nunique()
        )

        unique_ratio = (
            n_unique
            / n_non_missing
        )

        mean_characters = float(
            character_counts.mean()
        )

        max_characters = int(
            character_counts.max()
        )

        mean_words = float(
            word_counts.mean()
        )

        space_ratio = float(
            non_missing.str.contains(
                r"\s",
                regex=True,
            ).mean()
        )

        is_text = bool(
            mean_characters
            >= self.min_mean_characters
            and mean_words
            >= self.min_mean_words
            and space_ratio
            >= self.min_space_ratio
            and unique_ratio
            >= self.min_unique_ratio
        )

        return TextColumnCandidate(
            column=column,
            is_text=is_text,
            n_non_missing=n_non_missing,
            n_unique=n_unique,
            unique_ratio=float(
                unique_ratio
            ),
            mean_characters=mean_characters,
            max_characters=max_characters,
            mean_words=mean_words,
            space_ratio=space_ratio,
        )

    @staticmethod
    def _is_string_like(
        series: pd.Series,
    ) -> bool:
        return bool(
            pd.api.types.is_object_dtype(
                series.dtype
            )
            or pd.api.types.is_string_dtype(
                series.dtype
            )
        )
