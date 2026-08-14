"""
=========================================================
EMIDAF Framework v1.0
Dataset Detection Result
---------------------------------------------------------
Résultat de la détection automatique d'un dataset.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DatasetDetectionResult:
    """
    Résultat complet de la détection d'un fichier.
    """

    file: Path

    filename: str

    extension: str

    mime_type: str

    encoding: str

    separator: str

    decimal: str

    has_header: bool

    rows: int

    columns: int

    size: int

    sha256: str

    created_at: str

    modified_at: str