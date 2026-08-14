"""
=========================================================
EMIDAF Framework v1.0
Project Mapper
=========================================================
"""

from __future__ import annotations

from database.models.project_model import ProjectModel
from emidaf_core.dto.project_dto import ProjectDTO


class ProjectMapper:

    @staticmethod
    def to_dto(model: ProjectModel) -> ProjectDTO:

        return ProjectDTO(
            id=model.id,
            workspace_id=model.workspace_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(dto: ProjectDTO) -> ProjectModel:

        return ProjectModel(
            id=dto.id,
            workspace_id=dto.workspace_id,
            name=dto.name,
            description=dto.description,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )