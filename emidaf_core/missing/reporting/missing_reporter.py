"""
=========================================================
EMIDAF Framework v1.0
Missing Data Reporter
---------------------------------------------------------
Reporting and export utilities for MissingPipelineResult.
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class MissingReporter:
    """
    Génère des rapports à partir d'un
    MissingPipelineResult.

    Formats supportés :
        - DataFrame
        - CSV
        - Excel
        - Markdown
        - HTML
    """

    def __init__(
        self,
        result: Any,
    ) -> None:

        self._validate_result(
            result
        )

        self.result = result

    # =====================================================
    # DATAFRAME
    # =====================================================

    def dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Retourne une copie de la table d'audit
        produite par MissingPipelineResult.
        """

        table = (
            self.result
            .summary_dataframe()
        )

        if not isinstance(
            table,
            pd.DataFrame,
        ):
            raise TypeError(
                "summary_dataframe() must return "
                "a pandas DataFrame."
            )

        return table.copy(
            deep=True
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Retourne une copie de la synthèse générale.
        """

        summary = (
            self.result
            .summary()
        )

        if not isinstance(
            summary,
            dict,
        ):
            raise TypeError(
                "summary() must return a dictionary."
            )

        return dict(
            summary
        )

    # =====================================================
    # CSV
    # =====================================================

    def to_csv(
        self,
        path: str | Path,
        *,
        index: bool = False,
        encoding: str = "utf-8",
    ) -> Path:
        """
        Exporte la table d'audit au format CSV.
        """

        output_path = (
            self._prepare_path(
                path=path,
                expected_suffix=".csv",
            )
        )

        self.dataframe().to_csv(
            output_path,
            index=index,
            encoding=encoding,
        )

        return output_path

    # =====================================================
    # EXCEL
    # =====================================================

    def to_excel(
        self,
        path: str | Path,
        *,
        index: bool = False,
    ) -> Path:
        """
        Exporte le rapport vers un fichier Excel.

        Feuilles :
            Summary
            Variables
        """

        output_path = (
            self._prepare_path(
                path=path,
                expected_suffix=".xlsx",
            )
        )

        summary_df = (
            self._summary_dataframe()
        )

        variables_df = (
            self.dataframe()
        )

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl",
        ) as writer:

            summary_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
            )

            variables_df.to_excel(
                writer,
                sheet_name="Variables",
                index=index,
            )

        return output_path

    # =====================================================
    # MARKDOWN
    # =====================================================

    def to_markdown(
        self,
        path: str | Path | None = None,
    ) -> str:
        """
        Produit une représentation Markdown.

        Si path est fourni, le rapport est également
        écrit dans un fichier .md.
        """

        summary = (
            self.summary()
        )

        table = (
            self.dataframe()
        )

        lines = [
            "# EMIDAF Missing Data Report",
            "",
            "## Summary",
            "",
        ]

        for key, value in (
            summary.items()
        ):
            lines.append(
                f"- **{key}**: {value}"
            )

        lines.extend(
            [
                "",
                "## Variables",
                "",
                table.to_markdown(
                    index=False
                ),
                "",
            ]
        )

        markdown = "\n".join(
            lines
        )

        if path is not None:

            output_path = (
                self._prepare_path(
                    path=path,
                    expected_suffix=".md",
                )
            )

            output_path.write_text(
                markdown,
                encoding="utf-8",
            )

        return markdown

    # =====================================================
    # HTML
    # =====================================================

    def to_html(
        self,
        path: str | Path | None = None,
    ) -> str:
        """
        Produit un rapport HTML autonome simple.
        """

        summary = (
            self.summary()
        )

        table = (
            self.dataframe()
        )

        summary_rows = "\n".join(
            (
                "<tr>"
                f"<th>{key}</th>"
                f"<td>{value}</td>"
                "</tr>"
            )
            for key, value
            in summary.items()
        )

        variables_html = (
            table.to_html(
                index=False,
                border=0,
            )
        )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>EMIDAF Missing Data Report</title>
</head>
<body>
    <h1>EMIDAF Missing Data Report</h1>

    <h2>Summary</h2>

    <table>
        {summary_rows}
    </table>

    <h2>Variables</h2>

    {variables_html}
</body>
</html>
"""

        if path is not None:

            output_path = (
                self._prepare_path(
                    path=path,
                    expected_suffix=".html",
                )
            )

            output_path.write_text(
                html,
                encoding="utf-8",
            )

        return html

    # =====================================================
    # MISSINGNESS MECHANISM
    # =====================================================

    def mechanism_summary(
        self,
    ) -> dict[str, Any]:
        """
        Retourne une synthèse structurée de l'évaluation
        MCAR / MAR / MNAR.

        Aucune conclusion plus forte que celle fournie par
        MissingAnalyzer n'est ajoutée.
        """

        report = getattr(
            self.result,
            "report",
            {},
        )

        if not isinstance(
            report,
            dict,
        ):
            return {
                "available": False,
                "overall": {},
                "mcar": {},
                "mar": {},
                "mnar": {},
            }

        mechanism = None

        for key in [
            "mechanism",
            "mechanisms",
            "missing_mechanism",
            "mechanism_analysis",
        ]:

            candidate = report.get(
                key
            )

            if isinstance(
                candidate,
                dict,
            ):
                mechanism = candidate
                break

        if mechanism is None:
            return {
                "available": False,
                "overall": {},
                "mcar": {},
                "mar": {},
                "mnar": {},
            }

        tests = mechanism.get(
            "tests",
            {},
        )

        if not isinstance(
            tests,
            dict,
        ):
            tests = {}

        mcar = tests.get(
            "mcar",
            {},
        )

        mar = tests.get(
            "mar",
            {},
        )

        mnar = tests.get(
            "mnar",
            {},
        )

        if not isinstance(mcar, dict):
            mcar = {}

        if not isinstance(mar, dict):
            mar = {}

        if not isinstance(mnar, dict):
            mnar = {}

        return {
            "available": True,

            "overall": {
                "status":
                    mechanism.get(
                        "status"
                    ),

                "candidate":
                    mechanism.get(
                        "candidate"
                    ),

                "detected":
                    mechanism.get(
                        "detected"
                    ),

                "confidence":
                    mechanism.get(
                        "confidence"
                    ),

                "statistic":
                    mechanism.get(
                        "statistic"
                    ),

                "pvalue":
                    mechanism.get(
                        "pvalue"
                    ),

                "test_name":
                    mechanism.get(
                        "test_name"
                    ),

                "explanation":
                    mechanism.get(
                        "explanation"
                    ),
            },

            "mcar": {
                "name":
                    mcar.get(
                        "name"
                    ),

                "available":
                    mcar.get(
                        "available"
                    ),

                "executed":
                    mcar.get(
                        "executed"
                    ),

                "statistic":
                    mcar.get(
                        "statistic"
                    ),

                "pvalue":
                    mcar.get(
                        "pvalue"
                    ),

                "degrees_of_freedom":
                    mcar.get(
                        "degrees_of_freedom"
                    ),

                "compatible_with_mcar":
                    mcar.get(
                        "compatible_with_mcar"
                    ),

                "message":
                    mcar.get(
                        "message"
                    ),
            },

            "mar": {
                "name":
                    mar.get(
                        "name"
                    ),

                "available":
                    mar.get(
                        "available"
                    ),

                "executed":
                    mar.get(
                        "executed"
                    ),

                "evidence_detected":
                    mar.get(
                        "evidence_detected"
                    ),

                "variables_tested":
                    mar.get(
                        "variables_tested"
                    ),

                "variables_with_evidence":
                    mar.get(
                        "variables_with_evidence"
                    ),

                "message":
                    mar.get(
                        "message"
                    ),
            },

            "mnar": {
                "name":
                    mnar.get(
                        "name"
                    ),

                "available":
                    mnar.get(
                        "available"
                    ),

                "executed":
                    mnar.get(
                        "executed"
                    ),

                "message":
                    mnar.get(
                        "message"
                    ),
            },
        }

    def mechanism_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Retourne une table lisible de l'évaluation
        des mécanismes MCAR, MAR et MNAR.
        """

        summary = (
            self.mechanism_summary()
        )

        columns = [
            "mechanism",
            "executed",
            "evidence",
            "statistic",
            "pvalue",
            "conclusion",
        ]

        if not summary.get(
            "available",
            False,
        ):
            return pd.DataFrame(
                columns=columns
            )

        mcar = summary.get(
            "mcar",
            {},
        )

        mar = summary.get(
            "mar",
            {},
        )

        mnar = summary.get(
            "mnar",
            {},
        )

        # -------------------------------------------------
        # MCAR
        # -------------------------------------------------

        mcar_executed = bool(
            mcar.get(
                "executed",
                False,
            )
        )

        mcar_compatible = (
            mcar.get(
                "compatible_with_mcar"
            )
        )

        if not mcar_executed:

            mcar_evidence = (
                "Not evaluated"
            )

            mcar_conclusion = (
                "MCAR was not evaluated."
            )

        elif mcar_compatible is True:

            mcar_evidence = (
                "Compatible"
            )

            mcar_conclusion = (
                "The data are compatible with MCAR "
                "under Little's test. This does not "
                "prove that the mechanism is MCAR."
            )

        elif mcar_compatible is False:

            mcar_evidence = (
                "Not compatible"
            )

            mcar_conclusion = (
                "Little's MCAR hypothesis is rejected. "
                "The observed data are not compatible "
                "with MCAR under this test."
            )

        else:

            mcar_evidence = (
                "Undetermined"
            )

            mcar_conclusion = (
                "The MCAR assessment is inconclusive."
            )

        # -------------------------------------------------
        # MAR
        # -------------------------------------------------

        mar_executed = bool(
            mar.get(
                "executed",
                False,
            )
        )

        mar_detected = (
            mar.get(
                "evidence_detected"
            )
        )

        if not mar_executed:

            mar_evidence = (
                "Not evaluated"
            )

            mar_conclusion = (
                "MAR-related observed-variable "
                "associations were not evaluated."
            )

        elif mar_detected is True:

            mar_evidence = (
                "Evidence detected"
            )

            mar_conclusion = (
                "Associations between missingness and "
                "observed variables were detected. "
                "This provides evidence compatible with "
                "MAR, but does not prove MAR."
            )

        else:

            mar_evidence = (
                "No evidence detected"
            )

            mar_conclusion = (
                "No observed-variable association "
                "evidence was detected. This does not "
                "establish MCAR and does not rule out "
                "MAR or MNAR."
            )

        # -------------------------------------------------
        # MNAR
        # -------------------------------------------------

        mnar_executed = bool(
            mnar.get(
                "executed",
                False,
            )
        )

        if mnar_executed:

            mnar_evidence = (
                "Risk assessment available"
            )

        else:

            mnar_evidence = (
                "Not confirmed"
            )

        mnar_conclusion = (
            "MNAR cannot generally be confirmed from "
            "observed data alone. Domain knowledge, "
            "external information or sensitivity "
            "analysis may be required."
        )

        rows = [
            {
                "mechanism":
                    "MCAR",

                "executed":
                    mcar_executed,

                "evidence":
                    mcar_evidence,

                "statistic":
                    mcar.get(
                        "statistic"
                    ),

                "pvalue":
                    mcar.get(
                        "pvalue"
                    ),

                "conclusion":
                    mcar_conclusion,
            },

            {
                "mechanism":
                    "MAR",

                "executed":
                    mar_executed,

                "evidence":
                    mar_evidence,

                "statistic":
                    None,

                "pvalue":
                    None,

                "conclusion":
                    mar_conclusion,
            },

            {
                "mechanism":
                    "MNAR",

                "executed":
                    mnar_executed,

                "evidence":
                    mnar_evidence,

                "statistic":
                    None,

                "pvalue":
                    None,

                "conclusion":
                    mnar_conclusion,
            },
        ]

        return pd.DataFrame(
            rows,
            columns=columns,
        )

    def _mechanism_markdown(
        self,
    ) -> str:
        """
        Produit la section Markdown structurée
        relative aux mécanismes de valeurs manquantes.
        """

        summary = (
            self.mechanism_summary()
        )

        if not summary.get(
            "available",
            False,
        ):
            return (
                "No explicit missingness-mechanism "
                "assessment was available. No conclusion "
                "regarding MCAR, MAR or MNAR should be "
                "inferred from the imputation strategy alone."
            )

        overall = summary.get(
            "overall",
            {},
        )

        table = (
            self.mechanism_dataframe()
        )

        lines = [
            "### Overall assessment",
            "",
            (
                f"- **Status:** "
                f"{overall.get('status')}"
            ),
            (
                f"- **Candidate mechanism:** "
                f"{overall.get('candidate')}"
            ),
            (
                f"- **Evidence detected:** "
                f"{overall.get('detected')}"
            ),
            (
                f"- **Confidence:** "
                f"{overall.get('confidence')}"
            ),
            (
                f"- **Statistic:** "
                f"{overall.get('statistic')}"
            ),
            (
                f"- **p-value:** "
                f"{self._format_pvalue(overall.get('pvalue'))}"
            ),
            "",
        ]

        explanation = overall.get(
            "explanation"
        )

        if explanation:

            lines.extend(
                [
                    "### Interpretation",
                    "",
                    str(
                        explanation
                    ),
                    "",
                ]
            )

        lines.extend(
            [
                "### MCAR / MAR / MNAR assessment",
                "",
                table.to_markdown(
                    index=False
                ),
            ]
        )

        return "\n".join(
            lines
        )

    def _mechanism_html(
        self,
    ) -> str:
        """
        Produit la section HTML structurée relative
        aux mécanismes de valeurs manquantes.
        """

        summary = (
            self.mechanism_summary()
        )

        if not summary.get(
            "available",
            False,
        ):
            return (
                "<p>No explicit missingness-mechanism "
                "assessment was available. No conclusion "
                "regarding MCAR, MAR or MNAR should be "
                "inferred from the imputation strategy "
                "alone.</p>"
            )

        overall = summary.get(
            "overall",
            {},
        )

        table = (
            self.mechanism_dataframe()
        )

        explanation = (
            overall.get(
                "explanation"
            )
            or
            "No additional interpretation was provided."
        )

        return f"""
<h3>Overall assessment</h3>

<ul>
    <li><strong>Status:</strong> {overall.get('status')}</li>
    <li><strong>Candidate mechanism:</strong> {overall.get('candidate')}</li>
    <li><strong>Evidence detected:</strong> {overall.get('detected')}</li>
    <li><strong>Confidence:</strong> {overall.get('confidence')}</li>
    <li><strong>Statistic:</strong> {overall.get('statistic')}</li>
    <li><strong>p-value:</strong> {self._format_pvalue(overall.get('pvalue'))}</li>
</ul>

<h3>Interpretation</h3>

<p>{explanation}</p>

<h3>MCAR / MAR / MNAR assessment</h3>

{table.to_html(index=False, border=0)}
"""

    @staticmethod
    def _format_pvalue(
        value: Any,
    ) -> str:
        """
        Formate une p-value pour le reporting.
        """

        if value is None:
            return "N/A"

        try:
            pvalue = float(
                value
            )
        except (
            TypeError,
            ValueError,
        ):
            return str(
                value
            )

        if pvalue < 0.001:
            return "< 0.001"

        return f"{pvalue:.4f}"

    # =====================================================
    # SCIENTIFIC REPORTING
    # =====================================================

    def to_scientific_markdown(
        self,
        path: str | Path | None = None,
    ) -> str:
        """
        Produit un rapport scientifique structuré
        sur l'analyse et le traitement des valeurs
        manquantes.

        Le rapport conserve une formulation prudente
        concernant les mécanismes MCAR, MAR et MNAR.
        """

        summary = self.summary()

        table = self.dataframe()

        report = getattr(
            self.result,
            "report",
            {},
        )

        mechanism_text = (
            self._mechanism_markdown()
        )

        methodological_notes = (
            self._methodological_notes(
                table
            )
        )

        review_required = summary.get(
            "review_required",
            [],
        )

        lines = [
            "# EMIDAF Scientific Missing-Data Report",
            "",
            "## 1. Executive summary",
            "",
            (
                f"- **Rows:** "
                f"{summary.get('rows', 0)}"
            ),
            (
                f"- **Columns:** "
                f"{summary.get('columns', 0)}"
            ),
            (
                f"- **Initial missing values:** "
                f"{summary.get('initial_missing_values', 0)}"
            ),
            (
                f"- **Final missing values:** "
                f"{summary.get('final_missing_values', 0)}"
            ),
            (
                f"- **Values imputed:** "
                f"{summary.get('total_values_imputed', 0)}"
            ),
            (
                f"- **Missing-value reduction:** "
                f"{summary.get('missing_values_reduction', 0)}"
            ),
            (
                f"- **Imputation applied:** "
                f"{summary.get('imputation_applied', False)}"
            ),
            (
                f"- **Pipeline success:** "
                f"{summary.get('success', False)}"
            ),
            "",
            "## 2. Missing-data diagnosis",
            "",
        ]

        if table.empty:

            lines.extend(
                [
                    (
                        "No variable-level imputation "
                        "decision was available."
                    ),
                    "",
                ]
            )

        else:

            lines.extend(
                [
                    table.to_markdown(
                        index=False
                    ),
                    "",
                ]
            )

        lines.extend(
            [
                "## 3. Missingness mechanism assessment",
                "",
                mechanism_text,
                "",
                "## 4. Imputation decisions",
                "",
            ]
        )

        if table.empty:

            lines.extend(
                [
                    "No imputation decision was generated.",
                    "",
                ]
            )

        else:

            for _, row in table.iterrows():

                column = row[
                    "column"
                ]

                strategy = row[
                    "strategy"
                ]

                missing_rate = row[
                    "missing_rate"
                ]

                predictors = row[
                    "predictors"
                ]

                applicable = row[
                    "applicable"
                ]

                parameters = row[
                    "parameters"
                ]

                lines.append(
                    f"### {column}"
                )

                lines.append(
                    ""
                )

                lines.append(
                    f"- Missing rate: "
                    f"{missing_rate}%"
                )

                lines.append(
                    f"- Strategy: "
                    f"{strategy}"
                )

                lines.append(
                    f"- Automatically applicable: "
                    f"{applicable}"
                )

                lines.append(
                    f"- Predictors: "
                    f"{predictors}"
                )

                lines.append(
                    f"- Parameters: "
                    f"{parameters}"
                )

                lines.append(
                    ""
                )

        lines.extend(
            [
                "## 5. Variables requiring manual review",
                "",
            ]
        )

        if review_required:

            for column in (
                review_required
            ):
                lines.append(
                    f"- {column}"
                )

        else:

            lines.append(
                "No variable currently requires "
                "manual review."
            )

        lines.extend(
            [
                "",
                "## 6. Methodological cautions",
                "",
            ]
        )

        for note in methodological_notes:
            lines.append(
                f"- {note}"
            )

        lines.extend(
            [
                "",
                "## 7. Reproducibility information",
                "",
                (
                    "- Generated by: "
                    "EMIDAF MissingReporter"
                ),
                (
                    "- Analysis source: "
                    "MissingPipelineResult"
                ),
                (
                    "- Variable-level decisions are "
                    "derived from ImputationPlan."
                ),
                (
                    "- Automatic imputation and manual "
                    "review decisions remain auditable."
                ),
                "",
            ]
        )

        markdown = "\n".join(
            lines
        )

        if path is not None:

            output_path = (
                self._prepare_path(
                    path=path,
                    expected_suffix=".md",
                )
            )

            output_path.write_text(
                markdown,
                encoding="utf-8",
            )

        return markdown

    def to_scientific_html(
        self,
        path: str | Path | None = None,
    ) -> str:
        """
        Produit une version HTML autonome du
        rapport scientifique.
        """

        summary = self.summary()

        table = self.dataframe()

        report = getattr(
            self.result,
            "report",
            {},
        )

        mechanism_text = (
            self._mechanism_html()
        )

        methodological_notes = (
            self._methodological_notes(
                table
            )
        )

        review_required = summary.get(
            "review_required",
            [],
        )

        summary_rows = "\n".join(
            (
                "<tr>"
                f"<th>{key}</th>"
                f"<td>{value}</td>"
                "</tr>"
            )
            for key, value
            in summary.items()
        )

        if table.empty:
            variable_table = (
                "<p>No variable-level decision "
                "was available.</p>"
            )
        else:
            variable_table = (
                table.to_html(
                    index=False,
                    border=0,
                )
            )

        if review_required:
            review_html = (
                "<ul>"
                + "".join(
                    f"<li>{column}</li>"
                    for column
                    in review_required
                )
                + "</ul>"
            )
        else:
            review_html = (
                "<p>No variable currently requires "
                "manual review.</p>"
            )

        notes_html = (
            "<ul>"
            + "".join(
                f"<li>{note}</li>"
                for note
                in methodological_notes
            )
            + "</ul>"
        )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>EMIDAF Scientific Missing-Data Report</title>
</head>
<body>

<h1>EMIDAF Scientific Missing-Data Report</h1>

<h2>1. Executive summary</h2>

<table>
{summary_rows}
</table>

<h2>2. Missing-data diagnosis</h2>

{variable_table}

<h2>3. Missingness mechanism assessment</h2>

{mechanism_text}

<h2>4. Imputation decisions</h2>

{variable_table}

<h2>5. Variables requiring manual review</h2>

{review_html}

<h2>6. Methodological cautions</h2>

{notes_html}

<h2>7. Reproducibility information</h2>

<ul>
    <li>Generated by EMIDAF MissingReporter.</li>
    <li>Analysis source: MissingPipelineResult.</li>
    <li>Variable-level decisions are derived from ImputationPlan.</li>
    <li>Automatic and manual decisions remain auditable.</li>
</ul>

</body>
</html>
"""

        if path is not None:

            output_path = (
                self._prepare_path(
                    path=path,
                    expected_suffix=".html",
                )
            )

            output_path.write_text(
                html,
                encoding="utf-8",
            )

        return html

    # =====================================================
    # SCIENTIFIC INTERPRETATION HELPERS
    # =====================================================

    @staticmethod
    def _scientific_mechanism_text(
        report: Any,
    ) -> str:
        """
        Produit une formulation prudente concernant
        les mécanismes de valeurs manquantes.
        """

        if not isinstance(
            report,
            dict,
        ):
            return (
                "No structured missingness-mechanism "
                "assessment was available."
            )

        possible_keys = [
            "mechanism",
            "mechanisms",
            "missing_mechanism",
            "mechanism_analysis",
        ]

        mechanism_data = None

        for key in possible_keys:

            if key in report:

                mechanism_data = (
                    report[
                        key
                    ]
                )

                break

        if mechanism_data is None:

            return (
                "No explicit missingness-mechanism "
                "assessment was available in the report. "
                "No conclusion regarding MCAR, MAR or MNAR "
                "should therefore be inferred from the "
                "imputation strategy alone."
            )

        return (
            "The MissingAnalyzer produced the following "
            "mechanism-related information: "
            f"{mechanism_data}. "
            "This information must be interpreted as "
            "diagnostic evidence rather than definitive "
            "proof of the missingness mechanism."
        )

    @staticmethod
    def _methodological_notes(
        table: pd.DataFrame,
    ) -> list[str]:
        """
        Génère les précautions méthodologiques
        adaptées aux stratégies présentes.
        """

        notes = [
            (
                "Failure to reject an MCAR hypothesis "
                "does not prove that the data are MCAR."
            ),
            (
                "MAR is an assumption supported by "
                "observed-data relationships and cannot "
                "generally be proven from observed data alone."
            ),
            (
                "MNAR cannot generally be confirmed from "
                "observed data alone and may require domain "
                "knowledge or sensitivity analysis."
            ),
        ]

        if (
            table.empty
            or "strategy"
            not in table.columns
        ):
            return notes

        strategies = set(
            table[
                "strategy"
            ].astype(
                str
            )
        )

        if (
            "MEAN" in strategies
            or "MODE" in strategies
        ):
            notes.append(
                "Simple imputation may reduce variability "
                "and may distort relationships between "
                "variables."
            )

        if "KNN" in strategies:
            notes.append(
                "KNN imputation depends on the selected "
                "predictors, distance structure and variable "
                "scales."
            )

        if "MICE" in strategies:
            notes.append(
                "The current EMIDAF MICE implementation is "
                "an iterative MICE-like imputation procedure; "
                "it is not equivalent to a full multiple-"
                "imputation analysis with Rubin's rules."
            )

        if "REVIEW" in strategies:
            notes.append(
                "Variables marked REVIEW are intentionally "
                "not automatically imputed and require "
                "methodological or domain-specific assessment."
            )

        return notes

    # =====================================================
    # SCIENTIFIC EXCEL
    # =====================================================

    def to_scientific_excel(
        self,
        path: str | Path,
        *,
        index: bool = False,
    ) -> Path:
        """
        Exporte un rapport scientifique complet vers Excel.

        Feuilles
        --------
        Summary:
            Synthèse générale du pipeline.

        Mechanisms:
            Évaluation structurée MCAR / MAR / MNAR.

        Variables:
            Décisions d'imputation par variable.

        Review:
            Variables nécessitant une revue manuelle.

        Methodological Notes:
            Précautions méthodologiques liées aux
            mécanismes et stratégies utilisées.
        """

        output_path = (
            self._prepare_path(
                path=path,
                expected_suffix=".xlsx",
            )
        )

        summary_df = (
            self._summary_dataframe()
        )

        mechanisms_df = (
            self.mechanism_dataframe()
        )

        variables_df = (
            self.dataframe()
        )

        review_df = (
            self._review_dataframe()
        )

        notes_df = (
            self._methodological_notes_dataframe()
        )

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl",
        ) as writer:

            summary_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
            )

            mechanisms_df.to_excel(
                writer,
                sheet_name="Mechanisms",
                index=False,
            )

            variables_df.to_excel(
                writer,
                sheet_name="Variables",
                index=index,
            )

            review_df.to_excel(
                writer,
                sheet_name="Review",
                index=False,
            )

            notes_df.to_excel(
                writer,
                sheet_name="Methodological Notes",
                index=False,
            )

        return output_path

    def _review_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Retourne les variables nécessitant une
        revue manuelle.
        """

        table = (
            self.dataframe()
        )

        columns = [
            "column",
            "missing_rate",
            "strategy",
            "predictors",
            "applicable",
            "review_required",
            "parameters",
        ]

        if (
            table.empty
            or "review_required"
            not in table.columns
        ):
            return pd.DataFrame(
                columns=columns
            )

        review_table = table[
            table[
                "review_required"
            ].astype(
                bool
            )
        ].copy()

        return review_table.reset_index(
            drop=True
        )

    def _methodological_notes_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Retourne les précautions méthodologiques
        sous forme tabulaire.
        """

        notes = (
            self._methodological_notes(
                self.dataframe()
            )
        )

        return pd.DataFrame(
            [
                {
                    "note_id":
                        index + 1,

                    "methodological_note":
                        note,
                }
                for index, note
                in enumerate(
                    notes
                )
            ]
        )

    # =====================================================
    # INTERNAL SUMMARY DATAFRAME
    # =====================================================

    def _summary_dataframe(
        self,
    ) -> pd.DataFrame:
        """
        Convertit la synthèse générale en table
        clé / valeur.
        """

        summary = (
            self.summary()
        )

        return pd.DataFrame(
            [
                {
                    "metric": key,
                    "value": value,
                }
                for key, value
                in summary.items()
            ]
        )

    # =====================================================
    # PATH HANDLING
    # =====================================================

    @staticmethod
    def _prepare_path(
        path: str | Path,
        expected_suffix: str,
    ) -> Path:

        if not isinstance(
            path,
            (
                str,
                Path,
            ),
        ):
            raise TypeError(
                "path must be a string or Path."
            )

        output_path = Path(
            path
        )

        if (
            output_path.suffix.lower()
            != expected_suffix
        ):
            output_path = (
                output_path
                .with_suffix(
                    expected_suffix
                )
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return output_path

    # =====================================================
    # VALIDATION
    # =====================================================

    @staticmethod
    def _validate_result(
        result: Any,
    ) -> None:

        required_methods = [
            "summary",
            "summary_dataframe",
        ]

        for method_name in (
            required_methods
        ):

            method = getattr(
                result,
                method_name,
                None,
            )

            if not callable(
                method
            ):
                raise TypeError(
                    "result must expose callable "
                    f"'{method_name}()'."
                )
