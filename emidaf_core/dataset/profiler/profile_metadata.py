"""
=========================================================

EMIDAF Framework v1.0

Profile Metadata

---------------------------------------------------------

Métadonnées du profil de dataset.

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class ProfileMetadata:
    """
    Métadonnées associées à un profil de dataset.

    Ces informations sont persistées dans la base
    afin d'assurer la traçabilité des analyses.
    """

    # ======================================================
    # Identifiants
    # ======================================================

    profile_id: Optional[int] = None
    dataset_id: Optional[int] = None
    project_id: Optional[int] = None
    workspace_id: Optional[int] = None
    uuid: str = ""

    # ======================================================
    # Informations générales
    # ======================================================

    profile_name: str = ""
    dataset_name: str = ""
    description: str = ""
    author: str = ""
    framework: str = "EMIDAF"
    framework_version: str = "1.0.0"
    profiler_version: str = "1.0.0"
    python_version: str = ""
    pandas_version: str = ""
    numpy_version: str = ""

    # ======================================================
    # Dates
    # ======================================================

    created_at: datetime = field(
        default_factory=datetime.now
    )
    updated_at: datetime = field(
        default_factory=datetime.now
    )
    execution_started_at: Optional[datetime] = None
    execution_finished_at: Optional[datetime] = None

    # ======================================================
    # Performances
    # ======================================================

    execution_time: float = 0.0
    analyzed_rows: int = 0
    analyzed_columns: int = 0
    analyzed_cells: int = 0
    memory_usage: int = 0

    # ======================================================
    # Configuration
    # ======================================================

    sample_used: bool = False
    sample_size: int = 0
    random_state: int = 42
    correlation_threshold: float = 0.80
    outlier_threshold: float = 1.50

    # ======================================================
    # Statut
    # ======================================================

    status: str = "READY"
    success: bool = True
    warning_count: int = 0
    error_count: int = 0

    # ======================================================
    # Export
    # ======================================================

    exported: bool = False
    exported_at: Optional[datetime] = None
    export_format: str = ""
    report_path: str = ""

    # ======================================================
    # Méthodes utilitaires
    # ======================================================

    @property
    def duration(self) -> float:
        """
        Alias de execution_time.
        """
        return self.execution_time

    @property
    def shape(self) -> tuple[int, int]:
        """
        Dimensions analysées.
        """
        return (
            self.analyzed_rows,
            self.analyzed_columns,
        )

    @property
    def total_cells(self) -> int:
        """
        Nombre total de cellules.
        """
        return self.analyzed_rows * self.analyzed_columns

    def start(self) -> None:
        """
        Début du profilage.
        """
        self.execution_started_at = datetime.now()

    def finish(self) -> None:
        """
        Fin du profilage.
        """
        self.execution_finished_at = datetime.now()

        if self.execution_started_at is not None:
            delta = (
                self.execution_finished_at
                - self.execution_started_at
            )

            self.execution_time = round(
                delta.total_seconds(),
                4,
            )

    def to_dict(self) -> dict:
        """
        Conversion vers dictionnaire.

        Les objets datetime sont convertis en chaînes
        ISO 8601 afin de permettre la sérialisation JSON.
        """
        result = {}

        for key in self.__dataclass_fields__:
            value = getattr(self, key)

            if isinstance(value, datetime):
                value = value.isoformat()

            result[key] = value

        return result

    @classmethod
    def from_dict(cls, values: dict):
        return cls(**values)
