"""
=========================================================
EMIDAF Framework v1.0
EMIX - EQAE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class EQAESourceAdapter(BaseSourceAdapter):

    engine_name = "eqae"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        summary = payload.get(
            "summary",
            {},
        )

        global_summary = (
            summary.get(
                "global",
                {},
            )
            if isinstance(
                summary,
                dict,
            )
            else {}
        )

        n_themes = global_summary.get(
            "n_themes"
        )

        description = (
            "Résultat qualitatif validé dans EQAE."
        )

        if n_themes is not None:
            description += (
                f" Nombre de thèmes : "
                f"{n_themes}."
            )

        return MixedMethodSource(
            source_id=source_id,
            engine="eqae",
            family="qualitative",
            label=(
                label
                or "EQAE — Analyse qualitative"
            ),
            result_type="qualitative_analysis",
            result_ref="eqae",
            description=description,
        )
