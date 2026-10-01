"""
=========================================================
EMIDAF Framework v1.0
EMIX - Mixed Methods Integration
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


VALID_RELATION_TYPES = {
    "convergence",
    "complementarity",
    "divergence",
    "undetermined",
}


@dataclass(frozen=True)
class IntegrationLink:
    """
    Décrit un rapprochement entre deux résultats
    issus de sources analytiques différentes.

    La relation ne constitue pas une conclusion
    causale. Elle documente une intégration proposée
    ou validée dans une démarche de méthodes mixtes.
    """

    link_id: str
    source_id_1: str
    source_id_2: str
    element_1: str
    element_2: str
    relation_type: str
    researcher_note: str = ""
    candidate_id: str | None = None
    validated: bool = False

    def __post_init__(self) -> None:

        if not self.link_id.strip():
            raise ValueError(
                "link_id ne peut pas être vide."
            )

        if not self.source_id_1.strip():
            raise ValueError(
                "source_id_1 ne peut pas être vide."
            )

        if not self.source_id_2.strip():
            raise ValueError(
                "source_id_2 ne peut pas être vide."
            )

        if self.source_id_1 == self.source_id_2:
            raise ValueError(
                "Une intégration doit relier "
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

        if self.relation_type not in VALID_RELATION_TYPES:
            raise ValueError(
                f"Type de relation invalide : "
                f"{self.relation_type}"
            )

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
