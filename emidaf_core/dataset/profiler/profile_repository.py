"""
=========================================================
EMIDAF Framework v1.0
Profile Repository
---------------------------------------------------------
Gestion de la persistance des profils.
=========================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from emidaf_core.database.database_manager import DatabaseManager

from .profile_result import ProfileResult


class ProfileRepository:
    """
    Repository des profils.

    Cette classe centralise toutes les opérations
    CRUD sur les profils.
    """

    TABLE_NAME = "profiles"

    def __init__(
        self,
        database: DatabaseManager
    ) -> None:

        self.database = database

    # =====================================================
    # CREATE
    # =====================================================

    def save(
        self,
        profile: ProfileResult
    ) -> int:
        """
        Sauvegarde un profil.

        Retourne l'identifiant créé.
        """

        data = profile.to_dict()

        query = """
        INSERT INTO profiles
        (
            profile_name,
            dataset_name,
            created_at,
            execution_time,
            quality_score,
            overall_score,
            content
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """

        values = (

            profile.metadata.profile_name,

            profile.metadata.dataset_name,

            str(profile.metadata.created_at),

            profile.metadata.execution_time,

            profile.summary.quality_score,

            profile.summary.overall_score,

            json.dumps(
                data,
                default=str
            )

        )

        cursor = self.database.execute(
            query,
            values
        )

        return cursor.lastrowid

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile_id: int,
        profile: ProfileResult
    ) -> None:
        """
        Met à jour un profil.
        """

        query = """
        UPDATE profiles
        SET

            profile_name=?,

            dataset_name=?,

            execution_time=?,

            quality_score=?,

            overall_score=?,

            content=?

        WHERE id=?
        """

        values = (

            profile.metadata.profile_name,

            profile.metadata.dataset_name,

            profile.metadata.execution_time,

            profile.summary.quality_score,

            profile.summary.overall_score,

            json.dumps(
                profile.to_dict(),
                default=str
            ),

            profile_id

        )

        self.database.execute(
            query,
            values
        )

        # =====================================================
    # READ
    # =====================================================

    def find_by_id(
        self,
        profile_id: int
    ) -> Optional[dict]:
        """
        Recherche un profil par identifiant.

        Retourne un dictionnaire ou None.
        """

        query = """
        SELECT *
        FROM profiles
        WHERE id = ?
        """

        return self.database.fetch_one(
            query,
            (profile_id,)
        )

    # =====================================================
    # FIND BY NAME
    # =====================================================

    def find_by_name(
        self,
        profile_name: str
    ) -> list[dict]:
        """
        Recherche les profils ayant ce nom.
        """

        query = """
        SELECT *
        FROM profiles
        WHERE profile_name = ?
        ORDER BY created_at DESC
        """

        return self.database.fetch_all(
            query,
            (profile_name,)
        )

    # =====================================================
    # FIND BY DATASET
    # =====================================================

    def find_by_dataset(
        self,
        dataset_name: str
    ) -> list[dict]:
        """
        Recherche tous les profils
        d'un dataset.
        """

        query = """
        SELECT *
        FROM profiles
        WHERE dataset_name = ?
        ORDER BY created_at DESC
        """

        return self.database.fetch_all(
            query,
            (dataset_name,)
        )

    # =====================================================
    # FIND ALL
    # =====================================================

    def find_all(self) -> list[dict]:
        """
        Retourne tous les profils.
        """

        query = """
        SELECT *
        FROM profiles
        ORDER BY created_at DESC
        """

        return self.database.fetch_all(query)

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        profile_id: int
    ) -> bool:
        """
        Vérifie l'existence d'un profil.
        """

        query = """
        SELECT COUNT(*)
        FROM profiles
        WHERE id = ?
        """

        result = self.database.fetch_scalar(
            query,
            (profile_id,)
        )

        return result > 0

    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:
        """
        Nombre total de profils.
        """

        query = """
        SELECT COUNT(*)
        FROM profiles
        """

        return self.database.fetch_scalar(query)

    # =====================================================
    # LAST PROFILE
    # =====================================================

    def last(self) -> Optional[dict]:
        """
        Retourne le dernier profil créé.
        """

        query = """
        SELECT *
        FROM profiles
        ORDER BY created_at DESC
        LIMIT 1
        """

        return self.database.fetch_one(query)

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        keyword: str
    ) -> list[dict]:
        """
        Recherche textuelle.
        """

        query = """
        SELECT *
        FROM profiles

        WHERE

            profile_name LIKE ?

            OR

            dataset_name LIKE ?

        ORDER BY created_at DESC
        """

        value = f"%{keyword}%"

        return self.database.fetch_all(

            query,

            (

                value,

                value

            )

        )

    # =====================================================
    # LIST DATASETS
    # =====================================================

    def datasets(self) -> list[str]:
        """
        Liste des datasets profilés.
        """

        query = """
        SELECT DISTINCT dataset_name
        FROM profiles
        ORDER BY dataset_name
        """

        rows = self.database.fetch_all(query)

        return [

            row["dataset_name"]

            for row in rows

        ]

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

        query = """
        DELETE FROM profiles
        WHERE id = ?
        """

        cursor = self.database.execute(
            query,
            (profile_id,)
        )

        return cursor.rowcount > 0

    # =====================================================
    # DELETE BY NAME
    # =====================================================

    def delete_by_name(
        self,
        profile_name: str
    ) -> int:
        """
        Supprime tous les profils portant ce nom.
        """

        query = """
        DELETE FROM profiles
        WHERE profile_name = ?
        """

        cursor = self.database.execute(
            query,
            (profile_name,)
        )

        return cursor.rowcount

    # =====================================================
    # DELETE ALL
    # =====================================================

    def delete_all(self) -> int:
        """
        Supprime tous les profils.
        """

        query = """
        DELETE FROM profiles
        """

        cursor = self.database.execute(query)

        return cursor.rowcount

    # =====================================================
    # EXPORT JSON
    # =====================================================

    def export_json(
        self,
        profile_id: int,
        file_path: str
    ) -> None:
        """
        Exporte un profil au format JSON.
        """

        profile = self.find_by_id(profile_id)

        if profile is None:

            raise ValueError(
                f"Profile {profile_id} not found."
            )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(

                profile,

                file,

                indent=4,

                ensure_ascii=False,

                default=str

            )

    # =====================================================
    # IMPORT JSON
    # =====================================================

    def import_json(
        self,
        file_path: str
    ) -> int:
        """
        Importe un profil JSON.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            profile = json.load(file)

        query = """
        INSERT INTO profiles
        (
            profile_name,
            dataset_name,
            created_at,
            execution_time,
            quality_score,
            overall_score,
            content
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?
        )
        """

        values = (

            profile["profile_name"],

            profile["dataset_name"],

            profile["created_at"],

            profile["execution_time"],

            profile["quality_score"],

            profile["overall_score"],

            json.dumps(
                profile,
                default=str
            )

        )

        cursor = self.database.execute(
            query,
            values
        )

        return cursor.lastrowid

    # =====================================================
    # BACKUP
    # =====================================================

    def backup(
        self,
        directory: str
    ) -> int:
        """
        Sauvegarde tous les profils dans
        un dossier.
        """

        profiles = self.find_all()

        path = Path(directory)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        count = 0

        for profile in profiles:

            filename = path / f"profile_{profile['id']}.json"

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(

                    profile,

                    file,

                    indent=4,

                    ensure_ascii=False,

                    default=str

                )

            count += 1

        return count

    # =====================================================
    # RESTORE
    # =====================================================

    def restore(
        self,
        directory: str
    ) -> int:
        """
        Restaure un ensemble de profils.
        """

        directory = Path(directory)

        count = 0

        for file in directory.glob("*.json"):

            self.import_json(
                str(file)
            )

            count += 1

        return count

    # =====================================================
    # UTILITIES
    # =====================================================

    def is_empty(self) -> bool:

        return self.count() == 0

    def __len__(self):

        return self.count()

    def __contains__(
        self,
        profile_id: int
    ):

        return self.exists(profile_id)

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __str__(self):

        return (

            f"ProfileRepository("

            f"{self.count()} profiles)"

        )

    def __repr__(self):

        return (

            f"ProfileRepository("

            f"table='{self.TABLE_NAME}')"

        )

    def duplicate(
        self,
        profile_id: int
    ) -> int:
        """
        Duplique un profil.
        """

        profile = self.find_by_id(profile_id)

        if profile is None:

            raise ValueError(
                f"Profile {profile_id} not found."
            )

        profile["profile_name"] += "_copy"

        query = """
        INSERT INTO profiles
        (
            profile_name,
            dataset_name,
            created_at,
            execution_time,
            quality_score,
            overall_score,
            content
        )
        VALUES
        (
            ?,?,?,?,?,?,?
        )
        """

        values = (
            profile["profile_name"],
            profile["dataset_name"],
            profile["created_at"],
            profile["execution_time"],
            profile["quality_score"],
            profile["overall_score"],
            profile["content"]
        )

        cursor = self.database.execute(
            query,
            values
        )

        return cursor.lastrowid


    
