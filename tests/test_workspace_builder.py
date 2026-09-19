from pathlib import Path

import yaml

from database.database_manager import DatabaseManager
from database.providers.sqlite_provider import SQLiteProvider

from emidaf_core.modules.workspace.workspace_builder import WorkspaceBuilder
from emidaf_core.modules.workspace.workspace_constants import (
    WORKSPACE_STRUCTURE,
    CONFIG_FILE,
    DATABASE_FILE,
    METADATA_FILE,
)


def create_builder():
    provider = SQLiteProvider("sqlite:///:memory:")
    database_manager = DatabaseManager(provider)
    return WorkspaceBuilder(database_manager)


def test_build_creates_workspace(tmp_path):

    workspace_path = tmp_path / "test_workspace"

    builder = create_builder()

    builder.build(
        workspace_path=workspace_path,
        name="TEST_WORKSPACE",
        author="EMIDAF",
        description="Workspace de test",
    )

    assert workspace_path.exists()
    assert workspace_path.is_dir()


def test_build_creates_directories(tmp_path):

    workspace_path = tmp_path / "test_workspace"

    builder = create_builder()

    builder.build(
        workspace_path=workspace_path,
        name="TEST_WORKSPACE",
        author="EMIDAF",
        description="Workspace de test",
    )

    for folder, children in WORKSPACE_STRUCTURE.items():

        root = workspace_path / folder

        assert root.exists()
        assert root.is_dir()

        for child in children:

            child_path = root / child

            assert child_path.exists()
            assert child_path.is_dir()


def test_build_creates_configuration(tmp_path):

    workspace_path = tmp_path / "test_workspace"

    builder = create_builder()

    builder.build(
        workspace_path=workspace_path,
        name="TEST_WORKSPACE",
    )

    config_path = workspace_path / CONFIG_FILE

    assert config_path.exists()
    assert config_path.is_file()

    with open(
        config_path,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    assert "workspace" in config

    assert config["workspace"]["version"] == "1.0.0"
    assert config["workspace"]["language"] == "fr"
    assert config["workspace"]["theme"] == "light"
    assert config["workspace"]["autosave"] is True


def test_build_creates_metadata(tmp_path):

    workspace_path = tmp_path / "test_workspace"

    builder = create_builder()

    builder.build(
        workspace_path=workspace_path,
        name="TEST_WORKSPACE",
        author="EMIDAF",
        description="Workspace de test",
    )

    metadata_path = workspace_path / METADATA_FILE

    assert metadata_path.exists()
    assert metadata_path.is_file()

    import json

    with open(
        metadata_path,
        "r",
        encoding="utf-8",
    ) as file:

        metadata = json.load(file)

    assert metadata["name"] == "TEST_WORKSPACE"
    assert metadata["author"] == "EMIDAF"
    assert metadata["description"] == "Workspace de test"
    assert metadata["version"] == "1.0.0"
    assert "workspace_id" in metadata
    assert metadata["workspace_id"]


def test_build_creates_database(tmp_path):

    workspace_path = tmp_path / "test_workspace"

    builder = create_builder()

    builder.build(
        workspace_path=workspace_path,
        name="TEST_WORKSPACE",
    )

    database_path = workspace_path / DATABASE_FILE

    assert database_path.exists()
    assert database_path.is_file()
    assert database_path.stat().st_size > 0
