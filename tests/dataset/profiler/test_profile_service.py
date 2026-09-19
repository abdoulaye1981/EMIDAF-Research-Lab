import json

import pandas as pd
import pytest

from emidaf_core.dataset.profiler.profile_service import ProfileService


class FakeProfiler:
    def __init__(self, profile):
        self._profile = profile

    def profile(self, dataframe):
        return self._profile


class FakeRepository:
    def __init__(self, profile=None):
        self.profile = profile
        self.saved = []
        self.updated = []
        self.deleted = []
        self.imported = []
        self.backed_up = []
        self.restored = []

    def save(self, profile):
        self.saved.append(profile)
        return 1

    def update(self, profile_id, profile):
        self.updated.append((profile_id, profile))

    def find_by_id(self, profile_id):
        return self.profile

    def find_all(self):
        return [self.profile] if self.profile is not None else []

    def exists(self, profile_id):
        return self.profile is not None

    def count(self):
        return 1 if self.profile is not None else 0

    def delete(self, profile_id):
        self.deleted.append(profile_id)
        return True

    def delete_all(self):
        return 1

    def duplicate(self, profile_id):
        return 2

    def export_json(self, profile_id, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.profile, file, default=str)

    def import_json(self, filename):
        self.imported.append(filename)
        return 1

    def backup(self, directory):
        self.backed_up.append(directory)
        return 1

    def restore(self, directory):
        self.restored.append(directory)
        return 1

    def last(self):
        return self.profile

    def search(self, keyword):
        return []

    def datasets(self):
        return []

    def is_empty(self):
        return self.profile is None


class FakeBuilder:
    pass


def make_profile():
    profile = type("ProfileResult", (), {})()

    summary = type("Summary", (), {})()
    summary.rows = 100
    summary.columns = 5
    summary.quality_score = 90.0
    summary.overall_score = 85.0
    summary.missing_values = 10
    summary.duplicate_rows = 2

    profile.summary = summary
    profile.profile_name = "Profil test"
    profile.is_valid = True
    return profile


@pytest.fixture
def profile():
    return make_profile()


@pytest.fixture
def repository(profile):
    return FakeRepository(profile)


@pytest.fixture
def service(repository):
    profiler = FakeProfiler(make_profile())

    service = ProfileService(
        profiler=profiler,
        builder=FakeBuilder(),
        repository=repository,
    )

    return service


def test_profile(service):
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22],
            "score": [10, 12, 15],
        }
    )

    result = service.profile(dataframe)

    assert result is not None


def test_profile_save(service, repository):
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22],
            "score": [10, 12, 15],
        }
    )

    result = service.profile(
        dataframe,
        save=True,
    )

    assert result is not None
    assert len(repository.saved) == 1


def test_save(service, repository, profile):
    result = service.save(profile)

    assert result == 1
    assert repository.saved == [profile]


def test_find(service, profile):
    result = service.find(1)

    assert result is profile


def test_find_all(service):
    result = service.find_all()

    assert len(result) == 1


def test_exists(service):
    assert service.exists(1) is True


def test_count(service):
    assert service.count() == 1


def test_update(service, repository, profile):
    service.update(1, profile)

    assert repository.updated == [(1, profile)]


def test_delete(service, repository):
    result = service.delete(1)

    assert result is True
    assert repository.deleted == [1]


def test_delete_nonexistent():
    repository = FakeRepository(profile=None)

    service = ProfileService(
        profiler=FakeProfiler(make_profile()),
        builder=FakeBuilder(),
        repository=repository,
    )

    assert service.delete(1) is False


def test_delete_all(service):
    assert service.delete_all() == 1


def test_refresh(service, repository):
    dataframe = pd.DataFrame(
        {
            "age": [20, 21, 22],
            "score": [10, 12, 15],
        }
    )

    result = service.refresh(
        dataframe,
        1,
    )

    assert result is not None
    assert repository.updated[0][0] == 1


def test_duplicate(service):
    assert service.duplicate(1) == 2


def test_compare(service, profile):
    second = make_profile()
    second.summary.quality_score = 95.0
    second.summary.overall_score = 90.0

    result = service.compare(
        profile,
        second,
    )

    assert result["rows"] == 0
    assert result["columns"] == 0
    assert result["quality_score"] == 5.0
    assert result["overall_score"] == 5.0


def test_last(service, profile):
    assert service.last() is profile


def test_search(service):
    assert service.search("test") == []


def test_datasets(service):
    assert service.datasets() == []


def test_is_empty(service):
    assert service.is_empty() is False

def test_validate(service, profile):
    assert service.validate(profile) is True

def test_statistics(service):
    result = service.statistics()

    assert result["profiles"] == 1
    assert result["empty"] is False


def test_len(service):
    assert len(service) == 1


def test_contains(service):
    assert 1 in service


def test_str(service):
    assert "ProfileService" in str(service)


def test_repr(service):
    assert "ProfileService" in repr(service)
