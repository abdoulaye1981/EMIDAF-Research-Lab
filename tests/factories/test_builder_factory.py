import pytest

from emidaf_core.factories.builder_factory import BuilderFactory


def test_list_builders():
    builders = BuilderFactory.list()

    assert "project" in builders
    assert "workspace" in builders
    assert "profile" in builders
    assert "missing" in builders
    assert "dataset" in builders


def test_exists_known_builder():
    assert BuilderFactory.exists("project")
    assert BuilderFactory.exists("workspace")
    assert BuilderFactory.exists("profile")
    assert BuilderFactory.exists("missing")
    assert BuilderFactory.exists("dataset")


def test_exists_unknown_builder():
    assert not BuilderFactory.exists("unknown")


def test_create_unknown_builder():
    with pytest.raises(ValueError):
        BuilderFactory.create("unknown")
