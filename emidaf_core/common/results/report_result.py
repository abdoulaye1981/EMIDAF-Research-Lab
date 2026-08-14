"""
=========================================================
EMIDAF Framework
Report Result
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Résultat de la génération d'un rapport.

Utilisé par

- HTML Reporter
- PDF Reporter
- DOCX Reporter
- Markdown Reporter
- Excel Reporter
- PowerPoint Reporter
- LaTeX Reporter
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .base_result import BaseResult


@dataclass(slots=True)
class ReportResult(BaseResult):
    """
    Résultat d'un rapport EMIDAF.
    """

    category: str = "Reporting"

    # =====================================================
    # Informations générales
    # =====================================================

    report_name: str = ""

    report_type: str = ""

    author: str = ""

    organization: str = ""

    version: str = "1.0.0"

    language: str = "fr"

    theme: str = "default"

    # =====================================================
    # Contenu
    # =====================================================

    title: str = ""

    subtitle: str = ""

    summary: str = ""

    sections: list[str] = field(
        default_factory=list
    )

    figures: list[str] = field(
        default_factory=list
    )

    tables: list[str] = field(
        default_factory=list
    )

    appendices: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # Export
    # =====================================================

    output_directory: str = ""

    html_file: str = ""

    pdf_file: str = ""

    docx_file: str = ""

    latex_file: str = ""

    markdown_file: str = ""

    excel_file: str = ""

    powerpoint_file: str = ""

    json_file: str = ""

    # =====================================================
    # Taille
    # =====================================================

    pages: int = 0

    words: int = 0

    tables_count: int = 0

    figures_count: int = 0

    # =====================================================
    # Paramètres
    # =====================================================

    parameters: dict = field(
        default_factory=dict
    )

    metadata: dict = field(
        default_factory=dict
    )

    statistics: dict = field(
        default_factory=dict
    )

    # =====================================================
    # Validation
    # =====================================================

    def has_html(self):

        return self.html_file != ""

    def has_pdf(self):

        return self.pdf_file != ""

    def has_docx(self):

        return self.docx_file != ""

    def has_latex(self):

        return self.latex_file != ""

    def has_excel(self):

        return self.excel_file != ""

    def has_powerpoint(self):

        return self.powerpoint_file != ""

    # =====================================================
    # Ajout d'éléments
    # =====================================================

    def add_section(self, title: str):

        self.sections.append(title)

    def add_table(self, table: str):

        self.tables.append(table)

    def add_figure(self, figure: str):

        self.figures.append(figure)

    def add_appendix(self, appendix: str):

        self.appendices.append(appendix)

    # =====================================================
    # Résumé
    # =====================================================

    def summary(self):

        return {

            "Report": self.report_name,

            "Type": self.report_type,

            "Pages": self.pages,

            "Words": self.words,

            "Sections": len(self.sections),

            "Tables": len(self.tables),

            "Figures": len(self.figures),

            "Author": self.author

        }

    # =====================================================
    # Compact
    # =====================================================

    def compact(self):

        return {

            "report": self.report_name,

            "type": self.report_type,

            "pages": self.pages

        }

    # =====================================================
    # Display
    # =====================================================

    def __repr__(self):

        return (

            f"ReportResult("

            f"name='{self.report_name}', "

            f"type='{self.report_type}', "

            f"pages={self.pages}"

            f")"

        )