"""
=========================================================
EMIDAF Framework v1.0
Base Mapper
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Generic
from typing import TypeVar


ModelType = TypeVar("ModelType")
DtoType = TypeVar("DtoType")


class BaseMapper(
    ABC,
    Generic[ModelType, DtoType]
):
    """
    Classe de base de tous les mappers.

    Définit le contrat de conversion
    entre un modèle ORM et un DTO.
    """

    @abstractmethod
    def to_dto(
        self,
        model: ModelType
    ) -> DtoType:
        """
        Convertit un modèle ORM en DTO.
        """
        raise NotImplementedError

    @abstractmethod
    def to_model(
        self,
        dto: DtoType
    ) -> ModelType:
        """
        Convertit un DTO en modèle ORM.
        """
        raise NotImplementedError