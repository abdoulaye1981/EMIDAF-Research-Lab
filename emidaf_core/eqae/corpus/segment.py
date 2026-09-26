"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Segments
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class QualitativeSegment:
    """
    Unité textuelle pouvant être codée dans EQAE.

    Un segment correspond à un verbatim, une phrase,
    un paragraphe ou toute autre unité définie par
    le chercheur.
    """

    segment_id: str
    document_id: str
    text: str
    start: int | None = None
    end: int | None = None
    metadata: dict[str, Any] | None = None

    @classmethod
    def create(
        cls,
        *,
        document_id: str,
        text: str,
        start: int | None = None,
        end: int | None = None,
        metadata: dict[str, Any] | None = None,
        segment_id: str | None = None,
    ) -> "QualitativeSegment":

        document_id = str(
            document_id
        ).strip()

        text = str(
            text
        ).strip()

        if not document_id:
            raise ValueError(
                "document_id ne peut pas être vide."
            )

        if not text:
            raise ValueError(
                "Le texte du segment ne peut pas être vide."
            )

        if start is not None and start < 0:
            raise ValueError(
                "start doit être positif ou nul."
            )

        if end is not None and end < 0:
            raise ValueError(
                "end doit être positif ou nul."
            )

        if (
            start is not None
            and end is not None
            and end < start
        ):
            raise ValueError(
                "end doit être supérieur ou égal à start."
            )

        identifier = (
            str(segment_id).strip()
            if segment_id is not None
            else uuid4().hex
        )

        if not identifier:
            raise ValueError(
                "segment_id ne peut pas être vide."
            )

        return cls(
            segment_id=identifier,
            document_id=document_id,
            text=text,
            start=start,
            end=end,
            metadata=(
                dict(metadata)
                if metadata is not None
                else {}
            ),
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(self)
