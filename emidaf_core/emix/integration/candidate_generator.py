"""
=========================================================
EMIDAF Framework v1.0
EMIX - Integration Candidate Generator
=========================================================
"""

from __future__ import annotations

from uuid import uuid4

from .candidate import IntegrationCandidate
from ..sources import MixedMethodSource


class IntegrationCandidateGenerator:
    """
    Génère des rapprochements potentiels entre
    sources analytiques distinctes.

    Le générateur ne qualifie jamais automatiquement
    la relation scientifique.
    """

    def generate(
        self,
        *,
        source_1: MixedMethodSource,
        source_2: MixedMethodSource,
        element_1: str,
        element_2: str,
        rationale: str = "",
        candidate_id: str | None = None,
    ) -> IntegrationCandidate:

        if source_1.source_id == source_2.source_id:
            raise ValueError(
                "Les deux sources doivent être distinctes."
            )

        return IntegrationCandidate(
            candidate_id=(
                candidate_id
                or uuid4().hex
            ),
            source_id_1=source_1.source_id,
            source_id_2=source_2.source_id,
            element_1=element_1,
            element_2=element_2,
            rationale=rationale,
            status="pending",
        )
