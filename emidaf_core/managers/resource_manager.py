"""
=========================================================
EMIDAF Framework v1.0
Resource Manager
---------------------------------------------------------
Gestion centralisée des ressources du Framework
=========================================================
"""

from pathlib import Path
from typing import Optional


class ResourceManager:
    """
    Gestionnaire des ressources statiques d'EMIDAF.

    Responsabilités
    ----------------
    - Fournir les chemins vers les ressources
    - Vérifier leur existence
    - Centraliser tous les accès aux assets
    """

    def __init__(self, assets_directory: Optional[Path] = None):

        self._assets = assets_directory or Path("assets")

        self._images = self._assets / "images"

        self._icons = self._assets / "icons"

        self._css = self._assets / "css"

        self._reports = Path("reports")

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self) -> None:
        """
        Initialise le ResourceManager.
        """
        pass

    # =====================================================
    # DOSSIERS
    # =====================================================

    @property
    def assets(self) -> Path:
        return self._assets

    @property
    def images(self) -> Path:
        return self._images

    @property
    def icons(self) -> Path:
        return self._icons

    @property
    def css(self) -> Path:
        return self._css

    @property
    def reports(self) -> Path:
        return self._reports

    # =====================================================
    # ACCES AUX RESSOURCES
    # =====================================================

    def image(self, filename: str) -> Path:
        return self._images / filename

    def icon(self, filename: str) -> Path:
        return self._icons / filename

    def stylesheet(self, filename: str) -> Path:
        return self._css / filename

    def report_template(self) -> Path:
        return self._reports / "template.docx"

    # =====================================================
    # VALIDATION
    # =====================================================

    def exists(self, resource: Path) -> bool:
        return resource.exists()