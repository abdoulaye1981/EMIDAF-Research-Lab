"""
=========================================================
EMIDAF Framework v1.0
Dataset Detection DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from emidaf_core.dataset.dataset_detection_result import (
    DatasetDetectionResult
)


@dataclass(slots=True)
class DatasetDetectionDTO:
    """
    DTO de détection.
    """

    detection: DatasetDetectionResult