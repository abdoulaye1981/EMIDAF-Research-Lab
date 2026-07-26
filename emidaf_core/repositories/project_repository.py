from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import Project as ProjectModel

from emidaf_core.entities.project import Project


class ProjectRepository:

    def __init__(self):

        self.db: Session = SessionLocal()

    def create(self, project: Project):

        db_project = ProjectModel(

            name=project.name,

            description=project.description,

            author=project.author,

            created_at=project.created_at,

            updated_at=project.updated_at

        )

        self.db.add(db_project)

        self.db.commit()

        self.db.refresh(db_project)

        project.id = db_project.id

        return project

    def get_all(self):

        projects = self.db.query(ProjectModel).all()

        result = []

        for p in projects:

            result.append(

                Project(

                    id=p.id,

                    name=p.name,

                    description=p.description,

                    author=p.author,

                    workspace="",

                    created_at=p.created_at,

                    updated_at=p.updated_at

                )

            )

        return result