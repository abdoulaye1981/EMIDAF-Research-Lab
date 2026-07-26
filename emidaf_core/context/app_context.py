from typing import Optional

from emidaf_core.entities.project import Project


class AppContext:

    def __init__(self):

        self.current_project: Optional[Project] = None

        self.current_dataset = None

        self.current_user = None

        self.current_experiment = None