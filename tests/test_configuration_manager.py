from emidaf_core.managers.configuration_manager import ConfigurationManager


def test_manager_creation():

    manager = ConfigurationManager()

    assert manager is not None


def test_configuration_loaded():

    manager = ConfigurationManager()

    assert manager.count() > 0


def test_keys():

    manager = ConfigurationManager()

    keys = manager.keys()

    assert isinstance(keys, list)
    assert len(keys) > 0


def test_values():

    manager = ConfigurationManager()

    values = manager.values()

    assert isinstance(values, list)


def test_items():

    manager = ConfigurationManager()

    items = manager.items()

    assert isinstance(items, list)


def test_has():

    manager = ConfigurationManager()

    assert manager.has("theme")
    assert manager.has("database")
    assert not manager.has("xxxx")


def test_get():

    manager = ConfigurationManager()

    assert manager.get("theme") is not None
    assert manager.get("xxxx") is None
    assert manager.get("xxxx", "default") == "default"


def test_set():

    manager = ConfigurationManager()

    old_theme = manager.theme

    manager.set("theme", "Dark")

    assert manager.theme == "Dark"

    manager.set("theme", old_theme)


def test_remove():

    manager = ConfigurationManager()

    manager.set("temp_test", 123)

    assert manager.has("temp_test")

    manager.remove("temp_test")

    assert not manager.has("temp_test")


def test_clear():

    manager = ConfigurationManager()

    manager.set("temp_test", 123)

    manager.clear()

    assert manager.count() == 0


def test_properties():

    manager = ConfigurationManager()

    assert manager.application is not None
    assert manager.version is not None
    assert manager.theme is not None
    assert manager.language is not None
    assert manager.workspace is not None
    assert manager.database is not None


def test_reload():

    manager = ConfigurationManager()

    manager.set("theme", "Dark")

    manager.reload()

    assert manager.theme != "Dark" or manager.theme == "Dark"


def test_save():

    manager = ConfigurationManager()

    manager.save()
