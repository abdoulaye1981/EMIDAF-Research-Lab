"""
=========================================================
EMIDAF Framework v1.0
Dataset Builder
---------------------------------------------------------
Construction des objets DatasetDTO.
=========================================================
"""

from __future__ import annotations

from datetime import datetime

from emidaf_core.dto.dataset_dto import DatasetDTO


class DatasetBuilder:
    """
    Builder permettant de construire un DatasetDTO.

    Le Builder ne réalise aucune opération de lecture,
    de persistance ou de validation métier.
    """

    def build(
        self,
        project_id: int,
        name: str,
        original_filename: str,
        stored_filename: str,
        extension: str,
        separator: str = ",",
        encoding: str = "utf-8",
        rows: int = 0,
        columns: int = 0,
        size: int = 0,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> DatasetDTO:
        """
        Construit et retourne un DatasetDTO.
        """

        return DatasetDTO(
            project_id=project_id,
            name=name,
            original_filename=original_filename,
            stored_filename=stored_filename,
            extension=extension,
            separator=separator,
            encoding=encoding,
            rows=rows,
            columns=columns,
            size=size,
            created_at=created_at,
            updated_at=updated_at,
        )
