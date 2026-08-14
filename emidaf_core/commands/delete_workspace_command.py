"""
=========================================================
Delete Workspace Command
=========================================================
"""

from pathlib import Path

from emidaf_core.commands.base_command import BaseCommand
from emidaf_core.modules.workspace.workspace_manager import (
    WorkspaceManager
)


class DeleteWorkspaceCommand(BaseCommand):

    def __init__(self, manager: WorkspaceManager):

        self.manager = manager

    def execute(self, workspace_path: Path):

        self.manager.delete_workspace(
            workspace_path
        )