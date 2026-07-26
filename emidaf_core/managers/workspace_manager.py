from pathlib import Path


class WorkspaceManager:

    def __init__(self):

        self.workspace = Path("workspace/projects")

    def initialize(self):

        self.workspace.mkdir(

            parents=True,

            exist_ok=True

        )

    def list_projects(self):

        return [

            p for p in self.workspace.iterdir()

            if p.is_dir()

        ]