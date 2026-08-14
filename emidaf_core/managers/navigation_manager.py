"""
=========================================================
EMIDAF Framework v1.0
Navigation Manager
=========================================================
"""

from typing import List, Optional


class NavigationManager:
    """
    Gestionnaire de la navigation de l'application.
    """

    def __init__(self):

        self._current_page: Optional[str] = None

        self._history: List[str] = []

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self) -> None:

        self.clear()

    # =====================================================
    # NAVIGATION
    # =====================================================

    def navigate(self, page: str) -> None:

        if self._current_page is not None:

            self._history.append(self._current_page)

        self._current_page = page

    def current(self) -> Optional[str]:

        return self._current_page

    def previous(self) -> Optional[str]:

        if not self._history:
            return None

        return self._history[-1]

    def back(self) -> Optional[str]:

        if not self._history:
            return None

        self._current_page = self._history.pop()

        return self._current_page

    # =====================================================
    # INFORMATIONS
    # =====================================================

    def history(self) -> List[str]:

        return self._history.copy()

    def can_go_back(self) -> bool:

        return len(self._history) > 0

    # =====================================================
    # NETTOYAGE
    # =====================================================

    def clear(self) -> None:

        self._current_page = None

        self._history.clear()