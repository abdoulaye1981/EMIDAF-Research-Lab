"""
=========================================================
EMIDAF Framework v1.0
EMIX - ETAE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class ETAESourceAdapter(BaseSourceAdapter):

    engine_name = "etae"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        available_sections = [
            key
            for key, value in payload.items()
            if value is not None
        ]

        return MixedMethodSource(
            source_id=source_id,
            engine="etae",
            family="textual",
            label=(
                label
                or "ETAE — Analyse textuelle"
            ),
            result_type="text_analysis",
            result_ref="etae",
            description=(
                "Résultat textuel computationnel "
                "produit par ETAE. "
                f"Sections disponibles : "
                f"{', '.join(available_sections)}"
            ),
        )
