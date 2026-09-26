"""
=========================================================
EMIDAF Framework v1.0
EQAE - Code Cooccurrence Analyzer
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any

from ..coding import QualitativeCoder


@dataclass(frozen=True)
class CodeCooccurrence:
    """
    Cooccurrence observée entre deux codes qualitatifs.
    """

    code_id_1: str
    code_id_2: str
    count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "code_id_1": self.code_id_1,
            "code_id_2": self.code_id_2,
            "count": self.count,
        }


class CooccurrenceAnalyzer:
    """
    Analyse les cooccurrences de codes dans les segments
    ou les documents.
    """

    VALID_LEVELS = {
        "segment",
        "document",
    }

    def __init__(
        self,
        coder: QualitativeCoder,
    ) -> None:

        if not isinstance(
            coder,
            QualitativeCoder,
        ):
            raise TypeError(
                "coder doit être une instance "
                "de QualitativeCoder."
            )

        self.coder = coder

    def analyze(
        self,
        *,
        level: str = "segment",
    ) -> list[CodeCooccurrence]:
        """
        Calcule les cooccurrences de codes.

        level="segment" :
            codes présents dans un même segment.

        level="document" :
            codes présents dans un même document.
        """

        level = str(
            level
        ).strip().lower()

        if level not in self.VALID_LEVELS:
            raise ValueError(
                "Niveau de cooccurrence invalide : "
                f"{level}"
            )

        grouped: dict[
            str,
            set[str],
        ] = {}

        for assignment in self.coder.assignments:

            if level == "segment":
                key = assignment.segment_id
            else:
                key = assignment.document_id

            grouped.setdefault(
                key,
                set(),
            ).add(
                assignment.code_id
            )

        counts: dict[
            tuple[str, str],
            int,
        ] = {}

        for code_ids in grouped.values():

            ordered = sorted(
                code_ids
            )

            for pair in combinations(
                ordered,
                2,
            ):
                counts[pair] = (
                    counts.get(
                        pair,
                        0,
                    )
                    + 1
                )

        return [
            CodeCooccurrence(
                code_id_1=pair[0],
                code_id_2=pair[1],
                count=count,
            )
            for pair, count
            in sorted(
                counts.items()
            )
        ]

    def matrix(
        self,
        *,
        level: str = "segment",
    ) -> dict[str, dict[str, int]]:
        """
        Produit une matrice symétrique de cooccurrence.
        """

        code_ids = sorted(
            code.code_id
            for code
            in self.coder.codebook.codes
        )

        matrix = {
            code_id: {
                other_id: 0
                for other_id
                in code_ids
            }
            for code_id
            in code_ids
        }

        for item in self.analyze(
            level=level
        ):
            matrix[
                item.code_id_1
            ][
                item.code_id_2
            ] = item.count

            matrix[
                item.code_id_2
            ][
                item.code_id_1
            ] = item.count

        return matrix

    def to_dict(
        self,
        *,
        level: str = "segment",
    ) -> dict[str, Any]:
        """
        Sérialise les cooccurrences et la matrice.
        """

        results = self.analyze(
            level=level
        )

        return {
            "level": level,
            "cooccurrences": [
                item.to_dict()
                for item in results
            ],
            "matrix": self.matrix(
                level=level
            ),
        }
