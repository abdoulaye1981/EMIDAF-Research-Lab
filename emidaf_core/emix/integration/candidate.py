"""
=========================================================
EMIDAF Framework v1.0
EMIX - Integration Candidate
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class IntegrationCandidate:
    """
    Rapprochement potentiel proposé à l'examen
    du chercheur.

    Un candidat n'est pas une relation scientifique
    validée. Il doit être examiné avant création
    éventuelle d'un IntegrationLink.
    """

    candidate_id: str
    source_id_1: str
    source_id_2: str
    element_1: str
    element_2: str
    rationale: str = ""
    status: str = "pending"

    def __post_init__(self) -> None:

        if not self.candidate_id.strip():
            raise ValueError(
                "candidate_id ne peut pas être vide."
            )

        if self.source_id_1 == self.source_id_2:
            raise ValueError(
                "Un candidat doit relier "
                "deux sources distinctes."
            )

        if not self.element_1.strip():
            raise ValueError(
                "element_1 ne peut pas être vide."
            )

        if not self.element_2.strip():
            raise ValueError(
                "element_2 ne peut pas être vide."
            )

        if self.status not in {
            "pending",
            "accepted",
            "rejected",
        }:
            raise ValueError(
                f"Statut invalide : {self.status}"
            )

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
