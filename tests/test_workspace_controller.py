from unittest.mock import Mock

from database.models.workspace_model import WorkspaceModel

from emidaf_core.controllers.workspace_controller import WorkspaceController


def create_controller():

    service = Mock()

    controller = WorkspaceController(service)

    return controller, service


def test_controller_creation():

    controller, service = create_controller()

    assert controller is not None


def test_create():

    controller, service = create_controller()

    workspace = WorkspaceModel(
        name="Test Workspace",
        path="/tmp/test_workspace"
    )

    service.create_workspace.return_value = workspace

    result = controller.create(workspace)

    assert result == workspace

    service.create_workspace.assert_called_once_with(
        workspace
    )


def test_get():

    controller, service = create_controller()

    workspace = WorkspaceModel(
        name="Test Workspace",
        path="/tmp/test_workspace"
    )

    service.get_workspace.return_value = workspace

    result = controller.get(1)

    assert result == workspace

    service.get_workspace.assert_called_once_with(1)


def test_get_all():

    controller, service = create_controller()

    workspaces = [
        WorkspaceModel(
            name="Workspace 1",
            path="/tmp/workspace1"
        ),
        WorkspaceModel(
            name="Workspace 2",
            path="/tmp/workspace2"
        )
    ]

    service.get_all_workspaces.return_value = workspaces

    result = controller.get_all()

    assert result == workspaces

    service.get_all_workspaces.assert_called_once_with()


def test_exists():

    controller, service = create_controller()

    service.workspace_exists.return_value = True

    result = controller.exists(10)

    assert result is True

    service.workspace_exists.assert_called_once_with(10)


def test_count():

    controller, service = create_controller()

    service.count_workspaces.return_value = 5

    result = controller.count()

    assert result == 5

    service.count_workspaces.assert_called_once_with()


def test_update():

    controller, service = create_controller()

    workspace = WorkspaceModel(
        name="Workspace Updated",
        path="/tmp/workspace_updated"
    )

    service.update_workspace.return_value = workspace

    result = controller.update(workspace)

    assert result == workspace

    service.update_workspace.assert_called_once_with(
        workspace
    )


def test_delete():

    controller, service = create_controller()

    service.delete_workspace.return_value = True

    result = controller.delete(10)

    assert result is True

    service.delete_workspace.assert_called_once_with(10)


def test_delete_all():

    controller, service = create_controller()

    controller.delete_all()

    service.delete_all.assert_called_once_with()
