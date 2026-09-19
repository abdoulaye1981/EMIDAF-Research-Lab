"""
=========================================================
EMIDAF Framework v1.0
Profile Manager
---------------------------------------------------------
Gestionnaire des profils de datasets
=========================================================
"""

from __future__ import annotations

from typing import Any, Optional

from emidaf_core.core.base_manager import BaseManager
from emidaf_core.dataset.profiler.profile_service import ProfileService


class ProfileManager(BaseManager):
    """
    Gestionnaire des profils de datasets.

    Le Manager constitue le point d'entrée
    du module de profilage.
    """

    def __init__(
        self,
        service: ProfileService,
    ) -> None:

        super().__init__(service)

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        dataframe=None,
    ) -> Any:

        if dataframe is not None:
            return self.profile(dataframe)

        return self.find_all()

    # =====================================================
    # PROFILE
    # =====================================================

    def profile(
        self,
        dataframe,
        save: bool = False,
    ):
        return self.service.profile(
             dataframe,
             save,
        )
    # =====================================================
    # CREATE
    # =====================================================

    def save(
        self,
        profile,
    ):

        return self.service.save(profile)

    # =====================================================
    # READ
    # =====================================================

    def find(
        self,
        profile_id: int,
    ):

        return self.service.find(profile_id)

    def find_all(self):

        return self.service.find_all()

    def exists(
        self,
        profile_id: int,
    ) -> bool:

        return self.service.exists(profile_id)

    def count(self) -> int:

        return self.service.count()

    def last(self):

        return self.service.last()

    def search(
        self,
        query: str,
    ):

        return self.service.search(query)

    def datasets(self):

        return self.service.datasets()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile_id: int,
        profile,
    ):
        return self.service.update(
            profile_id,
            profile,
        )
    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        profile_id: int,
    ):

        return self.service.delete(profile_id)

    def clear(self) -> None:

        self.service.delete_all()

    # =====================================================
    # PROFILE OPERATIONS
    # =====================================================
    def refresh(
        self,
        dataframe,
        profile_id: int,
    ):
        return self.service.refresh(
           dataframe,
           profile_id,
        )

    def duplicate(
        self,
        profile_id: int,
    ):

        return self.service.duplicate(profile_id)

    def compare(
        self,
        first,
        second,
    ):

        return self.service.compare(
            first,
            second,
        )
    def validate(
        self,
        profile,
    ):

        return self.service.validate(profile)

    def statistics(self):

        return self.service.statistics()

    def is_empty(self) -> bool:

        return self.service.is_empty()

    # =====================================================
    # IMPORT / EXPORT
    # =====================================================

    def export_json(
        self,
        profile_id: int,
        path,
    ):

        return self.service.export_json(
            profile_id,
            path,
        )

    def import_json(
        self,
        path,
    ):

        return self.service.import_json(path)

    # =====================================================
    # BACKUP / RESTORE
    # =====================================================

    def backup(
        self,
        path,
    ):

        return self.service.backup(path)

    def restore(
        self,
        path,
    ):

        return self.service.restore(path)

    # =====================================================
    # REFRESH
    # =====================================================

    def __len__(self):

        return self.count()

    def __contains__(
        self,
        profile_id: int,
    ) -> bool:

        return self.exists(profile_id)
