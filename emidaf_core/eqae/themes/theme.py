"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Themes
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class QualitativeTheme:
    """
    Représente un thème ou sous-thème qualitatif.

    Un thème EQAE est construit et validé
    par le chercheur.
    """

    theme_id: str
    name: str
    description: str = ""
    parent_theme_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str = "",
        parent_theme_id: str | None = None,
        theme_id: str | None = None,
    ) -> "QualitativeTheme":

        name = str(name).strip()

        if not name:
            raise ValueError(
                "Le nom du thème ne peut pas être vide."
            )

        identifier = (
            str(theme_id).strip()
            if theme_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "theme_id ne peut pas être vide."
            )

        return cls(
            theme_id=identifier,
            name=name,
            description=str(
                description
            ).strip(),
            parent_theme_id=parent_theme_id,
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(self)
