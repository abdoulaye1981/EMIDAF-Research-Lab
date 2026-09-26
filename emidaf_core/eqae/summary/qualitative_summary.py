"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Summary
=========================================================
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from ..coding import (
    AssistedCodingManager,
    QualitativeCoder,
)
from ..quotations import QuotationManager
from ..themes import ThematicAnalysis


@dataclass(frozen=True)
class CodeSummary:
    """
    Synthèse descriptive d'un code qualitatif.
    """

    code_id: str
    name: str
    n_assignments: int
    n_documents: int
    n_segments: int
    n_quotations: int

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "code_id": self.code_id,
            "name": self.name,
            "n_assignments": self.n_assignments,
            "n_documents": self.n_documents,
            "n_segments": self.n_segments,
            "n_quotations": self.n_quotations,
        }


@dataclass(frozen=True)
class ThemeSummary:
    """
    Synthèse descriptive d'un thème qualitatif.
    """

    theme_id: str
    name: str
    n_codes: int
    n_assignments: int
    n_documents: int
    n_quotations: int

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "theme_id": self.theme_id,
            "name": self.name,
            "n_codes": self.n_codes,
            "n_assignments": self.n_assignments,
            "n_documents": self.n_documents,
            "n_quotations": self.n_quotations,
        }


class QualitativeSummaryBuilder:
    """
    Construit une synthèse descriptive EQAE.

    Cette synthèse ne remplace pas l'interprétation
    du chercheur. Elle organise les résultats produits
    par les différentes briques qualitatives.
    """

    def __init__(
        self,
        *,
        coder: QualitativeCoder,
        thematic_analysis: ThematicAnalysis,
        quotation_manager: QuotationManager | None = None,
        assisted_coding: AssistedCodingManager | None = None,
    ) -> None:

        if not isinstance(
            coder,
            QualitativeCoder,
        ):
            raise TypeError(
                "coder doit être une instance "
                "de QualitativeCoder."
            )

        if not isinstance(
            thematic_analysis,
            ThematicAnalysis,
        ):
            raise TypeError(
                "thematic_analysis doit être une instance "
                "de ThematicAnalysis."
            )

        if (
            thematic_analysis.codebook
            is not coder.codebook
        ):
            raise ValueError(
                "Le coder et l'analyse thématique "
                "doivent utiliser le même codebook."
            )

        if (
            quotation_manager is not None
            and quotation_manager.coder is not coder
        ):
            raise ValueError(
                "quotation_manager doit utiliser "
                "le même coder."
            )

        if (
            assisted_coding is not None
            and assisted_coding.coder is not coder
        ):
            raise ValueError(
                "assisted_coding doit utiliser "
                "le même coder."
            )

        self.coder = coder
        self.thematic_analysis = (
            thematic_analysis
        )
        self.quotation_manager = (
            quotation_manager
        )
        self.assisted_coding = (
            assisted_coding
        )

    def summarize_codes(
        self,
    ) -> list[CodeSummary]:
        """
        Produit les indicateurs descriptifs par code.
        """

        assignments_by_code = defaultdict(
            list
        )

        for assignment in self.coder.assignments:
            assignments_by_code[
                assignment.code_id
            ].append(
                assignment
            )

        results = []

        for code in self.coder.codebook.codes:

            assignments = (
                assignments_by_code[
                    code.code_id
                ]
            )

            documents = {
                assignment.document_id
                for assignment
                in assignments
            }

            segments = {
                assignment.segment_id
                for assignment
                in assignments
            }

            n_quotations = 0

            if (
                self.quotation_manager
                is not None
            ):
                n_quotations = len(
                    self.quotation_manager
                    .quotations_for_code(
                        code.code_id
                    )
                )

            results.append(
                CodeSummary(
                    code_id=code.code_id,
                    name=code.name,
                    n_assignments=len(
                        assignments
                    ),
                    n_documents=len(
                        documents
                    ),
                    n_segments=len(
                        segments
                    ),
                    n_quotations=n_quotations,
                )
            )

        return results

    def summarize_themes(
        self,
    ) -> list[ThemeSummary]:
        """
        Produit les indicateurs descriptifs par thème.
        """

        assignments_by_code = defaultdict(
            list
        )

        for assignment in self.coder.assignments:
            assignments_by_code[
                assignment.code_id
            ].append(
                assignment
            )

        results = []

        for theme in (
            self.thematic_analysis.themes
        ):

            code_ids = set(
                self.thematic_analysis
                .codes_for_theme(
                    theme.theme_id
                )
            )

            assignments = []

            for code_id in code_ids:
                assignments.extend(
                    assignments_by_code[
                        code_id
                    ]
                )

            documents = {
                assignment.document_id
                for assignment
                in assignments
            }

            n_quotations = 0

            if (
                self.quotation_manager
                is not None
            ):
                n_quotations = len(
                    self.quotation_manager
                    .quotations_for_theme(
                        theme.theme_id
                    )
                )

            results.append(
                ThemeSummary(
                    theme_id=theme.theme_id,
                    name=theme.name,
                    n_codes=len(
                        code_ids
                    ),
                    n_assignments=len(
                        assignments
                    ),
                    n_documents=len(
                        documents
                    ),
                    n_quotations=n_quotations,
                )
            )

        return results

    def assisted_status_counts(
        self,
    ) -> dict[str, int]:
        """
        Compte les suggestions assistées par statut.
        """

        counts = {
            "pending": 0,
            "accepted": 0,
            "modified": 0,
            "rejected": 0,
        }

        if self.assisted_coding is None:
            return counts

        raw = Counter(
            suggestion.status
            for suggestion
            in self.assisted_coding.suggestions
        )

        for status in counts:
            counts[status] = int(
                raw.get(
                    status,
                    0,
                )
            )

        return counts

    def global_indicators(
        self,
    ) -> dict[str, int]:
        """
        Produit les indicateurs globaux EQAE.
        """

        assignments = self.coder.assignments

        documents = {
            assignment.document_id
            for assignment
            in assignments
        }

        segments = {
            assignment.segment_id
            for assignment
            in assignments
        }

        n_quotations = 0

        if (
            self.quotation_manager
            is not None
        ):
            n_quotations = len(
                self.quotation_manager.quotations
            )

        n_suggestions = 0

        if self.assisted_coding is not None:
            n_suggestions = len(
                self.assisted_coding.suggestions
            )

        return {
            "n_codes": len(
                self.coder.codebook.codes
            ),
            "n_themes": len(
                self.thematic_analysis.themes
            ),
            "n_assignments": len(
                assignments
            ),
            "n_documents_coded": len(
                documents
            ),
            "n_segments_coded": len(
                segments
            ),
            "n_quotations": n_quotations,
            "n_assisted_suggestions": (
                n_suggestions
            ),
        }

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Produit la synthèse EQAE complète.
        """

        return {
            "global": (
                self.global_indicators()
            ),
            "codes": [
                result.to_dict()
                for result
                in self.summarize_codes()
            ],
            "themes": [
                result.to_dict()
                for result
                in self.summarize_themes()
            ],
            "assisted_coding": (
                self.assisted_status_counts()
            ),
        }
