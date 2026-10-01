"""
=========================================================
EMIDAF Framework v1.0
EMIX - Joint Display
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class JointDisplayRow:
    """
    Représente une ligne d'un joint display
    de méthodes mixtes.

    Le joint display juxtapose les résultats
    sans produire automatiquement de méta-inférence.
    """

    row_id: str
    quantitative_result: str
    qualitative_result: str
    relation_type: str
    integrated_comment: str = ""
    source_link_id: str | None = None

    def __post_init__(self) -> None:

        if not self.row_id.strip():
            raise ValueError(
                "row_id ne peut pas être vide."
            )

        if not self.quantitative_result.strip():
            raise ValueError(
                "quantitative_result "
                "ne peut pas être vide."
            )

        if not self.qualitative_result.strip():
            raise ValueError(
                "qualitative_result "
                "ne peut pas être vide."
            )

        if self.relation_type not in {
            "convergence",
            "complementarity",
            "divergence",
            "undetermined",
        }:
            raise ValueError(
                f"Type de relation invalide : "
                f"{self.relation_type}"
            )

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
