"""
=========================================================
EMIDAF Framework
Reporting - Report Builder
=========================================================
"""

from __future__ import annotations

from typing import Any

from emidaf_core.common.results.report_result import ReportResult

from .section import ReportSection


class ReportBuilder:
    """
    Construction structurée d'un rapport global EMIDAF.
    """

    def __init__(
        self,
        *,
        title: str = "Rapport d'analyse EMIDAF",
        subtitle: str = "",
        summary: str = "",
        author: str = "Abdoulaye Wakhab DIOP",
        organization: str = "",
        language: str = "fr",
    ):
        self.title = title
        self.subtitle = subtitle
        self.summary = summary
        self.author = author
        self.organization = organization
        self.language = language

        self._sections: list[ReportSection] = []

    @property
    def sections(self) -> list[ReportSection]:
        return list(self._sections)

    def add_section(
        self,
        title: str,
        data: Any = None,
        *,
        interpretation: str = "",
        limitations: list[str] | None = None,
        category: str = "analysis",
    ) -> "ReportBuilder":

        section = ReportSection(
            title=title,
            data=data,
            interpretation=interpretation,
            limitations=limitations or [],
            category=category,
        )

        self._sections.append(section)

        return self

    def build(self) -> ReportResult:
        """
        Construit un ReportResult sans effectuer d'export.
        """

        structured_sections = [
            section.to_dict()
            for section in self._sections
        ]

        text_parts = [
            self.title,
            self.subtitle,
            self.summary,
        ]

        for section in structured_sections:
            text_parts.append(section["title"])
            text_parts.append(str(section.get("data", "")))
            text_parts.append(
                section.get("interpretation", "")
            )
            text_parts.extend(
                section.get("limitations", [])
            )

        words = len(
            " ".join(text_parts).split()
        )

        report = ReportResult(
            report_name=self.title,
            report_type="EMIDAF Global Analysis",
            author=self.author,
            organization=self.organization,
            language=self.language,
            title=self.title,
            subtitle=self.subtitle,
            summary=self.summary,
            sections=[
                section.title
                for section in self._sections
            ],
            words=words,
        )

        report.metadata[
            "structured_sections"
        ] = structured_sections

        report.statistics[
            "sections_count"
        ] = len(self._sections)

        return report
