"""
=========================================================
EMIDAF Framework v1.0
Analyzer Registry
---------------------------------------------------------
Registre central des analyzers.
=========================================================
"""

from __future__ import annotations

from typing import Iterator

from emidaf_core.core.base_registry import BaseRegistry

from .base_analyzer import BaseAnalyzer


class AnalyzerRegistry(BaseRegistry[BaseAnalyzer]):
    """
    Registre des analyzers.

    Hérite du BaseRegistry et ajoute uniquement
    la gestion des analyzers activés/désactivés.
    """

    def __init__(self) -> None:

        super().__init__()

        self._enabled: dict[str, bool] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        analyzer: BaseAnalyzer,
        *,
        overwrite: bool = False,
    ) -> None:

        super().register(

            analyzer,

            overwrite=overwrite

        )

        self._enabled[analyzer.name] = True

    # =====================================================
    # UNREGISTER
    # =====================================================

    def unregister(
        self,
        name: str,
    ) -> None:

        super().unregister(name)

        self._enabled.pop(name, None)

    # =====================================================
    # ENABLE
    # =====================================================

    def enable(
        self,
        name: str,
    ) -> None:

        if self.exists(name):

            self._enabled[name] = True

    # =====================================================
    # DISABLE
    # =====================================================

    def disable(
        self,
        name: str,
    ) -> None:

        if self.exists(name):

            self._enabled[name] = False

    # =====================================================
    # STATUS
    # =====================================================

    def is_enabled(
        self,
        name: str,
    ) -> bool:

        return self._enabled.get(name, False)

    # =====================================================
    # ENABLED ANALYZERS
    # =====================================================

    def enabled(self) -> list[BaseAnalyzer]:

        return [

            analyzer

            for analyzer in self.values

            if self._enabled.get(analyzer.name, False)

        ]

    # =====================================================
    # ITERATOR
    # =====================================================

    def __iter__(self) -> Iterator[BaseAnalyzer]:

        return iter(self.enabled())