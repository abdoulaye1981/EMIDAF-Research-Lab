"""
=========================================================
EMIDAF Framework v1.0
EMIX - Mixed Methods Summary
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..sources import MixedMethodSource
from ..integration import (
    IntegrationCandidate,
    IntegrationLink,
)
from ..joint_display import JointDisplayRow
from ..inference import MetaInference


@dataclass(frozen=True)
class MixedMethodsSummary:
    """
    Synthèse sérialisable d'une intégration
    de méthodes mixtes.

    La synthèse distingue explicitement :
    - les suggestions d'intégration ;
    - les liens d'intégration construits ;
    - les méta-inférences du chercheur.
    """

    sources: tuple[MixedMethodSource, ...]
    links: tuple[IntegrationLink, ...]
    joint_display: tuple[JointDisplayRow, ...]
    meta_inferences: tuple[MetaInference, ...]
    candidates: tuple[IntegrationCandidate, ...] = ()

    def to_dict(self) -> dict[str, Any]:

        relation_counts = {
            "convergence": 0,
            "complementarity": 0,
            "divergence": 0,
            "undetermined": 0,
        }

        for link in self.links:
            relation_counts[
                link.relation_type
            ] += 1

        candidate_counts = {
            "pending": 0,
            "accepted": 0,
            "rejected": 0,
        }

        for candidate in self.candidates:

            if (
                candidate.status
                in candidate_counts
            ):
                candidate_counts[
                    candidate.status
                ] += 1

        validated_links = [
            link
            for link in self.links
            if link.validated
        ]

        validated_inferences = [
            inference
            for inference
            in self.meta_inferences
            if inference.validated
        ]

        return {
            "global": {
                "n_sources": len(
                    self.sources
                ),
                "n_candidates": len(
                    self.candidates
                ),
                "n_links": len(
                    self.links
                ),
                "n_joint_display_rows": len(
                    self.joint_display
                ),
                "n_meta_inferences": len(
                    self.meta_inferences
                ),
                "n_validated_links": len(
                    validated_links
                ),
                "n_validated_meta_inferences": len(
                    validated_inferences
                ),
            },
            "candidate_statuses": (
                candidate_counts
            ),
            "relations": (
                relation_counts
            ),
            "validation": {
                "suggestions_are_conclusions": False,
                "validated_links": len(
                    validated_links
                ),
                "validated_meta_inferences": len(
                    validated_inferences
                ),
                "principle": (
                    "Les suggestions d'intégration "
                    "ne constituent pas des conclusions. "
                    "Les liens et méta-inférences restent "
                    "soumis à la validation du chercheur."
                ),
            },
            "sources": [
                source.to_dict()
                for source in self.sources
            ],
            "candidates": [
                candidate.to_dict()
                for candidate
                in self.candidates
            ],
            "links": [
                link.to_dict()
                for link in self.links
            ],
            "joint_display": [
                row.to_dict()
                for row in self.joint_display
            ],
            "meta_inferences": [
                inference.to_dict()
                for inference
                in self.meta_inferences
            ],
        }
