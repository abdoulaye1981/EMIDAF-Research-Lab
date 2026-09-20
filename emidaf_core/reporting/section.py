"""
=========================================================
EMIDAF Framework
Reporting - Report Section
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReportSection:
    """
    Section structurée d'un rapport EMIDAF.

    Une section distingue :
    - les résultats calculés ;
    - leur interprétation ;
    - les limites méthodologiques.
    """

    title: str
    data: Any = None
    interpretation: str = ""
    limitations: list[str] = field(default_factory=list)
    category: str = "analysis"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "category": self.category,
            "data": self.data,
            "interpretation": self.interpretation,
            "limitations": list(self.limitations),
        }
