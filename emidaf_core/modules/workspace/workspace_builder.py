"""
=========================================================
EMIDAF Framework v1.0
Workspace Builder
---------------------------------------------------------
Construction complète d'un Workspace EMIDAF.
=========================================================
"""

from __future__ import annotations

import json

from datetime import datetime
from dataclasses import asdict
from pathlib import Path

import yaml

from database.database_manager import DatabaseManager

from .workspace_constants import (
    WORKSPACE_STRUCTURE,
    CONFIG_FILE,
    DATABASE_FILE,
    METADATA_FILE
)

from .workspace_metadata import WorkspaceMetadata

from .workspace_utils import generate_workspace_id


class WorkspaceBuilder:
    """
    Construit un Workspace EMIDAF.

    Responsabilités
    ----------------
    - Créer l'arborescence
    - Créer config.yaml
    - Créer metadata.json
    - Initialiser SQLite
    """

    def __init__(
        self,
        database_manager: DatabaseManager
    ):

        self._database_manager = database_manager

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        workspace_path: Path,
        name: str,
        author: str = "",
        description: str = ""
    ) -> None:
        """
        Construit complètement un Workspace.
        """

        workspace_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_directories(workspace_path)

        self._create_configuration(
            workspace_path
        )

        self._create_metadata(
            workspace_path,
            name,
            author,
            description
        )

        self._create_database(
            workspace_path
        )

    # =====================================================
    # DIRECTORIES
    # =====================================================

    def _create_directories(
        self,
        workspace_path: Path
    ) -> None:

        for folder, children in WORKSPACE_STRUCTURE.items():

            root = workspace_path / folder

            root.mkdir(
                parents=True,
                exist_ok=True
            )

            for child in children:

                (
                    root / child
                ).mkdir(
                    parents=True,
                    exist_ok=True
                )

    # =====================================================
    # CONFIGURATION
    # =====================================================

    def _create_configuration(
        self,
        workspace_path: Path
    ) -> None:

        config = {

            "workspace": {

                "version": "1.0.0",

                "language": "fr",

                "theme": "light",

                "autosave": True

            }

        }

        file = workspace_path / CONFIG_FILE

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as stream:

            yaml.safe_dump(
                config,
                stream,
                sort_keys=False,
                allow_unicode=True
            )

    # =====================================================
    # METADATA
    # =====================================================

    def _create_metadata(
           self,
           workspace_path: Path,
           name: str,
           author: str,
           description: str
    ) -> None:

       metadata = WorkspaceMetadata(
                workspace_id=generate_workspace_id(),
                name=name,
                version="1.0.0",
                author=author,
                description=description,
                created_at=datetime.now(),
                last_opened=datetime.now()
       )


       file = workspace_path / METADATA_FILE

       with open(
          file,
          "w",
           encoding="utf-8"
       ) as stream:

           json.dump(
               {
                "workspace_id": metadata.workspace_id,
                "name": metadata.name,
                "version": metadata.version,
                "author": metadata.author,
                "description": metadata.description,
                "created_at": metadata.created_at.isoformat(),
                "last_opened": metadata.last_opened.isoformat()
               },
               stream,
               indent=4,
               ensure_ascii=False
           )

    # =====================================================
    # DATABASE
    # =====================================================

    def _create_database(
         self,
         workspace_path: Path
    ) -> None:

         database = workspace_path / DATABASE_FILE

         self._database_manager.create_database(
               database
         )
