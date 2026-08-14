"""
=========================================================
EMIDAF Framework
Analyzer Result
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base_result import BaseResult


class AnalyzerResult(BaseResult):
    """
    Résultat retourné par tous les analyzers.
    """

    def __init__(
        self,
        analyzer: str,
        version: str = "1.0.0"
    ) -> None:

        super().__init__()

        self._analyzer = analyzer

        self._version = version

        self._description = ""

        self._status = "SUCCESS"

        self._statistics: dict[str, Any] = {}

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def analyzer(self) -> str:
        return self._analyzer

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(
        self,
        value: str
    ) -> None:

        self._description = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(
        self,
        value: str
    ) -> None:

        self._status = value

    # =====================================================
    # STATISTICS
    # =====================================================

    @property
    def statistics(self) -> dict[str, Any]:
        return self._statistics

    def set_statistic(
        self,
        key: str,
        value: Any
    ) -> None:

        self._statistics[key] = value

    def statistic(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        return self._statistics.get(key, default)

    # =====================================================
    # FINALIZE
    # =====================================================

    def finalize(self) -> None:

        if self.error_count > 0:

            self.success = False

            self.status = "FAILED"

        elif self.warning_count > 0:

            self.status = "WARNING"

        else:

            self.status = "SUCCESS"

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self) -> dict[str, Any]:

        data = super().to_dict()

        data.update(

            {

                "analyzer": self.analyzer,

                "version": self.version,

                "description": self.description,

                "status": self.status,

                "statistics": self.statistics,

            }

        )

        return data