"""
=========================================================
EMIDAF Framework v1.0
EQAE - Assisted Qualitative Coding
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4

from ..corpus import QualitativeSegment
from .codebook import Codebook
from .coder import QualitativeCoder


@dataclass(frozen=True)
class CodingSuggestion:
    """
    Suggestion de codage produite par une méthode
    assistée.

    Une suggestion n'est jamais considérée comme
    un codage validé tant que le chercheur ne l'a
    pas acceptée ou modifiée.
    """

    suggestion_id: str
    segment_id: str
    document_id: str
    suggested_code_id: str
    confidence: float | None = None
    rationale: str = ""
    source: str = "assisted"
    status: str = "pending"

    reviewed_code_id: str | None = None
    reviewer_note: str = ""

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(self)


class AssistedCodingManager:
    """
    Gestion du cycle de validation humaine des
    suggestions de codage assisté.
    """

    VALID_STATUSES = {
        "pending",
        "accepted",
        "modified",
        "rejected",
    }

    def __init__(
        self,
        *,
        codebook: Codebook,
        coder: QualitativeCoder,
    ) -> None:

        if not isinstance(
            codebook,
            Codebook,
        ):
            raise TypeError(
                "codebook doit être une instance "
                "de Codebook."
            )

        if not isinstance(
            coder,
            QualitativeCoder,
        ):
            raise TypeError(
                "coder doit être une instance "
                "de QualitativeCoder."
            )

        if coder.codebook is not codebook:
            raise ValueError(
                "Le coder et le gestionnaire assisté "
                "doivent utiliser le même codebook."
            )

        self.codebook = codebook
        self.coder = coder

        self._suggestions: dict[
            str,
            CodingSuggestion,
        ] = {}

        self._segments: dict[
            str,
            QualitativeSegment,
        ] = {}

    @property
    def suggestions(
        self,
    ) -> list[CodingSuggestion]:

        return list(
            self._suggestions.values()
        )

    def suggest_code(
        self,
        *,
        segment: QualitativeSegment,
        code_id: str,
        confidence: float | None = None,
        rationale: str = "",
        source: str = "assisted",
        suggestion_id: str | None = None,
    ) -> CodingSuggestion:
        """
        Crée une suggestion de codage en statut pending.
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
                "Code suggéré introuvable : "
                f"{code_id}"
            )

        if confidence is not None:

            confidence = float(
                confidence
            )

            if not (
                0.0
                <= confidence
                <= 1.0
            ):
                raise ValueError(
                    "confidence doit être comprise "
                    "entre 0 et 1."
                )

        identifier = (
            str(suggestion_id).strip()
            if suggestion_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "suggestion_id ne peut pas être vide."
            )

        if identifier in self._suggestions:
            raise ValueError(
                "Identifiant de suggestion déjà utilisé : "
                f"{identifier}"
            )

        for suggestion in (
            self._suggestions.values()
        ):
            if (
                suggestion.segment_id
                == segment.segment_id
                and suggestion.suggested_code_id
                == code_id
                and suggestion.status
                == "pending"
            ):
                raise ValueError(
                    "Une suggestion pending identique "
                    "existe déjà."
                )

        suggestion = CodingSuggestion(
            suggestion_id=identifier,
            segment_id=segment.segment_id,
            document_id=segment.document_id,
            suggested_code_id=code_id,
            confidence=confidence,
            rationale=str(
                rationale
            ).strip(),
            source=str(
                source
            ).strip() or "assisted",
        )

        self._segments[
            segment.segment_id
        ] = segment

        self._suggestions[
            identifier
        ] = suggestion

        return suggestion

    def get_suggestion(
        self,
        suggestion_id: str,
    ) -> CodingSuggestion | None:

        return self._suggestions.get(
            str(suggestion_id)
        )

    def suggestions_by_status(
        self,
        status: str,
    ) -> list[CodingSuggestion]:

        status = str(
            status
        ).strip().lower()

        if status not in self.VALID_STATUSES:
            raise ValueError(
                "Statut invalide : "
                f"{status}"
            )

        return [
            suggestion
            for suggestion
            in self._suggestions.values()
            if suggestion.status == status
        ]

    def accept(
        self,
        suggestion_id: str,
        *,
        reviewer_note: str = "",
    ) -> CodingSuggestion:
        """
        Accepte la suggestion et crée un codage
        assisté validé dans QualitativeCoder.
        """

        suggestion = (
            self._require_pending(
                suggestion_id
            )
        )

        segment = self._segments[
            suggestion.segment_id
        ]

        self.coder.assign_code(
            segment=segment,
            code_id=(
                suggestion
                .suggested_code_id
            ),
            mode="assisted",
            memo=str(
                reviewer_note
            ).strip(),
        )

        reviewed = CodingSuggestion(
            **{
                **suggestion.to_dict(),
                "status": "accepted",
                "reviewed_code_id": (
                    suggestion
                    .suggested_code_id
                ),
                "reviewer_note": str(
                    reviewer_note
                ).strip(),
            }
        )

        self._suggestions[
            suggestion.suggestion_id
        ] = reviewed

        return reviewed

    def modify(
        self,
        suggestion_id: str,
        *,
        code_id: str,
        reviewer_note: str = "",
    ) -> CodingSuggestion:
        """
        Modifie la suggestion avant validation.
        """

        suggestion = (
            self._require_pending(
                suggestion_id
            )
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
                "Code de remplacement introuvable : "
                f"{code_id}"
            )

        segment = self._segments[
            suggestion.segment_id
        ]

        self.coder.assign_code(
            segment=segment,
            code_id=code_id,
            mode="assisted",
            memo=str(
                reviewer_note
            ).strip(),
        )

        reviewed = CodingSuggestion(
            **{
                **suggestion.to_dict(),
                "status": "modified",
                "reviewed_code_id": code_id,
                "reviewer_note": str(
                    reviewer_note
                ).strip(),
            }
        )

        self._suggestions[
            suggestion.suggestion_id
        ] = reviewed

        return reviewed

    def reject(
        self,
        suggestion_id: str,
        *,
        reviewer_note: str = "",
    ) -> CodingSuggestion:
        """
        Rejette une suggestion sans créer de codage.
        """

        suggestion = (
            self._require_pending(
                suggestion_id
            )
        )

        reviewed = CodingSuggestion(
            **{
                **suggestion.to_dict(),
                "status": "rejected",
                "reviewed_code_id": None,
                "reviewer_note": str(
                    reviewer_note
                ).strip(),
            }
        )

        self._suggestions[
            suggestion.suggestion_id
        ] = reviewed

        return reviewed

    def _require_pending(
        self,
        suggestion_id: str,
    ) -> CodingSuggestion:
        """
        Vérifie qu'une suggestion existe et qu'elle
        est encore en attente de validation.
        """

        suggestion_id = str(
            suggestion_id
        )

        suggestion = self._suggestions.get(
            suggestion_id
        )

        if suggestion is None:
            raise ValueError(
                "Suggestion introuvable : "
                f"{suggestion_id}"
            )

        if suggestion.status != "pending":
            raise ValueError(
                "Cette suggestion a déjà été examinée."
            )

        return suggestion

    def to_dict(self) -> dict[str, Any]:

        return {
            "suggestions": [
                suggestion.to_dict()
                for suggestion
                in self.suggestions
            ]
        }
