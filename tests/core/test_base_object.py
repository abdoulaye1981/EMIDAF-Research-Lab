from emidaf_core.core.base_object import BaseObject


class TestObject(BaseObject):
    pass


def test_creation():

    obj = TestObject()

    assert obj.id is not None

    assert obj.metadata == {}

    assert obj.tags == set()


def test_metadata():

    obj = TestObject()

    obj.set_metadata("author", "Abdoulaye")

    assert obj.get_metadata("author") == "Abdoulaye"


def test_tags():

    obj = TestObject()

    obj.add_tag("dataset")

    assert obj.has_tag("dataset")