from emidaf_core.core.base_repository import BaseRepository
from emidaf_core.core.base_service import BaseService


class MemoryRepository(BaseRepository):

    def __init__(self):

        super().__init__()

        self.storage = {}

    def save(self, obj):

        self.storage[obj["id"]] = obj

        return obj["id"]

    def load(self, identifier):

        return self.storage.get(identifier)

    def update(self, identifier, obj):

        self.storage[identifier] = obj

        return obj

    def delete(self, identifier):

        self.storage.pop(identifier, None)

    def exists(self, identifier):

        return identifier in self.storage

    def count(self):

        return len(self.storage)

    def clear(self):

        self.storage.clear()


class DummyService(BaseService):

    def execute(self):

        return "OK"


def test_service():

    repo = MemoryRepository()

    service = DummyService(repo)

    service.save({"id": 1})

    assert service.exists(1)

    assert service.count() == 1