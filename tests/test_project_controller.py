from unittest.mock import Mock

from database.models.project_model import ProjectModel

from emidaf_core.controllers.project_controller import ProjectController


def create_controller():

    service = Mock()

    controller = ProjectController(service)

    return controller, service


def test_controller_creation():

    controller, service = create_controller()

    assert controller is not None


def test_create():

    controller, service = create_controller()

    project = ProjectModel(
        name="Test Project"
    )

    service.create_project.return_value = project

    result = controller.create(project)

    assert result == project

    service.create_project.assert_called_once_with(
        project
    )


def test_get():

    controller, service = create_controller()

    project = ProjectModel(
        name="Test Project"
    )

    service.get_project.return_value = project

    result = controller.get(1)

    assert result == project

    service.get_project.assert_called_once_with(1)


def test_get_all():

    controller, service = create_controller()

    projects = [
        ProjectModel(
            name="Project 1"
        ),
        ProjectModel(
            name="Project 2"
        )
    ]

    service.get_all_projects.return_value = projects

    result = controller.get_all()

    assert result == projects

    service.get_all_projects.assert_called_once_with()


def test_exists():

    controller, service = create_controller()

    service.project_exists.return_value = True

    result = controller.exists(10)

    assert result is True

    service.project_exists.assert_called_once_with(10)


def test_count():

    controller, service = create_controller()

    service.count_projects.return_value = 5

    result = controller.count()

    assert result == 5

    service.count_projects.assert_called_once_with()


def test_update():

    controller, service = create_controller()

    project = ProjectModel(
        name="Project Updated"
    )

    service.update_project.return_value = project

    result = controller.update(project)

    assert result == project

    service.update_project.assert_called_once_with(
        project
    )


def test_delete():

    controller, service = create_controller()

    service.delete_project.return_value = True

    result = controller.delete(10)

    assert result is True

    service.delete_project.assert_called_once_with(10)


def test_delete_all():

    controller, service = create_controller()

    controller.delete_all()

    service.delete_all.assert_called_once_with()
