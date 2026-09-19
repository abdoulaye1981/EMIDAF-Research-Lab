"""
=========================================================
EMIDAF Framework v1.0
Dataset DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from emidaf_core.dataset.dataset_detection_result import (
    DatasetDetectionResult
)

from emidaf_core.dataset.profiler.dataset_metadata import (
    DatasetMetadata
)
from emidaf_core.entities.dataset_profile import (
    DatasetProfile
)

@dataclass(slots=True)
class DatasetDTO:
    """
    Objet échangé entre les couches du Framework.
    """

    metadata: DatasetMetadata

    detection: DatasetDetectionResult

    profile: DatasetProfile
