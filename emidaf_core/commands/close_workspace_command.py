"""
=========================================================
Close Workspace Command
=========================================================
"""

from emidaf_core.commands.base_command import BaseCommand
from emidaf_core.modules.workspace.workspace_manager import (
    WorkspaceManager
)


class CloseWorkspaceCommand(BaseCommand):

    def __init__(self, manager: WorkspaceManager):

        self.manager = manager

    def execute(self):

        self.manager.close_workspace()