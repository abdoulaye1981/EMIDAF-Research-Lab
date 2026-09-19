"""
=========================================================
EMIDAF Framework
Base Result
=========================================================
"""

from __future__ import annotations

from typing import Any

from .base_object import BaseObject


class BaseResult(BaseObject):
    """
    Classe de base de tous les résultats EMIDAF.
    """

    def __init__(self) -> None:

        super().__init__()

        self._success = True

        self._score = 0.0

        self._execution_time = 0.0

        self._warnings: list[str] = []

        self._errors: list[str] = []

        self._recommendations: list[str] = []

        self._data: dict[str, Any] = {}

    # =====================================================
    # SUCCESS
    # =====================================================

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(
        self,
        value: bool
    ) -> None:

        self._success = bool(value)

    # =====================================================
    # SCORE
    # =====================================================

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(
        self,
        value: float
    ) -> None:

        self._score = float(value)

    # =====================================================
    # EXECUTION TIME
    # =====================================================

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @execution_time.setter
    def execution_time(
        self,
        value: float
    ) -> None:

        self._execution_time = float(value)

    # =====================================================
    # WARNINGS
    # =====================================================

    @property
    def warnings(self) -> list[str]:
        return self._warnings

    def add_warning(
        self,
        message: str
    ) -> None:

        if message not in self._warnings:

            self._warnings.append(message)

    # =====================================================
    # ERRORS
    # =====================================================

    @property
    def errors(self) -> list[str]:
        return self._errors

    def add_error(
        self,
        message: str
    ) -> None:

        self._errors.append(message)

        self._success = False

    @property
    def error_count(self) -> int:

        return len(self._errors)

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    @property
    def recommendations(self) -> list[str]:
        return self._recommendations

    def add_recommendation(
        self,
        message: str
    ) -> None:

        self._recommendations.append(message)

    # =====================================================
    # DATA
    # =====================================================

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def put(
        self,
        key: str,
        value: Any
    ) -> None:

        self._data[key] = value

    def get(
        self,
        key,
        default=None,
    ):
        """
        Récupère une valeur du résultat.

        Recherche d'abord dans les données internes,
        puis dans la représentation sérialisée,
        puis dans les attributs.
        """

        if key in self._data:
            return self._data[key]

        data = self.to_dict()

        if key in data:
            return data[key]

        return getattr(
            self,
            key,
            default
        )

    def clear(self) -> None:

        self._data.clear()

    # =====================================================
    # SUMMARY
    # =====================================================

    @property
    def warning_count(self) -> int:

        return len(self._warnings)

    @property
    def recommendation_count(self) -> int:

        return len(self._recommendations)

    @property
    def has_errors(self) -> bool:

        return self.error_count > 0

    @property
    def has_warnings(self) -> bool:

        return self.warning_count > 0

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self) -> dict[str, Any]:

        data = super().to_dict()

        data.update(

            {

                "success": self.success,

                "score": self.score,

                "execution_time": self.execution_time,

                "warnings": self.warnings,

                "errors": self.errors,

                "recommendations": self.recommendations,

                "data": self.data,

            }

        )

        return data
