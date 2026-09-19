"""
=========================================================
EMIDAF Framework v1.0
Dataset Profile DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from emidaf_core.entities.dataset_profile import (
    DatasetProfile
)

@dataclass(slots=True)
class DatasetProfileDTO:
    """
    DTO du profil du dataset.
    """

    profile: DatasetProfile
