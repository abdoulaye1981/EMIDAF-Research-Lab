"""
=========================================================
EMIDAF Framework v1.0
---------------------------------------------------------
Module : registry.py

Description :
    Central registry used to register and retrieve
    framework components.

Author :
    EMIDAF Development Team

Version :
    1.0.0
=========================================================
"""

from __future__ import annotations

from typing import Any


class Registry:
    """
    Central registry of the EMIDAF Framework.

    The Registry stores references to framework components
    such as managers, services or controllers.

    Notes
    -----
    - One component per unique name.
    - Components are stored by reference.
    - The registry contains no business logic.
    """

    def __init__(self) -> None:
        """
        Create an empty registry.
        """
        self._components: dict[str, Any] = {}

    def register(self, name: str, component: Any) -> None:
        """
        Register a component.

        Parameters
        ----------
        name : str
            Unique component name.

        component : Any
            Component instance.

        Raises
        ------
        ValueError
            If the name is empty.

        ValueError
            If component is None.

        KeyError
            If the component already exists.
        """

        if not name or not name.strip():
            raise ValueError("Component name cannot be empty.")

        if component is None:
            raise ValueError("Component cannot be None.")

        if name in self._components:
            raise KeyError(f"Component '{name}' is already registered.")

        self._components[name] = component

    def get(self, name: str) -> Any | None:
        """
        Retrieve a registered component.

        Parameters
        ----------
        name : str

        Returns
        -------
        Any | None
        """
        return self._components.get(name)

    def exists(self, name: str) -> bool:
        """
        Check whether a component exists.
        """
        return name in self._components

    def unregister(self, name: str) -> None:
        """
        Remove a component.

        No exception is raised if the component
        does not exist.
        """
        self._components.pop(name, None)

    def clear(self) -> None:
        """
        Remove every registered component.
        """
        self._components.clear()

    def list(self) -> list[str]:
        """
        Return the sorted component names.
        """
        return sorted(self._components.keys())

    def count(self) -> int:
        """
        Return the number of registered components.
        """
        return len(self._components)