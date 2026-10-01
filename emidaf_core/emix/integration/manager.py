"""
=========================================================
EMIDAF Framework v1.0
EMIX - Integration Manager
=========================================================
"""

from __future__ import annotations

from typing import Any

from .integrator import IntegrationLink
from ..sources import SourceRegistry


class IntegrationManager:
    """
    Gère les rapprochements entre sources EMIX.

    Le gestionnaire contrôle l'intégrité des références
    mais ne détermine pas automatiquement le type de
    relation scientifique.
    """

    def __init__(
        self,
        source_registry: SourceRegistry,
    ) -> None:

        self.source_registry = (
            source_registry
        )

        self._links: dict[
            str,
            IntegrationLink,
        ] = {}

    def add(
        self,
        link: IntegrationLink,
    ) -> IntegrationLink:

        if link.link_id in self._links:
            raise ValueError(
                f"Lien déjà enregistré : "
                f"{link.link_id}"
            )

        if not self.source_registry.exists(
            link.source_id_1
        ):
            raise ValueError(
                f"Source inconnue : "
                f"{link.source_id_1}"
            )

        if not self.source_registry.exists(
            link.source_id_2
        ):
            raise ValueError(
                f"Source inconnue : "
                f"{link.source_id_2}"
            )

        self._links[
            link.link_id
        ] = link

        return link

    def get(
        self,
        link_id: str,
    ) -> IntegrationLink:

        try:
            return self._links[
                link_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Lien EMIX inconnu : "
                f"{link_id}"
            ) from exc

    def all(
        self,
    ) -> list[IntegrationLink]:

        return list(
            self._links.values()
        )

    def remove(
        self,
        link_id: str,
    ) -> IntegrationLink:

        if link_id not in self._links:
            raise ValueError(
                f"Lien EMIX inconnu : "
                f"{link_id}"
            )

        return self._links.pop(
            link_id
        )

    def for_source(
        self,
        source_id: str,
    ) -> list[IntegrationLink]:

        return [
            link
            for link
            in self._links.values()
            if source_id in {
                link.source_id_1,
                link.source_id_2,
            }
        ]

    def by_relation(
        self,
        relation_type: str,
    ) -> list[IntegrationLink]:

        return [
            link
            for link
            in self._links.values()
            if (
                link.relation_type
                == relation_type
            )
        ]

    def validated(
        self,
    ) -> list[IntegrationLink]:

        return [
            link
            for link
            in self._links.values()
            if link.validated
        ]

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "links": [
                link.to_dict()
                for link
                in self._links.values()
            ]
        }
