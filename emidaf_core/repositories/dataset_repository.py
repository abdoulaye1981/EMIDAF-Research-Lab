"""
=========================================================
EMIDAF Framework v1.0
Dataset Repository
---------------------------------------------------------
Gestion de la persistance des jeux de données.
=========================================================
"""

from __future__ import annotations

from typing import List
from typing import Optional

from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy import select

from database.database_manager import DatabaseManager
from database.models.dataset_model import DatasetModel


class DatasetRepository:
    """
    Repository des jeux de données.

    Responsabilités
    ----------------
    - Ajouter un dataset
    - Rechercher un dataset
    - Modifier un dataset
    - Supprimer un dataset
    - Lister les datasets

    Aucune logique métier.
    """

    def __init__(self, database_manager: DatabaseManager) -> None:
        """
        Initialise le repository.

        Parameters
        ----------
        database_manager : DatabaseManager
            Gestionnaire de base de données.
        """

        self._database = database_manager

    # =====================================================
    # CREATE
    # =====================================================

    def add(self, dataset: DatasetModel) -> DatasetModel:
        """
        Ajoute un dataset.

        Parameters
        ----------
        dataset : DatasetModel

        Returns
        -------
        DatasetModel
        """

        with self._database.session_scope() as session:

            session.add(dataset)

            session.flush()

            session.refresh(dataset)

            return dataset

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(self, dataset_id: int) -> Optional[DatasetModel]:
        """
        Recherche un dataset par son identifiant.

        Parameters
        ----------
        dataset_id : int

        Returns
        -------
        DatasetModel | None
        """

        with self._database.session_scope() as session:

            return session.get(DatasetModel, dataset_id)

    def get_all(self) -> List[DatasetModel]:
        """
        Retourne tous les datasets.

        Returns
        -------
        list[DatasetModel]
        """

        with self._database.session_scope() as session:

            statement = select(DatasetModel)

            return list(session.scalars(statement).all())

    def exists(self, dataset_id: int) -> bool:
        """
        Vérifie si un dataset existe.

        Parameters
        ----------
        dataset_id : int

        Returns
        -------
        bool
        """

        with self._database.session_scope() as session:

            statement = select(
                exists().where(DatasetModel.id == dataset_id)
            )

            return bool(session.scalar(statement))

    def count(self) -> int:
        """
        Retourne le nombre de datasets.

        Returns
        -------
        int
        """

        with self._database.session_scope() as session:

            statement = select(func.count(DatasetModel.id))

            return session.scalar(statement) or 0

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dataset: DatasetModel) -> DatasetModel:
        """
        Met à jour un dataset.

        Parameters
        ----------
        dataset : DatasetModel

        Returns
        -------
        DatasetModel
        """

        with self._database.session_scope() as session:

            dataset = session.merge(dataset)

            session.flush()

            session.refresh(dataset)

            return dataset

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, dataset_id: int) -> bool:
        """
        Supprime un dataset.

        Parameters
        ----------
        dataset_id : int

        Returns
        -------
        bool
        """

        with self._database.session_scope() as session:

            dataset = session.get(DatasetModel, dataset_id)

            if dataset is None:
                return False

            session.delete(dataset)

            return True

    def delete_all(self) -> None:
        """
        Supprime tous les datasets.
        """

        with self._database.session_scope() as session:

            session.execute(delete(DatasetModel))