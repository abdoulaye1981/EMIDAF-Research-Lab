"""
=========================================================
EMIDAF Framework
Reporting - Exporter
=========================================================
"""

from __future__ import annotations

import re
from pathlib import Path

from emidaf_core.common.results.report_result import ReportResult

from .renderer import ReportRenderer


class ReportExporter:

    @staticmethod
    def _slug(text: str) -> str:
        value = text.strip().lower()

        value = re.sub(
            r"[^a-z0-9_-]+",
            "_",
            value,
        )

        return (
            value.strip("_")
            or "rapport_emidaf"
        )

    @classmethod
    def export(
        cls,
        report: ReportResult,
        output_directory: str | Path,
        *,
        formats: tuple[str, ...] = (
            "markdown",
            "html",
            "json",
        ),
    ) -> ReportResult:

        directory = Path(
            output_directory
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        basename = cls._slug(
            report.report_name
            or report.title
        )

        report.output_directory = str(
            directory
        )

        for format_name in formats:

            normalized = (
                format_name
                .strip()
                .lower()
            )

            if normalized in {
                "markdown",
                "md",
            }:
                path = directory / (
                    f"{basename}.md"
                )

                path.write_text(
                    ReportRenderer.markdown(
                        report
                    ),
                    encoding="utf-8",
                )

                report.markdown_file = str(
                    path
                )

            elif normalized == "html":

                path = directory / (
                    f"{basename}.html"
                )

                path.write_text(
                    ReportRenderer.html(
                        report
                    ),
                    encoding="utf-8",
                )

                report.html_file = str(
                    path
                )

            elif normalized == "json":

                path = directory / (
                    f"{basename}.json"
                )

                path.write_text(
                    ReportRenderer.json(
                        report
                    ),
                    encoding="utf-8",
                )

                report.json_file = str(
                    path
                )

            else:
                raise ValueError(
                    "Format de rapport non pris "
                    f"en charge : {format_name}"
                )

        return report
