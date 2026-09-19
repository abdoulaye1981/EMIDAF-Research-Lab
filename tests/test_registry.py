"""
=========================================================
EMIDAF Framework v1.0
---------------------------------------------------------
Unit tests for registry.py
=========================================================
"""

import unittest

from emidaf_core.registry import Registry


class TestRegistry(unittest.TestCase):
    """Unit tests for the Registry component."""

    def setUp(self) -> None:
        """Create a fresh registry before each test."""
        self.registry = Registry()

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def test_constructor(self) -> None:
        """The registry must be empty after construction."""
        self.assertEqual(self.registry.count(), 0)
        self.assertEqual(self.registry.list(), [])

    # --------------------------------------------------
    # register()
    # --------------------------------------------------

    def test_register(self) -> None:
        component = object()

        self.registry.register("database", component)

        self.assertEqual(self.registry.count(), 1)
        self.assertTrue(self.registry.exists("database"))

    def test_register_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            self.registry.register("", object())

    def test_register_none_component(self) -> None:
        with self.assertRaises(ValueError):
            self.registry.register("database", None)

    def test_register_duplicate(self) -> None:
        component = object()

        self.registry.register("database", component)

        with self.assertRaises(KeyError):
            self.registry.register("database", object())

    # --------------------------------------------------
    # get()
    # --------------------------------------------------

    def test_get_existing_component(self) -> None:
        component = object()

        self.registry.register("logger", component)

        self.assertIs(self.registry.get("logger"), component)

    def test_get_unknown_component(self) -> None:
        self.assertIsNone(self.registry.get("unknown"))

    # --------------------------------------------------
    # exists()
    # --------------------------------------------------

    def test_exists(self) -> None:
        component = object()

        self.registry.register("workspace", component)

        self.assertTrue(self.registry.exists("workspace"))
        self.assertFalse(self.registry.exists("database"))

    # --------------------------------------------------
    # unregister()
    # --------------------------------------------------

    def test_unregister(self) -> None:
        component = object()

        self.registry.register("workspace", component)

        self.registry.unregister("workspace")

        self.assertFalse(self.registry.exists("workspace"))
        self.assertEqual(self.registry.count(), 0)

    def test_unregister_unknown(self) -> None:
        self.registry.unregister("unknown")

        self.assertEqual(self.registry.count(), 0)

    # --------------------------------------------------
    # clear()
    # --------------------------------------------------

    def test_clear(self) -> None:
        self.registry.register("a", object())
        self.registry.register("b", object())
        self.registry.register("c", object())

        self.registry.clear()

        self.assertEqual(self.registry.count(), 0)
        self.assertEqual(self.registry.list(), [])

    # --------------------------------------------------
    # list()
    # --------------------------------------------------

    def test_list(self) -> None:
        self.registry.register("logger", object())
        self.registry.register("configuration", object())
        self.registry.register("workspace", object())

        self.assertEqual(
            self.registry.list(),
            [
                "configuration",
                "logger",
                "workspace",
            ],
        )

    # --------------------------------------------------
    # count()
    # --------------------------------------------------

    def test_count(self) -> None:
        self.assertEqual(self.registry.count(), 0)

        self.registry.register("one", object())
        self.assertEqual(self.registry.count(), 1)

        self.registry.register("two", object())
        self.assertEqual(self.registry.count(), 2)

        self.registry.unregister("one")
        self.assertEqual(self.registry.count(), 1)


if __name__ == "__main__":
    unittest.main()