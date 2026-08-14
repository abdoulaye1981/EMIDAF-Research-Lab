from tests.core.test_base_repository import MemoryRepository

repo = MemoryRepository()

repo.save(

    {

        "id": 1,

        "name": "Profile"

    }

)

print(

    repo.load(1)

)