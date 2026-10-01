"""
=========================================================
EMIDAF Framework v1.0
EMIX - Mixed Method Source
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


VALID_SOURCE_FAMILIES = {
    "quantitative",
    "qualitative",
    "textual",
    "decision",
}


@dataclass(frozen=True)
class MixedMethodSource:
    """
    Représente une source analytique mobilisée
    dans une intégration de méthodes mixtes.

    Une source décrit un résultat déjà produit
    par un autre moteur EMIDAF. EMIX ne recalcule
    pas ce résultat.
    """

    source_id: str
    engine: str
    family: str
    label: str
    result_type: str
    result_ref: str | None = None
    description: str = ""

    def __post_init__(self) -> None:

        if not self.source_id.strip():
            raise ValueError(
                "source_id ne peut pas être vide."
            )

        if not self.engine.strip():
            raise ValueError(
                "engine ne peut pas être vide."
            )

        if self.family not in VALID_SOURCE_FAMILIES:
            raise ValueError(
                f"Famille de source invalide : "
                f"{self.family}"
            )

        if not self.label.strip():
            raise ValueError(
                "label ne peut pas être vide."
            )

        if not self.result_type.strip():
            raise ValueError(
                "result_type ne peut pas être vide."
            )

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)
