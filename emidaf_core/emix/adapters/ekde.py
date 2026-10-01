"""
=========================================================
EMIDAF Framework v1.0
EMIX - EKDE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class EKDESourceAdapter(BaseSourceAdapter):

    engine_name = "ekde"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        return MixedMethodSource(
            source_id=source_id,
            engine="ekde",
            family="quantitative",
            label=(
                label
                or "EKDE — Découverte de connaissances"
            ),
            result_type="knowledge_discovery",
            result_ref="ekde",
            description=(
                "Résultat de découverte de structures "
                "ou de groupes produit par EKDE."
            ),
        )
