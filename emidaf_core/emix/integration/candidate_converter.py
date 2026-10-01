"""
=========================================================
EMIDAF Framework v1.0
EMIX - Candidate to Integration Link Converter
=========================================================
"""

from __future__ import annotations

from uuid import uuid4

from .candidate_manager import (
    IntegrationCandidateManager,
)
from .integrator import (
    IntegrationLink,
    VALID_RELATION_TYPES,
)


class CandidateToLinkConverter:
    """
    Convertit un candidat accepté en IntegrationLink.

    Le type de relation doit être explicitement
    fourni par le chercheur.
    """

    def __init__(
        self,
        candidate_manager: IntegrationCandidateManager,
    ) -> None:

        self.candidate_manager = (
            candidate_manager
        )

    def convert(
        self,
        *,
        candidate_id: str,
        relation_type: str,
        researcher_note: str = "",
        link_id: str | None = None,
        validated: bool = True,
    ) -> IntegrationLink:

        candidate = (
            self.candidate_manager.get(
                candidate_id
            )
        )

        if candidate.status != "accepted":
            raise ValueError(
                "Seul un candidat accepté peut être "
                "converti en lien d'intégration."
            )

        if relation_type not in VALID_RELATION_TYPES:
            raise ValueError(
                f"Type de relation invalide : "
                f"{relation_type}"
            )

        return IntegrationLink(
            link_id=(
                link_id
                or uuid4().hex
            ),
            source_id_1=(
                candidate.source_id_1
            ),
            source_id_2=(
                candidate.source_id_2
            ),
            element_1=(
                candidate.element_1
            ),
            element_2=(
                candidate.element_2
            ),
            relation_type=relation_type,
            researcher_note=researcher_note,
            candidate_id=candidate.candidate_id,
            validated=validated,
        )
