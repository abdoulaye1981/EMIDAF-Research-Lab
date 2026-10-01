"""
=========================================================
EMIDAF Framework v1.0
EMIX - Integration Candidate Manager
=========================================================
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from .candidate import IntegrationCandidate


class IntegrationCandidateManager:
    """
    Gère les candidats d'intégration proposés
    au chercheur.
    """

    def __init__(self) -> None:

        self._candidates: dict[
            str,
            IntegrationCandidate,
        ] = {}

    def add(
        self,
        candidate: IntegrationCandidate,
    ) -> IntegrationCandidate:

        if candidate.candidate_id in self._candidates:
            raise ValueError(
                f"Candidat déjà enregistré : "
                f"{candidate.candidate_id}"
            )

        self._candidates[
            candidate.candidate_id
        ] = candidate

        return candidate

    def get(
        self,
        candidate_id: str,
    ) -> IntegrationCandidate:

        try:
            return self._candidates[
                candidate_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Candidat inconnu : "
                f"{candidate_id}"
            ) from exc

    def all(
        self,
    ) -> list[IntegrationCandidate]:

        return list(
            self._candidates.values()
        )

    def pending(
        self,
    ) -> list[IntegrationCandidate]:

        return [
            candidate
            for candidate
            in self._candidates.values()
            if candidate.status == "pending"
        ]

    def accept(
        self,
        candidate_id: str,
    ) -> IntegrationCandidate:

        candidate = self.get(
            candidate_id
        )

        updated = replace(
            candidate,
            status="accepted",
        )

        self._candidates[
            candidate_id
        ] = updated

        return updated

    def reject(
        self,
        candidate_id: str,
    ) -> IntegrationCandidate:

        candidate = self.get(
            candidate_id
        )

        updated = replace(
            candidate,
            status="rejected",
        )

        self._candidates[
            candidate_id
        ] = updated

        return updated

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "candidates": [
                candidate.to_dict()
                for candidate
                in self._candidates.values()
            ]
        }
