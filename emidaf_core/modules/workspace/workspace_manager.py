"""
=========================================================
EMIDAF Framework v1.0
Workspace Manager
---------------------------------------------------------
Gestionnaire principal des Workspaces.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import List
from typing import Optional

from .workspace_builder import WorkspaceBuilder
from .workspace_loader import WorkspaceLoader
from .workspace_validator import WorkspaceValidator
from .workspace_metadata import WorkspaceMetadata


class WorkspaceManager:
    """
    Gestionnaire principal des Workspaces.

    Responsabilités
    ----------------
    - Créer
    - Ouvrir
    - Fermer
    - Renommer
    - Dupliquer
    - Archiver
    - Restaurer
    - Supprimer
    - Sauvegarder
    """

    def __init__(

        self,

        builder: WorkspaceBuilder,

        loader: WorkspaceLoader,

        validator: WorkspaceValidator

    ):

        self._builder = builder

        self._loader = loader

        self._validator = validator

        self._current_workspace = None

    # =====================================================
    # CREATE
    # =====================================================

    def create_workspace(

        self,

        workspace_path: Path,

        name: str,

        author: str = "",

        description: str = ""

    ) -> WorkspaceMetadata:

        self._validator.validate_name(name)

        self._validator.validate_path(workspace_path)

        self._validator.validate_permissions(workspace_path)

        self._validator.validate_not_exists(workspace_path)

        self._builder.build(

            workspace_path,

            name,

            author,

            description

        )

        workspace = self._loader.load(

            workspace_path

        )

        self._current_workspace = workspace

        return workspace

    # =====================================================
    # OPEN
    # =====================================================

    def open_workspace(

        self,

        workspace_path: Path

    ) -> WorkspaceMetadata:

        self._validator.validate_workspace(

            workspace_path

        )

        workspace = self._loader.load(

            workspace_path

        )

        self._current_workspace = workspace

        return workspace

    # =====================================================
    # CLOSE
    # =====================================================

    def close_workspace(self):

        self._current_workspace = None

    # =====================================================
    # SAVE
    # =====================================================

    def save_workspace(self):

        if self._current_workspace is None:

            return

        self._loader.save(

            self._current_workspace

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_workspace(

        self,

        workspace_path: Path

    ):

        self.close_workspace()

        import shutil

        shutil.rmtree(

            workspace_path

        )

    # =====================================================
    # CURRENT
    # =====================================================

    def get_current_workspace(

        self

    ) -> Optional[WorkspaceMetadata]:

        return self._current_workspace

    def set_current_workspace(

        self,

        workspace: WorkspaceMetadata

    ):

        self._current_workspace = workspace

    def has_workspace(self):

        return self._current_workspace is not None

    # =====================================================
    # INFORMATION
    # =====================================================

    def current_workspace_name(self):

        if self._current_workspace is None:

            return None

        return self._current_workspace.name

    # =====================================================
    # LIST
    # =====================================================

    def list_workspaces(

        self,

        root: Path

    ) -> List[str]:

        workspaces = []

        if not root.exists():

            return workspaces

        for folder in root.iterdir():

            if folder.is_dir():

                workspaces.append(

                    folder.name

                )

        return sorted(workspaces)