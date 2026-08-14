"""
=========================================================
EMIDAF Framework v1.0
Dataset Service
---------------------------------------------------------
Logique métier des jeux de données.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import List
from typing import Optional

from database.models.dataset_model import DatasetModel
from emidaf_core.repositories.dataset_repository import DatasetRepository


class DatasetService:
    """
    Service métier des jeux de données.

    Responsabilités
    ----------------
    - Validation
    - Création
    - Modification
    - Suppression
    - Recherche
    """

    def __init__(self, repository: DatasetRepository):

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create_dataset(self, dataset: DatasetModel) -> DatasetModel:
        """
        Crée un nouveau dataset.
        """

        self._validate(dataset)

        return self._repository.add(dataset)

    # =====================================================
    # READ
    # =====================================================

    def get_dataset(self, dataset_id: int) -> Optional[DatasetModel]:

        return self._repository.get_by_id(dataset_id)

    def get_all_datasets(self) -> List[DatasetModel]:

        return self._repository.get_all()

    def dataset_exists(self, dataset_id: int) -> bool:

        return self._repository.exists(dataset_id)

    def count_datasets(self) -> int:

        return self._repository.count()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_dataset(self, dataset: DatasetModel) -> DatasetModel:
        """
        Met à jour un dataset.
        """

        self._validate(dataset)

        return self._repository.update(dataset)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_dataset(self, dataset_id: int) -> bool:

        return self._repository.delete(dataset_id)

    def delete_all(self) -> None:

        self._repository.delete_all()

    # =====================================================
    # VALIDATION
    # =====================================================

    def _validate(self, dataset: DatasetModel) -> None:
        """
        Validation métier.
        """

        if not dataset.name.strip():
            raise ValueError("Dataset name cannot be empty.")

        if not dataset.original_filename.strip():
            raise ValueError("Original filename cannot be empty.")

        if not dataset.stored_filename.strip():
            raise ValueError("Stored filename cannot be empty.")

        if dataset.rows < 0:
            raise ValueError("Rows must be positive.")

        if dataset.columns < 0:
            raise ValueError("Columns must be positive.")

        if dataset.size < 0:
            raise ValueError("Size must be positive.")

        if not Path(dataset.stored_filename).suffix:
            raise ValueError("Dataset extension is invalid.")