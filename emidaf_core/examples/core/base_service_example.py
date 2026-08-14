from tests.core.test_base_service import MemoryRepository
from emidaf_core.core.base_service import BaseService


class ProfileService(BaseService):

    def execute(self):

        return "Profil exécuté"


repository = MemoryRepository()

service = ProfileService(repository)

service.save(

    {

        "id": 1,

        "name": "Profile"

    }

)

print(

    service.load(1)

)