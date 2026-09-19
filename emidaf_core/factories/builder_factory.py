from __future__ import annotations

from typing import Any


class BuilderFactory:

    @staticmethod
    def create(name: str, **kwargs: Any):
        name = name.lower().strip()

        if name == "project":
            from emidaf_core.builders.project_builder import ProjectBuilder
            return ProjectBuilder(**kwargs)

        if name == "workspace":
            from emidaf_core.modules.workspace.workspace_builder import WorkspaceBuilder
            return WorkspaceBuilder(**kwargs)

        if name == "profile":
            from emidaf_core.dataset.profiler.profile_builder import ProfileBuilder
            return ProfileBuilder(**kwargs)

        if name == "missing":
            from emidaf_core.missing.builder.missing_builder import MissingBuilder
            return MissingBuilder(**kwargs)

        if name == "dataset":
            from emidaf_core.builders.dataset_builder import DatasetBuilder
            return DatasetBuilder(**kwargs)

        raise ValueError(
            f"Unknown builder '{name}'."
        )

    @staticmethod
    def exists(name: str) -> bool:
        return name.lower().strip() in {
            "project",
            "workspace",
            "profile",
            "missing",
            "dataset",
        }

    @staticmethod
    def list() -> list[str]:
        return [
            "dataset",
            "missing",
            "profile",
            "project",
            "workspace",
        ]
