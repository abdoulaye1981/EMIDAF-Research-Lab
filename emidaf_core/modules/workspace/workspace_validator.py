"""
=========================================================
EMIDAF Framework v1.0
Workspace Validator
---------------------------------------------------------
Validation des espaces de travail.
=========================================================
"""

from __future__ import annotations

import os

from pathlib import Path

from .workspace_constants import (
    CONFIG_FILE,
    DATABASE_FILE,
    METADATA_FILE,
    WORKSPACE_STRUCTURE
)

from .workspace_exceptions import (
    InvalidWorkspaceError,
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
    WorkspacePermissionError
)


class WorkspaceValidator:
    """
    Validation des espaces de travail.

    Responsabilités
    ----------------
    - Vérifier le nom
    - Vérifier le chemin
    - Vérifier les permissions
    - Vérifier la structure
    - Vérifier les fichiers obligatoires
    """

    # =====================================================
    # NAME
    # =====================================================

    def validate_name(self, name: str) -> None:
        """
        Vérifie le nom du workspace.
        """

        if not name:

            raise InvalidWorkspaceError(
                "Workspace name cannot be empty."
            )

        if not name.strip():

            raise InvalidWorkspaceError(
                "Workspace name cannot be empty."
            )

        invalid = '<>:"/\\|?*'

        for character in invalid:

            if character in name:

                raise InvalidWorkspaceError(
                    f"Invalid character '{character}' in workspace name."
                )

    # =====================================================
    # PATH
    # =====================================================

    def validate_path(self, path: Path) -> None:
        """
        Vérifie que le chemin est valide.
        """

        if not isinstance(path, Path):

            raise InvalidWorkspaceError(
                "Workspace path must be a pathlib.Path."
            )

        if not path.is_absolute():

            raise InvalidWorkspaceError(
                "Workspace path must be absolute."
            )

    # =====================================================
    # PERMISSIONS
    # =====================================================

    def validate_permissions(self, path: Path) -> None:
        """
        Vérifie les droits d'écriture.
        """

        parent = path.parent

        if not parent.exists():

            raise WorkspaceNotFoundError(
                f"Parent directory does not exist: {parent}"
            )

        if not os.access(parent, os.W_OK):

            raise WorkspacePermissionError(
                f"No write permission on: {parent}"
            )

    # =====================================================
    # EXISTENCE
    # =====================================================

    def validate_not_exists(self, path: Path) -> None:
        """
        Vérifie que le workspace n'existe pas.
        """

        if path.exists():

            raise WorkspaceAlreadyExistsError(
                f"Workspace already exists: {path}"
            )

    def validate_exists(self, path: Path) -> None:
        """
        Vérifie que le workspace existe.
        """

        if not path.exists():

            raise WorkspaceNotFoundError(
                f"Workspace not found: {path}"
            )

    # =====================================================
    # STRUCTURE
    # =====================================================

    def validate_structure(self, path: Path) -> None:
        """
        Vérifie la structure complète du workspace.
        """

        self.validate_exists(path)

        for folder, subfolders in WORKSPACE_STRUCTURE.items():

            directory = path / folder

            if not directory.exists():

                raise InvalidWorkspaceError(
                    f"Missing directory: {directory}"
                )

            for subfolder in subfolders:

                child = directory / subfolder

                if not child.exists():

                    raise InvalidWorkspaceError(
                        f"Missing directory: {child}"
                    )

    # =====================================================
    # FILES
    # =====================================================

    def validate_configuration(self, path: Path) -> None:
        """
        Vérifie le fichier de configuration.
        """

        file = path / CONFIG_FILE

        if not file.exists():

            raise InvalidWorkspaceError(
                f"Configuration file missing: {file}"
            )

    def validate_database(self, path: Path) -> None:
        """
        Vérifie la base SQLite.
        """

        file = path / DATABASE_FILE

        if not file.exists():

            raise InvalidWorkspaceError(
                f"Database file missing: {file}"
            )

    def validate_metadata(self, path: Path) -> None:
        """
        Vérifie les métadonnées.
        """

        file = path / METADATA_FILE

        if not file.exists():

            raise InvalidWorkspaceError(
                f"Metadata file missing: {file}"
            )

    # =====================================================
    # COMPLETE VALIDATION
    # =====================================================

    def validate_workspace(self, path: Path) -> None:
        """
        Validation complète d'un workspace.
        """

        self.validate_exists(path)

        self.validate_structure(path)

        self.validate_configuration(path)

        self.validate_database(path)

        self.validate_metadata(path)