from emidaf_core.core.base_builder import BaseBuilder


class DummyBuilder(BaseBuilder):

    def build(self):

        self._result = {

            "ok": True

        }

        return self.finalize()


def test_builder():

    builder = DummyBuilder()

    result = builder.build()

    assert result["ok"]