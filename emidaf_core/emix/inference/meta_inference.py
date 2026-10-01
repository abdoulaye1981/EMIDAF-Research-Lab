"""
=========================================================
EMIDAF Framework v1.0
EMIX - Meta Inference
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class MetaInference:
    """
    Représente une méta-inférence issue d'une
    intégration de méthodes mixtes.

    La méta-inférence reste une interprétation
    du chercheur. EMIX ne la valide pas
    automatiquement.
    """

    inference_id: str
    statement: str
    link_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    researcher_note: str = ""
    validated: bool = False

    def __post_init__(self) -> None:

        if not self.inference_id.strip():
            raise ValueError(
                "inference_id ne peut pas être vide."
            )

        if not self.statement.strip():
            raise ValueError(
                "statement ne peut pas être vide."
            )

    def to_dict(self) -> dict[str, Any]:

        data = asdict(self)

        data["link_ids"] = list(
            self.link_ids
        )

        data["limitations"] = list(
            self.limitations
        )

        return data
