"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Coder
=========================================================
"""

from __future__ import annotations

from uuid import uuid4

from ..corpus import QualitativeSegment
from ..result import CodingAssignmentResult
from .codebook import Codebook


class QualitativeCoder:
    """
    Service de codage qualitatif manuel.

    Le coder associe un ou plusieurs codes
    à des segments du corpus.
    """

    VALID_MODES = {
        "manual",
        "assisted",
        "imported",
    }

    def __init__(
        self,
        codebook: Codebook,
    ) -> None:

        if not isinstance(
            codebook,
            Codebook,
        ):
            raise TypeError(
                "codebook doit être une instance de Codebook."
            )

        self.codebook = codebook

        self._assignments: dict[
            str,
            CodingAssignmentResult,
        ] = {}

    @property
    def assignments(
        self,
    ) -> list[CodingAssignmentResult]:

        return list(
            self._assignments.values()
        )

    def assign_code(
        self,
        *,
        segment: QualitativeSegment,
        code_id: str,
        mode: str = "manual",
        memo: str = "",
        assignment_id: str | None = None,
    ) -> CodingAssignmentResult:
        """
        Affecte un code existant à un segment.
        """

        if not isinstance(
            segment,
            QualitativeSegment,
        ):
            raise TypeError(
                "segment doit être une instance "
                "de QualitativeSegment."
            )

        code_id = str(
            code_id
        ).strip()

        if (
            self.codebook.get_code(
                code_id
            )
            is None
        ):
            raise ValueError(
                "Code inconnu : "
                f"{code_id}"
            )

        mode = str(
            mode
        ).strip().lower()

        if mode not in self.VALID_MODES:
            raise ValueError(
                "Mode de codage invalide : "
                f"{mode}"
            )

        identifier = (
            str(assignment_id).strip()
            if assignment_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "assignment_id ne peut pas être vide."
            )

        if identifier in self._assignments:
            raise ValueError(
                "Identifiant de codage déjà utilisé : "
                f"{identifier}"
            )

        for assignment in (
            self._assignments.values()
        ):
            if (
                assignment.segment_id
                == segment.segment_id
                and assignment.code_id
                == code_id
            ):
                raise ValueError(
                    "Ce code est déjà affecté "
                    "à ce segment."
                )

        result = CodingAssignmentResult(
            assignment_id=identifier,
            segment_id=segment.segment_id,
            document_id=segment.document_id,
            code_id=code_id,
            mode=mode,
            memo=str(
                memo
            ).strip(),
        )

        self._assignments[
            identifier
        ] = result

        return result

    def remove_assignment(
        self,
        assignment_id: str,
    ) -> CodingAssignmentResult:
        """
        Supprime une affectation de code.
        """

        assignment_id = str(
            assignment_id
        )

        if (
            assignment_id
            not in self._assignments
        ):
            raise ValueError(
                "Affectation introuvable : "
                f"{assignment_id}"
            )

        return self._assignments.pop(
            assignment_id
        )

    def assignments_for_segment(
        self,
        segment_id: str,
    ) -> list[CodingAssignmentResult]:
        """
        Retourne les codes affectés à un segment.
        """

        segment_id = str(
            segment_id
        )

        return [
            assignment
            for assignment
            in self._assignments.values()
            if (
                assignment.segment_id
                == segment_id
            )
        ]

    def to_dict(self):
        return {
            "assignments": [
                assignment.to_dict()
                for assignment
                in self.assignments
            ]
        }
