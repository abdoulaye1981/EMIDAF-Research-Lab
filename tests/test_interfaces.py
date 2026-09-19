from emidaf_core.interfaces.i_builder import IBuilder


class TestBuilder(IBuilder):

    def reset(self):
        self._result = None

    def build(self, value):
        self._result = value
        return self._result

    def validate(self):
        if self._result is None:
            raise RuntimeError("No result has been built.")

    def finalize(self):
        self.validate()
        return self._result


def test_builder_interface():

    builder = TestBuilder()

    builder.build("EMIDAF")

    assert builder.finalize() == "EMIDAF"


def test_builder_reset():

    builder = TestBuilder()

    builder.build("EMIDAF")

    builder.reset()

    assert builder._result is None
