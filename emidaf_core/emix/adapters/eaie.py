"""
=========================================================
EMIDAF Framework v1.0
EMIX - EAIE Source Adapter
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter
from ..sources import MixedMethodSource


class EAIESourceAdapter(BaseSourceAdapter):

    engine_name = "eaie"

    def adapt(
        self,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ) -> MixedMethodSource:

        model_name = (
            payload.get("model_name")
            or payload.get("model")
            or payload.get("estimator")
            or "Modèle prédictif"
        )

        result_type = (
            payload.get("task_type")
            or payload.get("problem_type")
            or "predictive_model"
        )

        return MixedMethodSource(
            source_id=source_id,
            engine="eaie",
            family="quantitative",
            label=(
                label
                or f"EAIE — {model_name}"
            ),
            result_type=str(
                result_type
            ),
            result_ref="eaie",
            description=(
                "Résultat quantitatif ou prédictif "
                "produit par EAIE et mobilisable "
                "dans une intégration de méthodes mixtes."
            ),
        )
