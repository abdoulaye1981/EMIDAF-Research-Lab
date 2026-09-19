"""
EMIDAF Research Lab
Dataset Manager
Version : 1.0.0
"""

from __future__ import annotations

from typing import Any

from database.models.dataset_model import DatasetModel

from emidaf_core.core.base_manager import BaseManager
from emidaf_core.services.dataset_service import DatasetService


class DatasetManager(BaseManager):
    """
    Gestionnaire des jeux de données.

    Le Manager constitue le point d'entrée
    du module Dataset.
    """

    def __init__(
        self,
        service: DatasetService,
    ) -> None:

        super().__init__(service)

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        dataset: DatasetModel | None = None,
    ) -> Any:
        """
        Point d'entrée du DatasetManager.

        Si un dataset est fourni, il est créé.
        Sinon, la liste des datasets est retournée.
        """

        if dataset is not None:
            return self.create(dataset)

        return self.get_all()

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        dataset: DatasetModel,
    ) -> DatasetModel:

        return self.service.create_dataset(dataset)

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        dataset_id: int,
    ) -> DatasetModel | None:

        return self.service.get_dataset(dataset_id)

    def get_all(self) -> list[DatasetModel]:

        return self.service.get_all_datasets()

    def exists(
        self,
        dataset_id: int,
    ) -> bool:

        return self.service.dataset_exists(dataset_id)

    def count(self) -> int:

        return self.service.count_datasets()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        dataset: DatasetModel,
    ) -> DatasetModel:

        return self.service.update_dataset(dataset)

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        dataset_id: int,
    ) -> bool:

        return self.service.delete_dataset(dataset_id)

    def clear(self) -> None:

        self.service.delete_all()
