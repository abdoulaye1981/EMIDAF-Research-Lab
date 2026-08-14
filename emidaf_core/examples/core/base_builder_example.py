from emidaf_core.core.base_builder import BaseBuilder


class PersonBuilder(BaseBuilder):

    def build(self):

        self._result = {

            "name": "Abdoulaye",

            "country": "Senegal"

        }

        return self.finalize()


builder = PersonBuilder()

print(

    builder.build()

)