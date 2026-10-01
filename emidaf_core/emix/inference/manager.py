"""
=========================================================
EMIDAF Framework v1.0
EMIX - Meta Inference Manager
=========================================================
"""

from __future__ import annotations

from typing import Any

from .meta_inference import MetaInference
from ..integration import IntegrationManager


class MetaInferenceManager:
    """
    Gère les méta-inférences EMIX.

    Une méta-inférence ne peut référencer
    que des IntegrationLink existants.
    """

    def __init__(
        self,
        integration_manager: IntegrationManager,
    ) -> None:

        self.integration_manager = (
            integration_manager
        )

        self._inferences: dict[
            str,
            MetaInference,
        ] = {}

    def add(
        self,
        inference: MetaInference,
    ) -> MetaInference:

        if (
            inference.inference_id
            in self._inferences
        ):
            raise ValueError(
                f"Méta-inférence déjà enregistrée : "
                f"{inference.inference_id}"
            )

        for link_id in inference.link_ids:

            self.integration_manager.get(
                link_id
            )

        self._inferences[
            inference.inference_id
        ] = inference

        return inference

    def get(
        self,
        inference_id: str,
    ) -> MetaInference:

        try:
            return self._inferences[
                inference_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Méta-inférence inconnue : "
                f"{inference_id}"
            ) from exc

    def all(
        self,
    ) -> list[MetaInference]:

        return list(
            self._inferences.values()
        )

    def validated(
        self,
    ) -> list[MetaInference]:

        return [
            inference
            for inference
            in self._inferences.values()
            if inference.validated
        ]

    def for_link(
        self,
        link_id: str,
    ) -> list[MetaInference]:

        return [
            inference
            for inference
            in self._inferences.values()
            if link_id in inference.link_ids
        ]

    def remove(
        self,
        inference_id: str,
    ) -> MetaInference:

        if (
            inference_id
            not in self._inferences
        ):
            raise ValueError(
                f"Méta-inférence inconnue : "
                f"{inference_id}"
            )

        return self._inferences.pop(
            inference_id
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "meta_inferences": [
                inference.to_dict()
                for inference
                in self._inferences.values()
            ]
        }
