"""
=========================================================
EMIDAF Framework v1.0
Dataset Metadata
---------------------------------------------------------
Métadonnées permanentes d'un dataset.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class DatasetMetadata:
    """
    Métadonnées persistantes d'un dataset.
    """

    dataset_id: Optional[int] = None

    project_id: Optional[int] = None

    workspace_id: Optional[int] = None

    name: str = ""

    original_filename: str = ""

    stored_filename: str = ""

    extension: str = ""

    encoding: str = "utf-8"

    separator: str = ","

    decimal: str = "."

    path: Path | None = None

    sha256: str = ""

    rows: int = 0

    columns: int = 0

    memory_usage: int = 0

    file_size: int = 0

    created_at: datetime = datetime.now()

    imported_at: datetime = datetime.now()

    updated_at: datetime = datetime.now()

    description: str = ""

    tags: str = ""

    status: str = "READY"