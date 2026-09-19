import pandas as pd

from emidaf_core.dataset.profiler.profile_manager import ProfileManager


class FakeService:

    def __init__(self):
        self.calls = []

    def profile(self, dataframe, save=False):
        self.calls.append(("profile", dataframe, save))
        return "profile_result"

    def save(self, profile):
        self.calls.append(("save", profile))
        return 1

    def find(self, profile_id):
        self.calls.append(("find", profile_id))
        return "profile"

    def find_all(self):
        self.calls.append(("find_all",))
        return ["profile1", "profile2"]

    def exists(self, profile_id):
        self.calls.append(("exists", profile_id))
        return True

    def count(self):
        self.calls.append(("count",))
        return 2

    def last(self):
        self.calls.append(("last",))
        return "last_profile"

    def search(self, query):
        self.calls.append(("search", query))
        return []

    def datasets(self):
        self.calls.append(("datasets",))
        return ["dataset1"]

    def update(self, profile_id, profile):
        self.calls.append(("update", profile_id, profile))
        return None

    def delete(self, profile_id):
        self.calls.append(("delete", profile_id))
        return True

    def delete_all(self):
        self.calls.append(("delete_all",))
        return 2

    def refresh(self, dataframe, profile_id):
        self.calls.append(("refresh", dataframe, profile_id))
        return "refreshed_profile"

    def duplicate(self, profile_id):
        self.calls.append(("duplicate", profile_id))
        return 3

    def compare(self, first, second):
        self.calls.append(("compare", first, second))
        return {"quality_score": 5.0}

    def validate(self, profile):
        self.calls.append(("validate", profile))
        return True

    def statistics(self):
        self.calls.append(("statistics",))
        return {"profiles": 2}

    def is_empty(self):
        self.calls.append(("is_empty",))
        return False

    def export_json(self, profile_id, path):
        self.calls.append(("export_json", profile_id, path))
        return None

    def import_json(self, path):
        self.calls.append(("import_json", path))
        return 1

    def backup(self, path):
        self.calls.append(("backup", path))
        return 2

    def restore(self, path):
        self.calls.append(("restore", path))
        return 2


def test_profile():
    service = FakeService()
    manager = ProfileManager(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = manager.profile(dataframe)

    assert result == "profile_result"
    assert service.calls[-1] == ("profile", dataframe, False)


def test_profile_save():
    service = FakeService()
    manager = ProfileManager(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = manager.profile(
        dataframe,
        save=True,
    )

    assert result == "profile_result"
    assert service.calls[-1] == ("profile", dataframe, True)


def test_run_with_dataframe():
    service = FakeService()
    manager = ProfileManager(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = manager.run(dataframe)

    assert result == "profile_result"


def test_run_without_dataframe():
    service = FakeService()
    manager = ProfileManager(service)

    result = manager.run()

    assert result == ["profile1", "profile2"]
    assert service.calls[-1] == ("find_all",)


def test_save():
    service = FakeService()
    manager = ProfileManager(service)

    result = manager.save("profile")

    assert result == 1
    assert service.calls[-1] == ("save", "profile")


def test_find():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.find(10) == "profile"
    assert service.calls[-1] == ("find", 10)


def test_find_all():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.find_all() == ["profile1", "profile2"]


def test_exists():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.exists(10) is True


def test_count():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.count() == 2


def test_last():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.last() == "last_profile"


def test_search():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.search("test") == []


def test_datasets():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.datasets() == ["dataset1"]


def test_update():
    service = FakeService()
    manager = ProfileManager(service)

    result = manager.update(5, "profile")

    assert result is None
    assert service.calls[-1] == ("update", 5, "profile")


def test_delete():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.delete(5) is True
    assert service.calls[-1] == ("delete", 5)


def test_clear():
    service = FakeService()
    manager = ProfileManager(service)

    manager.clear()

    assert service.calls[-1] == ("delete_all",)


def test_refresh():
    service = FakeService()
    manager = ProfileManager(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = manager.refresh(dataframe, 5)

    assert result == "refreshed_profile"
    assert service.calls[-1] == ("refresh", dataframe, 5)


def test_duplicate():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.duplicate(5) == 3
    assert service.calls[-1] == ("duplicate", 5)


def test_compare():
    service = FakeService()
    manager = ProfileManager(service)

    first = "profile1"
    second = "profile2"

    result = manager.compare(first, second)

    assert result == {"quality_score": 5.0}
    assert service.calls[-1] == (
        "compare",
        first,
        second,
    )


def test_validate():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.validate("profile") is True


def test_statistics():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.statistics() == {"profiles": 2}


def test_is_empty():
    service = FakeService()
    manager = ProfileManager(service)

    assert manager.is_empty() is False


def test_len():
    service = FakeService()
    manager = ProfileManager(service)

    assert len(manager) == 2


def test_contains():
    service = FakeService()
    manager = ProfileManager(service)

    assert 5 in manager
