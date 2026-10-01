"""
=========================================================
EMIDAF Framework v1.0
EMIX - Source Registry
=========================================================
"""

from __future__ import annotations

from typing import Any

from .source import MixedMethodSource


class SourceRegistry:
    """
    Registre des sources analytiques mobilisées
    dans une intégration de méthodes mixtes.
    """

    def __init__(self) -> None:
        self._sources: dict[
            str,
            MixedMethodSource,
        ] = {}

    def add(
        self,
        source: MixedMethodSource,
    ) -> MixedMethodSource:

        if source.source_id in self._sources:
            raise ValueError(
                f"Source déjà enregistrée : "
                f"{source.source_id}"
            )

        self._sources[
            source.source_id
        ] = source

        return source

    def get(
        self,
        source_id: str,
    ) -> MixedMethodSource:

        try:
            return self._sources[
                source_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Source EMIX inconnue : "
                f"{source_id}"
            ) from exc

    def exists(
        self,
        source_id: str,
    ) -> bool:

        return source_id in self._sources

    def all(
        self,
    ) -> list[MixedMethodSource]:

        return list(
            self._sources.values()
        )

    def remove(
        self,
        source_id: str,
    ) -> MixedMethodSource:

        if source_id not in self._sources:
            raise ValueError(
                f"Source EMIX inconnue : "
                f"{source_id}"
            )

        return self._sources.pop(
            source_id
        )

    def by_family(
        self,
        family: str,
    ) -> list[MixedMethodSource]:

        return [
            source
            for source
            in self._sources.values()
            if source.family == family
        ]

    def by_engine(
        self,
        engine: str,
    ) -> list[MixedMethodSource]:

        return [
            source
            for source
            in self._sources.values()
            if source.engine == engine
        ]

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "sources": [
                source.to_dict()
                for source
                in self._sources.values()
            ]
        }
