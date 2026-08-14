"""
=========================================================
EMIDAF Framework
Visualization Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat d'une visualisation.

Utilisé par

- Matplotlib
- Plotly
- Seaborn
- Bokeh
- Altair
- Dash
- Report Generator
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .base_result import BaseResult


@dataclass(slots=True)
class VisualizationResult(BaseResult):
    """
    Résultat d'une visualisation.
    """

    category: str = "Visualization"

    # =====================================================
    # Informations générales
    # =====================================================

    title: str = ""

    subtitle: str = ""

    description: str = ""

    chart_type: str = ""

    library: str = ""

    theme: str = ""

    # =====================================================
    # Axes
    # =====================================================

    x_label: str = ""

    y_label: str = ""

    z_label: str = ""

    x_variable: str = ""

    y_variable: str = ""

    z_variable: str = ""

    # =====================================================
    # Figure
    # =====================================================

    width: int = 1200

    height: int = 700

    dpi: int = 100

    interactive: bool = False

    # =====================================================
    # Fichiers
    # =====================================================

    figure = None

    axes = None

    file_path: str = ""

    html_path: str = ""

    png_path: str = ""

    svg_path: str = ""

    pdf_path: str = ""

    # =====================================================
    # Données
    # =====================================================

    rows: int = 0

    columns: int = 0

    variables: list[str] = field(
        default_factory=list
    )

    parameters: dict = field(
        default_factory=dict
    )

    metadata: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Validation
    # =====================================================

    def has_figure(self):

        return self.figure is not None

    def is_interactive(self):

        return self.interactive

    def is_saved(self):

        return self.file_path != ""

    # =====================================================
    # Export
    # =====================================================

    def add_variable(self, variable: str):

        self.variables.append(variable)

    def add_parameter(self, key, value):

        self.parameters[key] = value

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Title": self.title,

            "Type": self.chart_type,

            "Library": self.library,

            "Variables": self.variables,

            "Interactive": self.interactive,

            "Saved": self.is_saved()

        }

    # =====================================================
    # Export compact
    # =====================================================

    def compact(self):

        return {

            "title": self.title,

            "type": self.chart_type,

            "library": self.library

        }

    # =====================================================
    # Représentation
    # =====================================================

    def __repr__(self):

        return (

            f"VisualizationResult("

            f"title='{self.title}', "

            f"type='{self.chart_type}', "

            f"library='{self.library}'"

            f")"

        )