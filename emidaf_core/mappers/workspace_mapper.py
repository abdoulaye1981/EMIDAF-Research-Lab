"""
=========================================================
EMIDAF Framework v1.0
Workspace Mapper
=========================================================
"""

from __future__ import annotations

from database.models.workspace_model import WorkspaceModel
from emidaf_core.dto.workspace_dto import WorkspaceDTO


class WorkspaceMapper:

    @staticmethod
    def to_dto(model: WorkspaceModel) -> WorkspaceDTO:

        return WorkspaceDTO(
            id=model.id,
            name=model.name,
            path=model.path,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(dto: WorkspaceDTO) -> WorkspaceModel:

        return WorkspaceModel(
            id=dto.id,
            name=dto.name,
            path=dto.path,
            description=dto.description,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )