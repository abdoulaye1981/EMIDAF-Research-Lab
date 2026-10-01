"""
=========================================================
EMIDAF Framework v1.0
EMIX - EDSE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class EDSESourceAdapter(BaseSourceAdapter):

    engine_name = "edse"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        return MixedMethodSource(
            source_id=source_id,
            engine="edse",
            family="decision",
            label=(
                label
                or "EDSE — Aide à la décision"
            ),
            result_type="decision_support",
            result_ref="edse",
            description=(
                "Résultat d'aide à la décision "
                "produit par EDSE."
            ),
        )
