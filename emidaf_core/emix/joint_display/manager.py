"""
=========================================================
EMIDAF Framework v1.0
EMIX - Joint Display Manager
=========================================================
"""

from __future__ import annotations

from typing import Any

from .joint_display import JointDisplayRow
from ..integration import IntegrationManager


class JointDisplayManager:
    """
    Gère les lignes de joint display EMIX.

    Une ligne peut être liée à un IntegrationLink
    déjà enregistré.
    """

    def __init__(
        self,
        integration_manager: IntegrationManager,
    ) -> None:

        self.integration_manager = (
            integration_manager
        )

        self._rows: dict[
            str,
            JointDisplayRow,
        ] = {}

    def add(
        self,
        row: JointDisplayRow,
    ) -> JointDisplayRow:

        if row.row_id in self._rows:
            raise ValueError(
                f"Ligne déjà enregistrée : "
                f"{row.row_id}"
            )

        if row.source_link_id is not None:

            self.integration_manager.get(
                row.source_link_id
            )

        self._rows[
            row.row_id
        ] = row

        return row

    def get(
        self,
        row_id: str,
    ) -> JointDisplayRow:

        try:
            return self._rows[
                row_id
            ]
        except KeyError as exc:
            raise ValueError(
                f"Ligne de joint display "
                f"inconnue : {row_id}"
            ) from exc

    def all(
        self,
    ) -> list[JointDisplayRow]:

        return list(
            self._rows.values()
        )

    def remove(
        self,
        row_id: str,
    ) -> JointDisplayRow:

        if row_id not in self._rows:
            raise ValueError(
                f"Ligne de joint display "
                f"inconnue : {row_id}"
            )

        return self._rows.pop(
            row_id
        )

    def for_link(
        self,
        link_id: str,
    ) -> list[JointDisplayRow]:

        return [
            row
            for row
            in self._rows.values()
            if (
                row.source_link_id
                == link_id
            )
        ]

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return {
            "joint_display": [
                row.to_dict()
                for row
                in self._rows.values()
            ]
        }
