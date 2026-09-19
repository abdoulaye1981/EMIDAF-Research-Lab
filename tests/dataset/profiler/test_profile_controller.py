import pandas as pd

from emidaf_core.dataset.profiler.profile_controller import ProfileController


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
    controller = ProfileController(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = controller.profile(dataframe)

    assert result == "profile_result"
    assert service.calls[-1] == (
        "profile",
        dataframe,
        False,
    )


def test_profile_save():
    service = FakeService()
    controller = ProfileController(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = controller.profile(
        dataframe,
        save=True,
    )

    assert result == "profile_result"
    assert service.calls[-1] == (
        "profile",
        dataframe,
        True,
    )


def test_save():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.save("profile") == 1
    assert service.calls[-1] == (
        "save",
        "profile",
    )


def test_find():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.find(10) == "profile"
    assert service.calls[-1] == (
        "find",
        10,
    )


def test_find_all():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.find_all() == [
        "profile1",
        "profile2",
    ]


def test_exists():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.exists(10) is True


def test_count():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.count() == 2


def test_last():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.last() == "last_profile"


def test_search():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.search("test") == []


def test_datasets():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.datasets() == ["dataset1"]


def test_update():
    service = FakeService()
    controller = ProfileController(service)

    result = controller.update(
        5,
        "profile",
    )

    assert result is None
    assert service.calls[-1] == (
        "update",
        5,
        "profile",
    )


def test_delete():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.delete(5) is True
    assert service.calls[-1] == (
        "delete",
        5,
    )


def test_delete_all():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.delete_all() == 2
    assert service.calls[-1] == (
        "delete_all",
    )


def test_refresh():
    service = FakeService()
    controller = ProfileController(service)

    dataframe = pd.DataFrame({"age": [20, 21]})

    result = controller.refresh(
        dataframe,
        5,
    )

    assert result == "refreshed_profile"
    assert service.calls[-1] == (
        "refresh",
        dataframe,
        5,
    )


def test_duplicate():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.duplicate(5) == 3
    assert service.calls[-1] == (
        "duplicate",
        5,
    )


def test_compare():
    service = FakeService()
    controller = ProfileController(service)

    first = "profile1"
    second = "profile2"

    result = controller.compare(
        first,
        second,
    )

    assert result == {
        "quality_score": 5.0
    }

    assert service.calls[-1] == (
        "compare",
        first,
        second,
    )


def test_validate():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.validate("profile") is True


def test_statistics():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.statistics() == {
        "profiles": 2
    }


def test_is_empty():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.is_empty() is False


def test_export_json():
    service = FakeService()
    controller = ProfileController(service)

    controller.export_json(
        5,
        "/tmp/profile.json",
    )

    assert service.calls[-1] == (
        "export_json",
        5,
        "/tmp/profile.json",
    )


def test_import_json():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.import_json(
        "/tmp/profile.json"
    ) == 1


def test_backup():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.backup(
        "/tmp/backup"
    ) == 2


def test_restore():
    service = FakeService()
    controller = ProfileController(service)

    assert controller.restore(
        "/tmp/backup"
    ) == 2
