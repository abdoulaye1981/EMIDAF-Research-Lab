"""
=========================================================
EMIDAF Framework v1.0
EQAE - Quotation Manager
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4

from ..coding import QualitativeCoder
from ..corpus import QualitativeSegment
from ..themes import ThematicAnalysis


@dataclass(frozen=True)
class QualitativeQuotation:
    """
    Verbatim ou extrait retenu dans l'analyse qualitative.

    Une quotation référence un segment existant.
    Elle peut être associée à un ou plusieurs codes
    et être mobilisée comme élément de preuve pour
    un thème qualitatif.
    """

    quotation_id: str
    segment_id: str
    document_id: str
    text: str
    note: str = ""

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(self)


class QuotationManager:
    """
    Gestion des verbatims EQAE et récupération
    des extraits associés aux codes et thèmes.
    """

    def __init__(
        self,
        coder: QualitativeCoder,
        thematic_analysis: ThematicAnalysis,
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
            coder.codebook
            is not thematic_analysis.codebook
        ):
            raise ValueError(
                "Le coder et l'analyse thématique "
                "doivent utiliser le même codebook."
            )

        self.coder = coder
        self.thematic_analysis = (
            thematic_analysis
        )

        self._segments: dict[
            str,
            QualitativeSegment,
        ] = {}

        self._quotations: dict[
            str,
            QualitativeQuotation,
        ] = {}

    @property
    def quotations(
        self,
    ) -> list[QualitativeQuotation]:

        return list(
            self._quotations.values()
        )

    def register_segment(
        self,
        segment: QualitativeSegment,
    ) -> None:
        """
        Enregistre un segment pour permettre
        sa récupération ultérieure.
        """

        if not isinstance(
            segment,
            QualitativeSegment,
        ):
            raise TypeError(
                "segment doit être une instance "
                "de QualitativeSegment."
            )

        existing = self._segments.get(
            segment.segment_id
        )

        if (
            existing is not None
            and existing != segment
        ):
            raise ValueError(
                "Un autre segment utilise déjà "
                "cet identifiant : "
                f"{segment.segment_id}"
            )

        self._segments[
            segment.segment_id
        ] = segment

    def add_quotation(
        self,
        *,
        segment: QualitativeSegment,
        note: str = "",
        quotation_id: str | None = None,
    ) -> QualitativeQuotation:
        """
        Retient un segment comme verbatim analytique.
        """

        self.register_segment(
            segment
        )

        identifier = (
            str(quotation_id).strip()
            if quotation_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "quotation_id ne peut pas être vide."
            )

        if identifier in self._quotations:
            raise ValueError(
                "Identifiant de verbatim déjà utilisé : "
                f"{identifier}"
            )

        for quotation in (
            self._quotations.values()
        ):
            if (
                quotation.segment_id
                == segment.segment_id
            ):
                raise ValueError(
                    "Ce segment est déjà enregistré "
                    "comme verbatim."
                )

        quotation = QualitativeQuotation(
            quotation_id=identifier,
            segment_id=segment.segment_id,
            document_id=segment.document_id,
            text=segment.text,
            note=str(
                note
            ).strip(),
        )

        self._quotations[
            identifier
        ] = quotation

        return quotation

    def get_quotation(
        self,
        quotation_id: str,
    ) -> QualitativeQuotation | None:

        return self._quotations.get(
            str(quotation_id)
        )

    def quotations_for_code(
        self,
        code_id: str,
    ) -> list[QualitativeQuotation]:
        """
        Retourne les verbatims dont les segments
        portent le code demandé.
        """

        code_id = str(
            code_id
        )

        if (
            self.coder.codebook.get_code(
                code_id
            )
            is None
        ):
            raise ValueError(
                "Code introuvable : "
                f"{code_id}"
            )

        segment_ids = {
            assignment.segment_id
            for assignment
            in self.coder.assignments
            if assignment.code_id == code_id
        }

        return [
            quotation
            for quotation
            in self._quotations.values()
            if (
                quotation.segment_id
                in segment_ids
            )
        ]

    def quotations_for_theme(
        self,
        theme_id: str,
    ) -> list[QualitativeQuotation]:
        """
        Retourne les verbatims associés à l'ensemble
        des codes reliés à un thème.
        """

        code_ids = set(
            self.thematic_analysis
            .codes_for_theme(
                theme_id
            )
        )

        if not code_ids:
            return []

        segment_ids = {
            assignment.segment_id
            for assignment
            in self.coder.assignments
            if (
                assignment.code_id
                in code_ids
            )
        }

        return [
            quotation
            for quotation
            in self._quotations.values()
            if (
                quotation.segment_id
                in segment_ids
            )
        ]

    def quotations_for_document(
        self,
        document_id: str,
    ) -> list[QualitativeQuotation]:
        """
        Retourne les verbatims provenant
        d'un document.
        """

        document_id = str(
            document_id
        )

        return [
            quotation
            for quotation
            in self._quotations.values()
            if (
                quotation.document_id
                == document_id
            )
        ]

    def remove_quotation(
        self,
        quotation_id: str,
    ) -> QualitativeQuotation:
        """
        Retire un verbatim de la sélection analytique.
        """

        quotation_id = str(
            quotation_id
        )

        if (
            quotation_id
            not in self._quotations
        ):
            raise ValueError(
                "Verbatim introuvable : "
                f"{quotation_id}"
            )

        return self._quotations.pop(
            quotation_id
        )

    def to_dict(self):
        return {
            "quotations": [
                quotation.to_dict()
                for quotation
                in self.quotations
            ]
        }
