"""
=========================================================
EMIDAF Framework v1.0
Theme Manager
---------------------------------------------------------
Gestion des thèmes de l'application
=========================================================
"""

from __future__ import annotations

from typing import Dict, List, Optional


class ThemeManager:
    """
    Gestionnaire des thèmes graphiques.

    Responsabilités
    ----------------
    - Gérer les thèmes disponibles
    - Définir le thème courant
    - Fournir les propriétés d'un thème

    Aucun composant graphique n'est manipulé ici.
    """

    def __init__(self) -> None:

        self._themes: Dict[str, dict] = {}

        self._current_theme: Optional[str] = None

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self) -> None:

        self.clear()

    # =====================================================
    # THEMES
    # =====================================================

    def register(self, name: str, theme: dict) -> None:

        self._themes[name] = theme

        if self._current_theme is None:
            self._current_theme = name

    def unregister(self, name: str) -> bool:

        if name not in self._themes:
            return False

        del self._themes[name]

        if self._current_theme == name:
            self._current_theme = None

        return True

    # =====================================================
    # CONSULTATION
    # =====================================================

    def exists(self, name: str) -> bool:

        return name in self._themes

    def get(self, name: str) -> Optional[dict]:

        return self._themes.get(name)

    def list(self) -> List[str]:

        return sorted(self._themes.keys())

    def count(self) -> int:

        return len(self._themes)

    # =====================================================
    # THEME COURANT
    # =====================================================

    def set_current(self, name: str) -> None:

        if name not in self._themes:
            raise KeyError(f"Unknown theme '{name}'.")

        self._current_theme = name

    def get_current(self) -> Optional[dict]:

        if self._current_theme is None:
            return None

        return self._themes[self._current_theme]

    def get_current_name(self) -> Optional[str]:

        return self._current_theme

    # =====================================================
    # NETTOYAGE
    # =====================================================

    def clear(self) -> None:

        self._themes.clear()

        self._current_theme = None