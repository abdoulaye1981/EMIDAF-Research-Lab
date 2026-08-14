"""
=========================================================
EMIDAF Framework v1.0
Dataset Controller
---------------------------------------------------------
Contrôleur des jeux de données.
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from database.models.dataset_model import DatasetModel
from emidaf_core.services.dataset_service import DatasetService


class DatasetController:
    """
    Contrôleur des jeux de données.

    Il constitue l'interface entre l'interface utilisateur
    (Dash Studio) et le DatasetService.
    """

    def __init__(self, service: DatasetService):

        self._service = service

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, dataset: DatasetModel) -> DatasetModel:

        return self._service.create_dataset(dataset)

    # =====================================================
    # READ
    # =====================================================

    def get(self, dataset_id: int) -> Optional[DatasetModel]:

        return self._service.get_dataset(dataset_id)

    def get_all(self) -> List[DatasetModel]:

        return self._service.get_all_datasets()

    def exists(self, dataset_id: int) -> bool:

        return self._service.dataset_exists(dataset_id)

    def count(self) -> int:

        return self._service.count_datasets()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dataset: DatasetModel) -> DatasetModel:

        return self._service.update_dataset(dataset)

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, dataset_id: int) -> bool:

        return self._service.delete_dataset(dataset_id)

    def delete_all(self) -> None:

        self._service.delete_all()