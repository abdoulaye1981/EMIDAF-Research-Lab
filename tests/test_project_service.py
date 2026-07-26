from emidaf_core.services.project_service import ProjectService

service = ProjectService()

projects = service.get_projects()

print("Nombre de projets :", len(projects))

for project in projects:
    print(project)