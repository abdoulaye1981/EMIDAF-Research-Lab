"""
=========================================================
EMIDAF Framework v1.0
Profile Service
---------------------------------------------------------
Service métier du moteur de profilage.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .dataset_profiler import DatasetProfiler
from .profile_builder import ProfileBuilder
from .profile_repository import ProfileRepository
from .profile_result import ProfileResult


class ProfileService:
    """
    Service métier du Profiler.

    Responsabilités

    - lancer le profilage

    - construire le ProfileResult

    - sauvegarder

    - charger

    - supprimer

    - exporter
    """

    def __init__(
        self,
        profiler: DatasetProfiler,
        builder: ProfileBuilder,
        repository: ProfileRepository
    ) -> None:

        self.profiler = profiler

        self.builder = builder

        self.repository = repository

    # =====================================================
    # PROFILE
    # =====================================================

    def profile(
        self,
        dataframe: pd.DataFrame,
        save: bool = False
    ) -> ProfileResult:
        """
        Lance un profil complet.
        """

        profile = self.profiler.profile(
            dataframe
        )

        if save:

            self.repository.save(
                profile
            )

        return profile

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        profile: ProfileResult
    ) -> int:
        """
        Sauvegarde un profil.
        """

        return self.repository.save(
            profile
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile_id: int,
        profile: ProfileResult
    ) -> None:

        self.repository.update(

            profile_id,

            profile

        )

    # =====================================================
    # FIND
    # =====================================================

    def find(
        self,
        profile_id: int
    ):

        return self.repository.find_by_id(

            profile_id

        )

    # =====================================================
    # FIND ALL
    # =====================================================

    def find_all(self):

        return self.repository.find_all()

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        profile_id: int
    ) -> bool:

        return self.repository.exists(
            profile_id
        )

        # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        profile_id: int
    ) -> bool:
        """
        Supprime un profil.
        """

        if not self.exists(profile_id):

            return False

        return self.repository.delete(profile_id)

    # =====================================================
    # DELETE ALL
    # =====================================================

    def delete_all(self) -> int:
        """
        Supprime tous les profils.
        """

        return self.repository.delete_all()

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(
        self,
        dataframe: pd.DataFrame,
        profile_id: int
    ) -> ProfileResult:
        """
        Recalcule un profil existant.
        """

        profile = self.profiler.profile(
            dataframe
        )

        self.repository.update(
            profile_id,
            profile
        )

        return profile

    # =====================================================
    # DUPLICATE
    # =====================================================

    def duplicate( self,profile_id: int) -> int:

        profile = self.find(profile_id)

        if profile is None:

            raise ValueError(
                f"Profile {profile_id} not found."
            )

        profile["profile_name"] = (

            profile["profile_name"]

            + "_copy"

        )

        def duplicate(self,profile_id: int) -> int:

            return self.repository.duplicate(profile_id)

    # =====================================================
    # EXPORT JSON
    # =====================================================

    def export_json(
        self,
        profile_id: int,
        filename: str
    ) -> None:
        """
        Exporte un profil JSON.
        """

        self.repository.export_json(

            profile_id,

            filename

        )

    # =====================================================
    # IMPORT JSON
    # =====================================================

    def import_json(
        self,
        filename: str
    ) -> int:
        """
        Importe un profil JSON.
        """

        return self.repository.import_json(

            filename

        )

    # =====================================================
    # BACKUP
    # =====================================================

    def backup(
        self,
        directory: str
    ) -> int:
        """
        Sauvegarde complète.
        """

        return self.repository.backup(
            directory
        )

    # =====================================================
    # RESTORE
    # =====================================================

    def restore(
        self,
        directory: str
    ) -> int:
        """
        Restaure une sauvegarde.
        """

        return self.repository.restore(
            directory
        )

    # =====================================================
    # COMPARE
    # =====================================================

    def compare(
        self,
        first: ProfileResult,
        second: ProfileResult
    ) -> dict:
        """
        Compare deux profils.
        """

        return {

            "rows":

                second.summary.rows

                -

                first.summary.rows,

            "columns":

                second.summary.columns

                -

                first.summary.columns,

            "quality_score":

                round(

                    second.summary.quality_score

                    -

                    first.summary.quality_score,

                    2

                ),

            "overall_score":

                round(

                    second.summary.overall_score

                    -

                    first.summary.overall_score,

                    2

                ),

            "missing":

                second.summary.missing_values

                -

                first.summary.missing_values,

            "duplicates":

                second.summary.duplicate_rows

                -

                first.summary.duplicate_rows

        }

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        profile: ProfileResult
    ) -> bool:
        """
        Vérifie qu'un profil est valide.
        """

        return profile.is_valid

    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:
        """
        Nombre total de profils.
        """

        return self.repository.count()

        # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        keyword: str
    ) -> list[dict]:
        """
        Recherche des profils.
        """

        return self.repository.search(keyword)

    # =====================================================
    # DATASETS
    # =====================================================

    def datasets(
        self
    ) -> list[str]:
        """
        Liste des datasets profilés.
        """

        return self.repository.datasets()

    # =====================================================
    # LAST
    # =====================================================

    def last(
        self
    ):
        """
        Retourne le dernier profil.
        """

        return self.repository.last()

    # =====================================================
    # DUPLICATE
    # =====================================================

    def duplicate(
        self,
        profile_id: int
    ) -> int:
        """
        Duplique un profil.
        """

        return self.repository.duplicate(
            profile_id
        )

    # =====================================================
    # EMPTY
    # =====================================================

    def is_empty(
        self
    ) -> bool:
        """
        Vérifie si le repository est vide.
        """

        return self.repository.is_empty()

    # =====================================================
    # INFORMATION
    # =====================================================

    def statistics(
        self
    ) -> dict:
        """
        Statistiques du repository.
        """

        return {

            "profiles": self.count(),

            "datasets": len(

                self.datasets()

            ),

            "empty": self.is_empty()

        }

    # =====================================================
    # MAGIC METHODS
    # =====================================================

    def __len__(self):

        return self.count()

    def __contains__(
        self,
        profile_id: int
    ):

        return self.exists(
            profile_id
        )

    def __str__(self):

        return (

            f"ProfileService("

            f"{self.count()} profiles)"

        )

    def __repr__(self):

        return (

            "ProfileService("

            f"profiles={self.count()})"

        )