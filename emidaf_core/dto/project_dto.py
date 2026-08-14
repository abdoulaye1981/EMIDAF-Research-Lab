"""
=========================================================
EMIDAF Framework v1.0
Project DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ProjectDTO:
    """
    Objet de transfert représentant un projet.
    """

    id: int | None = None

    workspace_id: int = 0

    name: str = ""

    description: str = ""

    created_at: datetime | None = None

    updated_at: datetime | None = None