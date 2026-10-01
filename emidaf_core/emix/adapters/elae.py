"""
=========================================================
EMIDAF Framework v1.0
EMIX - ELAE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class ELAESourceAdapter(BaseSourceAdapter):

    engine_name = "elae"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        return MixedMethodSource(
            source_id=source_id,
            engine="elae",
            family="quantitative",
            label=(
                label
                or "ELAE — Analyse exploratoire"
            ),
            result_type="exploratory_analysis",
            result_ref="elae",
            description=(
                "Résultat exploratoire quantitatif "
                "produit par ELAE."
            ),
        )
