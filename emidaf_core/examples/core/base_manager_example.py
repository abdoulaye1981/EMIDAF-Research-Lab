from emidaf_core.core.base_manager import BaseManager

from tests.core.test_base_manager import (
    DummyService,
    MemoryRepository,
)


class ProfileManager(BaseManager):

    def run(self):

        return self.service.execute()


manager = ProfileManager(

    DummyService(

        MemoryRepository()

    )

)

print(

    manager.run()

)