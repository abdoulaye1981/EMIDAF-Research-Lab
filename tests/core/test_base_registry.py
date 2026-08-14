from emidaf_core.core.base_registry import BaseRegistry


def test_register():

    registry = BaseRegistry()

    registry.register(

        "test",

        10

    )

    assert registry.get("test") == 10


def test_exists():

    registry = BaseRegistry()

    registry.register(

        "x",

        15

    )

    assert registry.exists("x")


def test_unregister():

    registry = BaseRegistry()

    registry.register(

        "x",

        12

    )

    registry.unregister("x")

    assert not registry.exists("x")


def test_clear():

    registry = BaseRegistry()

    registry.register("a", 1)

    registry.register("b", 2)

    registry.clear()

    assert registry.size == 0