from emidaf_core.core.base_manager import BaseManager
from emidaf_core.core.base_service import BaseService
from emidaf_core.core.base_repository import BaseRepository


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


class DummyManager(BaseManager):

    def run(self):
        return self.service.execute()


def test_manager():

    manager = DummyManager(
        DummyService(
            MemoryRepository()
        )
    )

    assert manager.run() == "OK"