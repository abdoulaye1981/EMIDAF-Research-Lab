"""
=========================================================
EMIDAF Framework v1.0
Profile Controller
---------------------------------------------------------
Contrôleur des profils de datasets.
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.dataset.profiler.profile_service import ProfileService


class ProfileController:
    """
    Contrôleur des profils de datasets.

    Il constitue l'interface entre la couche
    utilisateur et le ProfileService.
    """

    def __init__(self, service: ProfileService):

        self._service = service

    # =====================================================
    # PROFILE
    # =====================================================

    def profile(
        self,
        dataframe,
        save: bool = False,
    ):
        return self._service.profile(
             dataframe,
             save,
        )
    # =====================================================
    # CREATE
    # =====================================================

    def save(self, profile):

        return self._service.save(profile)

    # =====================================================
    # READ
    # =====================================================

    def find(self, profile_id: int):

        return self._service.find(profile_id)

    def find_all(self):

        return self._service.find_all()

    def exists(self, profile_id: int) -> bool:

        return self._service.exists(profile_id)

    def count(self) -> int:

        return self._service.count()

    def last(self):

        return self._service.last()

    def search(self, query: str):

        return self._service.search(query)

    def datasets(self):

        return self._service.datasets()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile_id: int,
        profile,
    ):
        return self._service.update(
            profile_id,
            profile,
        )
    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, profile_id: int):

        return self._service.delete(profile_id)

    def delete_all(self) -> int:

        return self._service.delete_all()

    # =====================================================
    # PROFILE OPERATIONS
    # =====================================================

    def refresh(
        self,
        dataframe,
        profile_id: int,
    ):
        return self._service.refresh(
           dataframe,
           profile_id,
    )
    def duplicate(self, profile_id: int):

        return self._service.duplicate(profile_id)

    def compare(
        self,
        first,
        second,
    ):
        return self._service.compare(
           first,
           second,
        )
    def validate(self, profile):

        return self._service.validate(profile)

    def statistics(self):

        return self._service.statistics()

    def is_empty(self) -> bool:

        return self._service.is_empty()

    # =====================================================
    # IMPORT / EXPORT
    # =====================================================

    def export_json(
        self,
        profile_id: int,
        path,
    ):

        return self._service.export_json(
            profile_id,
            path,
        )

    def import_json(self, path):

        return self._service.import_json(path)

    # =====================================================
    # BACKUP / RESTORE
    # =====================================================

    def backup(self, path):

        return self._service.backup(path)

    def restore(self, path):

        return self._service.restore(path)
