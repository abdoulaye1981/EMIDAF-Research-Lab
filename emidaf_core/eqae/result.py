"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Analysis Result Objects
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class QualitativeCodeResult:
    """
    Représente un code qualitatif du codebook.
    """

    code_id: str
    name: str
    description: str = ""
    parent_code_id: str | None = None
    color: str | None = None
    is_active: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CodebookResult:
    """
    Représentation sérialisable d'un codebook EQAE.
    """

    name: str
    description: str
    codes: list[QualitativeCodeResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "codes": [
                code.to_dict()
                for code in self.codes
            ],
        }


@dataclass(frozen=True)
class CodingAssignmentResult:
    """
    Association entre un segment qualitatif et un code.
    """

    assignment_id: str
    segment_id: str
    document_id: str
    code_id: str
    mode: str
    memo: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
