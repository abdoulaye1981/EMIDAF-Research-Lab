"""
=========================================================
EMIDAF Framework v1.0
Dataset DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class DatasetDTO:
    """
    Objet de transfert représentant un dataset.
    """

    id: int | None = None

    project_id: int = 0

    name: str = ""

    original_filename: str = ""

    stored_filename: str = ""

    extension: str = ""

    separator: str = ","

    encoding: str = "utf-8"

    rows: int = 0

    columns: int = 0

    size: int = 0

    created_at: datetime | None = None

    updated_at: datetime | None = None