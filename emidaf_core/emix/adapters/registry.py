"""
=========================================================
EMIDAF Framework v1.0
EMIX - Source Adapter Registry
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base import BaseSourceAdapter


class SourceAdapterRegistry:
    """
    Registre des adaptateurs de moteurs EMIDAF.
    """

    def __init__(self) -> None:
        self._adapters: dict[
            str,
            BaseSourceAdapter,
        ] = {}

    def register(
        self,
        adapter: BaseSourceAdapter,
    ) -> None:

        engine = adapter.engine_name

        if not engine:
            raise ValueError(
                "L'adaptateur doit définir "
                "engine_name."
            )

        self._adapters[
            engine
        ] = adapter

    def get(
        self,
        engine: str,
    ) -> BaseSourceAdapter:

        try:
            return self._adapters[
                engine
            ]
        except KeyError as exc:
            raise ValueError(
                f"Aucun adaptateur EMIX "
                f"pour le moteur : {engine}"
            ) from exc

    def adapt(
        self,
        engine: str,
        payload: dict[str, Any],
        *,
        source_id: str,
        label: str | None = None,
    ):

        adapter = self.get(
            engine
        )

        return adapter.adapt(
            payload,
            source_id=source_id,
            label=label,
        )

    def engines(
        self,
    ) -> list[str]:

        return list(
            self._adapters.keys()
        )
