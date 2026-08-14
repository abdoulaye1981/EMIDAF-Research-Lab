"""
=========================================================
EMIDAF Framework v1.0
Dataset Profile
---------------------------------------------------------
Profil complet d'un dataset.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DatasetProfile:
    """
    Profil statistique général du dataset.
    """

    rows: int = 0

    columns: int = 0

    memory_usage: int = 0

    missing_values: int = 0

    duplicate_rows: int = 0

    numeric_columns: list[str] = field(default_factory=list)

    categorical_columns: list[str] = field(default_factory=list)

    datetime_columns: list[str] = field(default_factory=list)

    boolean_columns: list[str] = field(default_factory=list)

    text_columns: list[str] = field(default_factory=list)

    constant_columns: list[str] = field(default_factory=list)

    empty_columns: list[str] = field(default_factory=list)

    unique_values: dict[str, int] = field(default_factory=dict)