"""
=========================================================
EMIDAF Framework v1.0
Analyzer Result
---------------------------------------------------------
Objet standard retourné par tous les analyzers.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class AnalyzerResult:
    """
    Résultat retourné par un Analyzer.

    Tous les analyzers d'EMIDAF doivent retourner
    cette classe plutôt qu'un simple dictionnaire.
    """

    # =====================================================
    # Identification
    # =====================================================

    name: str

    analyzer: str = ""

    version: str = "1.0.0"

    # =====================================================
    # Exécution
    # =====================================================

    started_at: datetime = field(
        default_factory=datetime.now
    )

    finished_at: datetime | None = None

    execution_time: float = 0.0

    success: bool = True

    status: str = "SUCCESS"

    # =====================================================
    # Résultat principal
    # =====================================================

    result: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Informations complémentaires
    # =====================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Messages
    # =====================================================

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    recommendations: list[str] = field(
        default_factory=list
    )

    logs: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Score
    # =====================================================

    score: float | None = None

    confidence: float | None = None

    # =====================================================
    # Méthodes
    # =====================================================

    def finish(self) -> None:
        """
        Termine l'analyse.
        """

        self.finished_at = datetime.now()

        self.execution_time = round(

            (
                self.finished_at

                -

                self.started_at

            ).total_seconds(),

            4

        )

    def add_warning(
        self,
        message: str
    ) -> None:

        self.warnings.append(message)

    def add_error(
        self,
        message: str
    ) -> None:

        self.success = False

        self.status = "FAILED"

        self.errors.append(message)

    def add_log(
        self,
        message: str
    ) -> None:

        self.logs.append(message)

    def add_recommendation(
        self,
        recommendation: str
    ) -> None:

        self.recommendations.append(
            recommendation
        )

    def set_result(
        self,
        result: dict[str, Any]
    ) -> None:

        self.result = result

    def update_metadata(
        self,
        **kwargs
    ) -> None:

        self.metadata.update(kwargs)

    @property
    def has_warning(self) -> bool:

        return len(self.warnings) > 0

    @property
    def has_error(self) -> bool:

        return len(self.errors) > 0

    @property
    def recommendation_count(self) -> int:

        return len(self.recommendations)

    def to_dict(self) -> dict:

        return {

            "name": self.name,

            "analyzer": self.analyzer,

            "version": self.version,

            "status": self.status,

            "success": self.success,

            "execution_time": self.execution_time,

            "score": self.score,

            "confidence": self.confidence,

            "metadata": self.metadata,

            "statistics": self.statistics,

            "result": self.result,

            "warnings": self.warnings,

            "errors": self.errors,

            "recommendations": self.recommendations,

            "logs": self.logs

        }