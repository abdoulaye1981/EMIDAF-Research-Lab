"""
=========================================================
EMIDAF Framework v1.0
EQAE - Analytical Memo Manager
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class AnalyticalMemo:
    """
    Mémo analytique produit par le chercheur.

    Un mémo peut être global ou rattaché à une
    entité qualitative : document, segment, code,
    thème ou verbatim.
    """

    memo_id: str
    title: str
    content: str
    target_type: str = "analysis"
    target_id: str | None = None
    author: str | None = None
    created_at: str = ""

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(self)


class MemoManager:
    """
    Gestion des mémos analytiques EQAE.
    """

    VALID_TARGET_TYPES = {
        "analysis",
        "document",
        "segment",
        "code",
        "theme",
        "quotation",
    }

    def __init__(self) -> None:

        self._memos: dict[
            str,
            AnalyticalMemo,
        ] = {}

    @property
    def memos(
        self,
    ) -> list[AnalyticalMemo]:

        return list(
            self._memos.values()
        )

    def add_memo(
        self,
        *,
        title: str,
        content: str,
        target_type: str = "analysis",
        target_id: str | None = None,
        author: str | None = None,
        memo_id: str | None = None,
        created_at: str | None = None,
    ) -> AnalyticalMemo:
        """
        Ajoute un mémo analytique.
        """

        title = str(
            title
        ).strip()

        content = str(
            content
        ).strip()

        if not title:
            raise ValueError(
                "Le titre du mémo ne peut pas être vide."
            )

        if not content:
            raise ValueError(
                "Le contenu du mémo ne peut pas être vide."
            )

        target_type = str(
            target_type
        ).strip().lower()

        if (
            target_type
            not in self.VALID_TARGET_TYPES
        ):
            raise ValueError(
                "Type de cible invalide : "
                f"{target_type}"
            )

        if target_type == "analysis":

            if target_id is not None:
                raise ValueError(
                    "Un mémo global d'analyse ne doit "
                    "pas avoir de target_id."
                )

        else:

            if (
                target_id is None
                or not str(
                    target_id
                ).strip()
            ):
                raise ValueError(
                    "target_id est obligatoire pour "
                    f"une cible de type {target_type}."
                )

            target_id = str(
                target_id
            ).strip()

        identifier = (
            str(memo_id).strip()
            if memo_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "memo_id ne peut pas être vide."
            )

        if identifier in self._memos:
            raise ValueError(
                "Identifiant de mémo déjà utilisé : "
                f"{identifier}"
            )

        timestamp = (
            str(created_at).strip()
            if created_at is not None
            else datetime.now(
                timezone.utc
            ).isoformat()
        )

        if not timestamp:
            raise ValueError(
                "created_at ne peut pas être vide."
            )

        normalized_author = (
            str(author).strip()
            if author is not None
            else None
        )

        if normalized_author == "":
            normalized_author = None

        memo = AnalyticalMemo(
            memo_id=identifier,
            title=title,
            content=content,
            target_type=target_type,
            target_id=target_id,
            author=normalized_author,
            created_at=timestamp,
        )

        self._memos[
            identifier
        ] = memo

        return memo

    def get_memo(
        self,
        memo_id: str,
    ) -> AnalyticalMemo | None:
        """
        Retourne un mémo par son identifiant.
        """

        return self._memos.get(
            str(memo_id)
        )

    def memos_for_target(
        self,
        *,
        target_type: str,
        target_id: str | None = None,
    ) -> list[AnalyticalMemo]:
        """
        Retourne les mémos associés à une cible.
        """

        target_type = str(
            target_type
        ).strip().lower()

        if (
            target_type
            not in self.VALID_TARGET_TYPES
        ):
            raise ValueError(
                "Type de cible invalide : "
                f"{target_type}"
            )

        if target_type == "analysis":
            target_id = None
        else:
            if (
                target_id is None
                or not str(
                    target_id
                ).strip()
            ):
                raise ValueError(
                    "target_id est obligatoire pour "
                    f"une cible de type {target_type}."
                )

            target_id = str(
                target_id
            ).strip()

        return [
            memo
            for memo
            in self._memos.values()
            if (
                memo.target_type
                == target_type
                and memo.target_id
                == target_id
            )
        ]

    def remove_memo(
        self,
        memo_id: str,
    ) -> AnalyticalMemo:
        """
        Supprime un mémo analytique.
        """

        memo_id = str(
            memo_id
        )

        if memo_id not in self._memos:
            raise ValueError(
                "Mémo introuvable : "
                f"{memo_id}"
            )

        return self._memos.pop(
            memo_id
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Sérialise l'ensemble des mémos.
        """

        return {
            "memos": [
                memo.to_dict()
                for memo
                in self.memos
            ]
        }
