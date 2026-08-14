"""
=========================================================
EMIDAF Framework v1.0
Session Manager
---------------------------------------------------------
Gestion de la session de travail
=========================================================
"""

from __future__ import annotations

from typing import Any, Optional


class SessionManager:
    """
    Gestionnaire de la session de travail.

    Responsabilités
    ----------------
    - Gérer le workspace courant
    - Gérer le projet courant
    - Gérer le dataset courant
    - Gérer le thème courant
    - Gérer la langue
    - Stocker les préférences de session

    Ce manager ne contient aucune logique métier.
    """

    def __init__(self) -> None:

        self.initialize()

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self) -> None:

        self._workspace = None
        self._project = None
        self._dataset = None
        self._theme = None

        self._language = "fr"

        self._preferences: dict[str, Any] = {}

    # =====================================================
    # WORKSPACE
    # =====================================================

    def set_workspace(self, workspace: Any) -> None:
        self._workspace = workspace

    def get_workspace(self) -> Optional[Any]:
        return self._workspace

    # =====================================================
    # PROJECT
    # =====================================================

    def set_project(self, project: Any) -> None:
        self._project = project

    def get_project(self) -> Optional[Any]:
        return self._project

    def has_project(self) -> bool:
        return self._project is not None

    # =====================================================
    # DATASET
    # =====================================================

    def set_dataset(self, dataset: Any) -> None:
        self._dataset = dataset

    def get_dataset(self) -> Optional[Any]:
        return self._dataset

    def has_dataset(self) -> bool:
        return self._dataset is not None

    # =====================================================
    # THEME
    # =====================================================

    def set_theme(self, theme: Any) -> None:
        self._theme = theme

    def get_theme(self) -> Optional[Any]:
        return self._theme

    # =====================================================
    # LANGUE
    # =====================================================

    def set_language(self, language: str) -> None:
        self._language = language

    def get_language(self) -> str:
        return self._language

    # =====================================================
    # PREFERENCES
    # =====================================================

    def set_preference(self, key: str, value: Any) -> None:
        self._preferences[key] = value

    def get_preference(self, key: str, default: Any = None) -> Any:
        return self._preferences.get(key, default)

    def remove_preference(self, key: str) -> None:
        self._preferences.pop(key, None)

    def clear_preferences(self) -> None:
        self._preferences.clear()

    # =====================================================
    # SESSION
    # =====================================================

    def clear(self) -> None:
        """
        Réinitialise complètement la session.
        """
        self.initialize()