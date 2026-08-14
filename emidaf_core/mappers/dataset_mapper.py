from __future__ import annotations

from database.models.dataset_model import DatasetModel

from emidaf_core.dto.dataset_dto import DatasetDTO
from emidaf_core.mappers.base_mapper import BaseMapper


class DatasetMapper(
    BaseMapper[
        DatasetModel,
        DatasetDTO
    ]
):

    def to_dto(
        self,
        model: DatasetModel
    ) -> DatasetDTO:

        return DatasetDTO(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            original_filename=model.original_filename,
            stored_filename=model.stored_filename,
            extension=model.extension,
            separator=model.separator,
            encoding=model.encoding,
            rows=model.rows,
            columns=model.columns,
            size=model.size,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def to_model(
        self,
        dto: DatasetDTO
    ) -> DatasetModel:

        return DatasetModel(
            id=dto.id,
            project_id=dto.project_id,
            name=dto.name,
            original_filename=dto.original_filename,
            stored_filename=dto.stored_filename,
            extension=dto.extension,
            separator=dto.separator,
            encoding=dto.encoding,
            rows=dto.rows,
            columns=dto.columns,
            size=dto.size,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )