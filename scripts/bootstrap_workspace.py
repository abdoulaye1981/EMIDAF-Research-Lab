from __future__ import annotations

import os
from pathlib import Path

from database.models.workspace_model import WorkspaceModel
from emidaf_core.bootstrap.bootstrap import Bootstrap


def main() -> int:
    bootstrap = Bootstrap()
    bootstrap.initialize()

    repository = bootstrap.workspace_repository

    workspace_name = os.environ.get(
        "EMIDAF_DEFAULT_WORKSPACE_NAME",
        "EMIDAF Research Workspace",
    ).strip()

    workspace_path = Path(
        os.environ.get(
            "EMIDAF_WORKSPACE_PATH",
            "workspace",
        )
    ).expanduser().resolve()

    workspace_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    existing_workspaces = repository.get_all()

    for workspace in existing_workspaces:
        if workspace.name == workspace_name:
            print(
                "WORKSPACE : déjà présent "
                f"(id={workspace.id}, "
                f"name={workspace.name})"
            )
            return 0

    workspace = WorkspaceModel(
        name=workspace_name,
        path=str(workspace_path),
        description=(
            "Espace de travail principal "
            "EMIDAF Research Lab"
        ),
    )

    workspace = repository.add(workspace)

    print(
        "WORKSPACE : créé "
        f"(id={workspace.id}, "
        f"name={workspace.name})"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
