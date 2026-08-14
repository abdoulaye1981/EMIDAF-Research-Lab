"""
=========================================================
EMIDAF Framework v1.0
Workspace DTO
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkspaceDTO:
    """
    Objet de transfert représentant un espace de travail.
    """

    id: int | None = None

    name: str = ""

    path: str = ""

    description: str = ""

    is_active: bool = False

    created_at: datetime | None = None

    updated_at: datetime | None = None