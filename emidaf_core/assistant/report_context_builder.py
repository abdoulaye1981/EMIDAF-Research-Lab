from __future__ import annotations

from typing import Any

from emidaf_core.common.results.report_result import (
    ReportResult,
)

from .context_builder import ContextBuilder


class ReportContextBuilder:

    @classmethod
    def build(
        cls,
        report: ReportResult,
        analyses: dict[str, Any],
    ) -> dict[str, Any]:

        if not isinstance(report, ReportResult):
            raise TypeError(
                "report doit être un ReportResult."
            )

        structured_sections = report.metadata.get(
            "structured_sections",
            [],
        )

        return {
            "report": {
                "title": report.title,
                "subtitle": report.subtitle,
                "summary": report.summary,
                "author": report.author,
                "organization": report.organization,
                "language": report.language,
                "sections": ContextBuilder._sanitize(
                    structured_sections
                ),
                "statistics": ContextBuilder._sanitize(
                    report.statistics
                ),
            },
            "analyses": ContextBuilder.build(
                analyses
            ),
        }
