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


def test_repository():

    repo = MemoryRepository()

    repo.save({"id": 1, "name": "A"})

    assert repo.exists(1)

    assert repo.count() == 1

    repo.delete(1)

    assert repo.count() == 0