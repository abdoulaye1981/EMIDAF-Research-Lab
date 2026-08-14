"""
=========================================================
EMIDAF Framework
Base Object
=========================================================

Classe racine de tous les composants EMIDAF.

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0
"""

from __future__ import annotations

from abc import ABC
from datetime import datetime
from uuid import uuid4
from typing import Any


class BaseObject(ABC):
    """
    Classe de base de tous les objets EMIDAF.

    Fournit :

    - identifiant unique
    - date de création
    - métadonnées
    - tags
    - sérialisation
    - représentation
    """

    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._id = str(uuid4())

        self._created_at = datetime.utcnow()

        self._metadata: dict[str, Any] = {}

        self._tags: set[str] = set()

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def id(self) -> str:
        """
        Identifiant unique.
        """
        return self._id

    @property
    def created_at(self) -> datetime:
        """
        Date de création.
        """
        return self._created_at

    @property
    def metadata(self) -> dict[str, Any]:
        """
        Métadonnées.
        """
        return self._metadata

    @property
    def tags(self) -> set[str]:
        """
        Tags associés.
        """
        return self._tags

    # =====================================================
    # METADATA
    # =====================================================

    def set_metadata(
        self,
        key: str,
        value: Any
    ) -> None:
        """
        Ajoute une métadonnée.
        """

        self._metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Retourne une métadonnée.
        """

        return self._metadata.get(key, default)

    def remove_metadata(
        self,
        key: str
    ) -> None:
        """
        Supprime une métadonnée.
        """

        self._metadata.pop(key, None)

    def clear_metadata(self) -> None:
        """
        Supprime toutes les métadonnées.
        """

        self._metadata.clear()

    # =====================================================
    # TAGS
    # =====================================================

    def add_tag(
        self,
        tag: str
    ) -> None:
        """
        Ajoute un tag.
        """

        self._tags.add(tag)

    def remove_tag(
        self,
        tag: str
    ) -> None:
        """
        Supprime un tag.
        """

        self._tags.discard(tag)

    def has_tag(
        self,
        tag: str
    ) -> bool:
        """
        Vérifie si un tag existe.
        """

        return tag in self._tags

    def clear_tags(self) -> None:
        """
        Supprime tous les tags.
        """

        self._tags.clear()

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Sérialise l'objet.
        """

        return {

            "id": self.id,

            "created_at": self.created_at.isoformat(),

            "metadata": dict(self.metadata),

            "tags": sorted(self.tags),

            "class": self.__class__.__name__,

            "version": self.VERSION

        }

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:

        return (

            f"{self.__class__.__name__}"

            f"(id='{self.id}')"

        )

    def __str__(self) -> str:

        return self.__repr__()