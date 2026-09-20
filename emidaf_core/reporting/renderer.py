"""
=========================================================
EMIDAF Framework
Reporting - Professional Renderers
=========================================================
"""

from __future__ import annotations

from datetime import datetime
import html
import json
import math
import re
from typing import Any

from emidaf_core.common.results.report_result import (
    ReportResult,
)


# =========================================================
# SERIALIZATION
# =========================================================

def _json_default(value: Any):
    """
    Sérialisation tolérante pour numpy, pandas
    et objets scientifiques simples.
    """

    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass

    if hasattr(value, "tolist"):
        try:
            return value.tolist()
        except Exception:
            pass

    if hasattr(value, "to_dict"):
        try:
            return value.to_dict()
        except Exception:
            pass

    return str(value)


def _normalize(value: Any) -> Any:
    """
    Convertit les objets scientifiques en structures
    Python simples exploitables par les renderers.
    """

    if value is None:
        return None

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ):
        return value

    # pandas DataFrame
    if hasattr(value, "to_dict"):
        try:
            records = value.to_dict(
                orient="records"
            )
            if isinstance(records, list):
                return [
                    _normalize(item)
                    for item in records
                ]
        except TypeError:
            pass
        except Exception:
            pass

        try:
            return _normalize(
                value.to_dict()
            )
        except Exception:
            pass

    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass

    if hasattr(value, "tolist"):
        try:
            return _normalize(
                value.tolist()
            )
        except Exception:
            pass

    if isinstance(value, dict):
        return {
            str(key): _normalize(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
            set,
        ),
    ):
        return [
            _normalize(item)
            for item in value
        ]

    return str(value)


def _pretty(value: Any) -> str:

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        default=_json_default,
    )


# =========================================================
# LABELS / FORMATTING
# =========================================================

_LABELS = {
    "rows": "Observations",
    "columns": "Variables",
    "cells": "Cellules",
    "missing": "Valeurs manquantes",
    "duplicates": "Doublons",
    "rows_before": "Observations avant",
    "rows_after": "Observations après",
    "columns_before": "Variables avant",
    "columns_after": "Variables après",
    "before_metrics": "Situation avant traitement",
    "after_metrics": "Situation après traitement",
    "operations": "Transformations appliquées",
    "comparison": "Comparaison avant / après",
    "transformations": "Transformations appliquées",
    "synthese_traitement": "Synthèse du prétraitement",
    "performance": "Performances prédictives",
    "importance_native": "Importance native",
    "importance_permutation": "Importance par permutation",
    "interpretation": "Interprétation",
    "converted_columns": "Types corrigés automatiquement",
    "project_id": "Identifiant du projet",
    "project_name": "Projet",
    "dataset_id": "Identifiant du jeu de données",
    "dataset_name": "Jeu de données",
    "observations": "Observations",
    "variables": "Variables",
    "shape": "Dimensions",
    "missing_values_total": "Valeurs manquantes",
    "duplicate_rows": "Lignes dupliquées",
    "data_types": "Types des variables",
    "model": "Modèle",
    "model_name": "Modèle",
    "task": "Type de problème",
    "target": "Variable cible",
    "features": "Variables explicatives",
    "cv_mean": "Score moyen en validation croisée",
    "cv_std": "Écart-type en validation croisée",
    "test_score": "Score sur le jeu de test",
    "threshold": "Seuil décisionnel",
    "direction": "Direction du scénario",
    "summary": "Synthèse",
    "native_interpretation": "Interprétation de l'importance native",
    "permutation_interpretation": (
        "Interprétation de l'importance par permutation"
    ),
    "predictive_warning": "Avertissement prédictif",
    "status": "Statut",
    "imputation": "Imputation",
    "outliers": "Valeurs aberrantes",
    "encoding": "Encodage",
    "scaling": "Mise à l'échelle",
}


def _humanize_key(key: Any) -> str:

    key = str(key)

    if key in _LABELS:
        return _LABELS[key]

    text = key.replace("_", " ")
    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    if not text:
        return ""

    return (
        text[0].upper()
        + text[1:]
    )


def _format_number(value: float) -> str:

    if math.isnan(value):
        return "—"

    if math.isinf(value):
        return "∞" if value > 0 else "−∞"

    if value.is_integer():
        return f"{int(value):,}".replace(
            ",",
            " ",
        )

    absolute = abs(value)

    if absolute >= 100:
        formatted = f"{value:,.2f}"

    elif absolute >= 1:
        formatted = f"{value:.4f}"

    else:
        formatted = f"{value:.6f}"

    return (
        formatted
        .replace(",", " ")
    )


def _format_scalar(value: Any) -> str:

    if value is None:
        return "—"

    if isinstance(value, bool):
        return (
            "Oui"
            if value
            else "Non"
        )

    if isinstance(value, float):
        return _format_number(value)

    if isinstance(value, int):
        return f"{value:,}".replace(
            ",",
            " ",
        )

    value = str(value)

    translations = {
        "regression": "Régression",
        "classification": "Classification",
        "none": "Aucune",
        "standard": "Standardisation",
        "minmax": "Normalisation Min-Max",
        "remove_iqr": "Suppression par méthode IQR",
        "winsorize": "Winsorisation",
        "non_disponible": "Non disponible",
        "above": "Au-dessus du seuil",
        "below": "En dessous du seuil",
        "ridge": "Ridge",
        "lasso": "Lasso",
        "linear_regression": "Régression linéaire",
        "logistic_regression": "Régression logistique",
        "random_forest": "Forêt aléatoire",
        "svr": "SVR",
        "svc": "SVC",
    }

    return translations.get(
        value.lower(),
        value,
    )


# =========================================================
# HTML COMPONENTS
# =========================================================

def _render_scalar(value: Any) -> str:

    formatted = _format_scalar(value)

    return (
        '<span class="value">'
        + html.escape(formatted)
        + "</span>"
    )


def _render_simple_dict(data: dict) -> str:

    rows = []

    for key, value in data.items():

        rows.append(
            "<tr>"
            f"<th>{html.escape(_humanize_key(key))}</th>"
            f"<td>{_render_scalar(value)}</td>"
            "</tr>"
        )

    return (
        '<div class="table-wrapper">'
        '<table class="data-table">'
        "<tbody>"
        + "".join(rows)
        + "</tbody>"
        "</table>"
        "</div>"
    )


def _render_record_table(records: list[dict]) -> str:

    if not records:
        return (
            '<p class="empty-value">'
            "Aucun résultat disponible."
            "</p>"
        )

    keys = []

    for record in records:
        for key in record:
            if key not in keys:
                keys.append(key)

    head = "".join(
        "<th>"
        + html.escape(
            _humanize_key(key)
        )
        + "</th>"
        for key in keys
    )

    body = []

    for record in records:

        cells = []

        for key in keys:

            value = record.get(key)

            if isinstance(
                value,
                (
                    dict,
                    list,
                    tuple,
                ),
            ):
                rendered = _render_value(
                    value
                )
            else:
                rendered = _render_scalar(
                    value
                )

            cells.append(
                f"<td>{rendered}</td>"
            )

        body.append(
            "<tr>"
            + "".join(cells)
            + "</tr>"
        )

    return (
        '<div class="table-wrapper">'
        '<table class="data-table">'
        "<thead>"
        f"<tr>{head}</tr>"
        "</thead>"
        "<tbody>"
        + "".join(body)
        + "</tbody>"
        "</table>"
        "</div>"
    )


def _render_list(values: list) -> str:

    if not values:
        return (
            '<p class="empty-value">'
            "Aucune donnée."
            "</p>"
        )

    if all(
        isinstance(item, dict)
        for item in values
    ):
        return _render_record_table(
            values
        )

    items = []

    for item in values:

        if isinstance(
            item,
            (
                dict,
                list,
                tuple,
            ),
        ):
            rendered = _render_value(
                item
            )
        else:
            rendered = _render_scalar(
                item
            )

        items.append(
            f"<li>{rendered}</li>"
        )

    return (
        '<ul class="clean-list">'
        + "".join(items)
        + "</ul>"
    )


def _render_dict(data: dict) -> str:

    if not data:
        return (
            '<p class="empty-value">'
            "Aucun résultat."
            "</p>"
        )

    # Statut particulier
    if (
        data.get("status")
        == "non_disponible"
    ):
        message = data.get(
            "message",
            "Résultat non disponible.",
        )

        return (
            '<div class="status-box unavailable">'
            '<span class="status-badge">'
            "Non disponible"
            "</span>"
            f"<p>{html.escape(str(message))}</p>"
            "</div>"
        )

    scalar_items = {}
    complex_items = {}

    for key, value in data.items():

        if isinstance(
            value,
            (
                dict,
                list,
                tuple,
            ),
        ):
            complex_items[key] = value
        else:
            scalar_items[key] = value

    blocks = []

    if scalar_items:
        blocks.append(
            _render_simple_dict(
                scalar_items
            )
        )

    for key, value in complex_items.items():

        blocks.append(
            '<div class="nested-block">'
            '<h4>'
            + html.escape(
                _humanize_key(key)
            )
            + "</h4>"
            + _render_value(value)
            + "</div>"
        )

    return "".join(blocks)


def _render_value(value: Any) -> str:

    value = _normalize(value)

    if value is None:
        return (
            '<p class="empty-value">'
            "Non renseigné."
            "</p>"
        )

    if isinstance(value, dict):
        return _render_dict(value)

    if isinstance(value, list):
        return _render_list(value)

    return _render_scalar(value)


def _render_interpretation(
    interpretation: str,
) -> str:

    if not interpretation:
        return ""

    return f"""
    <div class="insight-box interpretation-box">
        <div class="insight-title">
            Interprétation
        </div>
        <p>
            {html.escape(interpretation)}
        </p>
    </div>
    """


def _render_limitations(
    limitations: list[str],
) -> str:

    if not limitations:
        return ""

    items = "".join(
        "<li>"
        + html.escape(str(item))
        + "</li>"
        for item in limitations
    )

    return f"""
    <div class="insight-box limitation-box">
        <div class="insight-title">
            Limites méthodologiques
        </div>
        <ul>
            {items}
        </ul>
    </div>
    """


def _extract_project_data(
    sections: list[dict],
) -> dict:

    for section in sections:

        if (
            section.get("category")
            == "project"
        ):
            data = section.get(
                "data"
            )

            if isinstance(data, dict):
                return data

        title = str(
            section.get(
                "title",
                "",
            )
        ).lower()

        if "projet" in title:

            data = section.get(
                "data"
            )

            if isinstance(data, dict):
                return data

    return {}


def _extract_inspection_data(
    sections: list[dict],
) -> dict:

    for section in sections:

        title = str(
            section.get(
                "title",
                "",
            )
        ).lower()

        if "inspection" in title:

            data = section.get(
                "data"
            )

            if isinstance(data, dict):
                return data

    return {}


def _kpi_card(
    value: Any,
    label: str,
) -> str:

    return f"""
    <div class="kpi-card">
        <div class="kpi-value">
            {html.escape(_format_scalar(value))}
        </div>
        <div class="kpi-label">
            {html.escape(label)}
        </div>
    </div>
    """


# =========================================================
# RENDERER
# =========================================================

class ReportRenderer:

    # =====================================================
    # MARKDOWN
    # =====================================================

    @staticmethod
    def markdown(
        report: ReportResult,
    ) -> str:

        lines = [
            f"# {report.title}",
            "",
        ]

        if report.subtitle:
            lines.extend(
                [
                    f"## {report.subtitle}",
                    "",
                ]
            )

        if report.summary:
            lines.extend(
                [
                    report.summary,
                    "",
                ]
            )

        sections = report.metadata.get(
            "structured_sections",
            [],
        )

        for index, section in enumerate(
            sections,
            start=1,
        ):

            lines.extend(
                [
                    (
                        f"## {index}. "
                        f"{section['title']}"
                    ),
                    "",
                ]
            )

            data = section.get(
                "data"
            )

            if data is not None:

                lines.extend(
                    [
                        "### Résultats",
                        "",
                        "```text",
                        _pretty(
                            _normalize(data)
                        ),
                        "```",
                        "",
                    ]
                )

            interpretation = section.get(
                "interpretation",
                "",
            )

            if interpretation:

                lines.extend(
                    [
                        "### Interprétation",
                        "",
                        interpretation,
                        "",
                    ]
                )

            limitations = section.get(
                "limitations",
                [],
            )

            if limitations:

                lines.extend(
                    [
                        "### Limites méthodologiques",
                        "",
                    ]
                )

                for limitation in limitations:

                    lines.append(
                        f"- {limitation}"
                    )

                lines.append("")

        return "\n".join(lines)

    # =====================================================
    # HTML
    # =====================================================

    @staticmethod
    def html(
        report: ReportResult,
    ) -> str:

        sections = report.metadata.get(
            "structured_sections",
            [],
        )

        project_data = _extract_project_data(
            sections
        )

        inspection_data = (
            _extract_inspection_data(
                sections
            )
        )

        project_name = (
            project_data.get(
                "project_name"
            )
            or "Projet EMIDAF"
        )

        dataset_name = (
            project_data.get(
                "dataset_name"
            )
            or "Jeu de données"
        )

        observations = (
            project_data.get(
                "observations"
            )
            or inspection_data.get(
                "shape",
                {},
            ).get(
                "rows"
            )
            or "—"
        )

        variables = (
            project_data.get(
                "variables"
            )
            or inspection_data.get(
                "shape",
                {},
            ).get(
                "columns"
            )
            or "—"
        )

        missing = inspection_data.get(
            "missing_values_total",
            "—",
        )

        duplicates = inspection_data.get(
            "duplicate_rows",
            "—",
        )

        generated_at = datetime.now().strftime(
            "%d/%m/%Y à %H:%M"
        )

        organization = (
            report.organization
            or "EMIDAF Research Lab"
        )

        author = (
            report.author
            or "EMIDAF"
        )

        sections_html = []

        for index, section in enumerate(
            sections,
            start=1,
        ):

            title = html.escape(
                section.get(
                    "title",
                    f"Section {index}",
                )
            )

            data = section.get(
                "data"
            )

            result_html = ""

            if data is not None:
                result_html = (
                    '<div class="section-results">'
                    '<h3>Résultats</h3>'
                    + _render_value(data)
                    + "</div>"
                )

            interpretation_html = (
                _render_interpretation(
                    section.get(
                        "interpretation",
                        "",
                    )
                )
            )

            limitation_html = (
                _render_limitations(
                    section.get(
                        "limitations",
                        [],
                    )
                )
            )

            sections_html.append(
                f"""
                <section class="report-section">
                    <div class="section-heading">
                        <div class="section-number">
                            {index:02d}
                        </div>

                        <div>
                            <div class="section-kicker">
                                ANALYSE EMIDAF
                            </div>
                            <h2>{title}</h2>
                        </div>
                    </div>

                    {result_html}

                    {interpretation_html}

                    {limitation_html}
                </section>
                """
            )

        return f"""<!DOCTYPE html>
<html lang="{html.escape(report.language or 'fr')}">

<head>
<meta charset="utf-8">
<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<title>{html.escape(report.title)}</title>

<style>

:root {{
    --emidaf-blue: #173f6d;
    --emidaf-blue-dark: #102f52;
    --emidaf-blue-light: #edf5fb;
    --emidaf-accent: #3b82b7;

    --text-primary: #1f2937;
    --text-secondary: #5f6b7a;

    --border: #dce3ea;
    --surface: #ffffff;
    --surface-soft: #f6f8fb;

    --success: #237a57;
    --success-bg: #eaf7f0;

    --warning: #946200;
    --warning-bg: #fff7df;

    --shadow:
        0 8px 24px rgba(15, 42, 70, 0.08);
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    background: #eef2f6;
    color: var(--text-primary);
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;
    line-height: 1.65;
}}

.report-container {{
    max-width: 1080px;
    margin: 32px auto;
    background: var(--surface);
    box-shadow: var(--shadow);
}}

.cover {{
    min-height: 620px;
    padding: 74px 72px;
    background:
        linear-gradient(
            135deg,
            var(--emidaf-blue-dark) 0%,
            var(--emidaf-blue) 62%,
            #25618f 100%
        );
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.brand {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.92;
}}

.cover-main {{
    max-width: 760px;
}}

.report-label {{
    margin-bottom: 18px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.72;
}}

.cover h1 {{
    margin: 0 0 22px 0;
    font-size: 44px;
    line-height: 1.12;
    font-weight: 720;
    letter-spacing: -0.025em;
}}

.cover-subtitle {{
    max-width: 720px;
    margin: 0;
    font-size: 18px;
    line-height: 1.6;
    opacity: 0.90;
}}

.cover-meta {{
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 14px 40px;
    padding-top: 28px;
    border-top:
        1px solid
        rgba(255, 255, 255, 0.25);
}}

.meta-item {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.meta-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.65;
}}

.meta-value {{
    font-size: 14px;
    font-weight: 600;
}}

.content {{
    padding: 52px 64px 72px;
}}

.executive-summary {{
    margin-bottom: 52px;
}}

.executive-summary h2 {{
    margin: 0 0 8px;
    color: var(--emidaf-blue-dark);
    font-size: 27px;
}}

.executive-summary > p {{
    margin-top: 0;
    color: var(--text-secondary);
}}

.kpi-grid {{
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-top: 26px;
}}

.kpi-card {{
    padding: 22px 18px;
    background: var(--surface-soft);
    border: 1px solid var(--border);
    border-radius: 12px;
    text-align: center;
}}

.kpi-value {{
    color: var(--emidaf-blue);
    font-size: 29px;
    font-weight: 750;
    line-height: 1.1;
}}

.kpi-label {{
    margin-top: 8px;
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 650;
    letter-spacing: 0.035em;
    text-transform: uppercase;
}}

.report-section {{
    margin: 0 0 54px;
    padding-top: 10px;
    page-break-inside: avoid;
}}

.section-heading {{
    display: flex;
    align-items: center;
    gap: 18px;
    padding-bottom: 15px;
    margin-bottom: 24px;
    border-bottom: 2px solid var(--emidaf-blue);
}}

.section-number {{
    flex: 0 0 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--emidaf-blue);
    color: white;
    font-size: 15px;
    font-weight: 750;
}}

.section-kicker {{
    color: var(--emidaf-accent);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.14em;
}}

.section-heading h2 {{
    margin: 2px 0 0;
    color: var(--emidaf-blue-dark);
    font-size: 24px;
    line-height: 1.25;
}}

.section-results h3 {{
    margin: 0 0 14px;
    color: var(--text-primary);
    font-size: 16px;
}}

.nested-block {{
    margin: 20px 0;
}}

.nested-block h4 {{
    margin: 0 0 10px;
    color: var(--emidaf-blue);
    font-size: 14px;
    font-weight: 700;
}}

.table-wrapper {{
    width: 100%;
    overflow-x: auto;
    margin: 12px 0 20px;
}}

.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

.data-table th,
.data-table td {{
    padding: 11px 13px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
}}

.data-table th {{
    background: var(--surface-soft);
    color: var(--text-secondary);
    text-align: left;
    font-weight: 650;
}}

.data-table tbody tr:hover {{
    background: #fafcff;
}}

.value {{
    font-weight: 520;
}}

.clean-list {{
    margin: 8px 0 18px;
    padding-left: 22px;
}}

.clean-list li {{
    margin-bottom: 6px;
}}

.insight-box {{
    margin-top: 22px;
    padding: 17px 19px;
    border-radius: 9px;
}}

.interpretation-box {{
    background: var(--emidaf-blue-light);
    border-left:
        4px solid
        var(--emidaf-accent);
}}

.limitation-box {{
    background: var(--warning-bg);
    border-left:
        4px solid
        #d49a22;
}}

.insight-title {{
    margin-bottom: 7px;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 0.055em;
    text-transform: uppercase;
}}

.insight-box p {{
    margin: 0;
}}

.insight-box ul {{
    margin: 7px 0 0;
    padding-left: 20px;
}}

.insight-box li {{
    margin-bottom: 5px;
}}

.status-box {{
    padding: 18px;
    border-radius: 10px;
}}

.status-box.unavailable {{
    background: #f7f8fa;
    border: 1px solid var(--border);
}}

.status-badge {{
    display: inline-block;
    margin-bottom: 8px;
    padding: 4px 9px;
    border-radius: 99px;
    background: #e9edf2;
    color: #5b6470;
    font-size: 11px;
    font-weight: 750;
    text-transform: uppercase;
}}

.empty-value {{
    color: var(--text-secondary);
    font-style: italic;
}}

.report-footer {{
    padding: 24px 64px;
    border-top: 1px solid var(--border);
    background: var(--surface-soft);
    color: var(--text-secondary);
    font-size: 11px;
    display: flex;
    justify-content: space-between;
    gap: 20px;
}}

@media
screen and (max-width: 760px) {{

    .report-container {{
        margin: 0;
    }}

    .cover {{
        min-height: auto;
        padding: 46px 28px;
    }}

    .cover h1 {{
        font-size: 34px;
    }}

    .cover-meta {{
        grid-template-columns: 1fr;
    }}

    .content {{
        padding: 38px 24px;
    }}

    .kpi-grid {{
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }}

    .report-footer {{
        padding: 20px 24px;
        flex-direction: column;
    }}
}}

@page {{
    size: A4;
    margin: 16mm 14mm 18mm;
}}

@media print {{

    body {{
        background: white;
        font-size: 10.5pt;
    }}

    .report-container {{
        max-width: none;
        margin: 0;
        box-shadow: none;
    }}

    .cover {{
        min-height: 250mm;
        page-break-after: always;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}

    .content {{
        padding: 0;
    }}

    .executive-summary {{
        page-break-after: avoid;
    }}

    .report-section {{
        page-break-inside: avoid;
    }}

    .kpi-card,
    .section-number,
    .interpretation-box,
    .limitation-box {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}

    .data-table tbody tr:hover {{
        background: transparent;
    }}

    .report-footer {{
        padding-left: 0;
        padding-right: 0;
    }}
}}

</style>
</head>

<body>

<div class="report-container">

    <header class="cover">

        <div class="brand">
            {html.escape(organization)}
        </div>

        <div class="cover-main">

            <div class="report-label">
                Rapport scientifique d'analyse
            </div>

            <h1>
                {html.escape(report.title)}
            </h1>

            <p class="cover-subtitle">
                {html.escape(report.subtitle or '')}
            </p>

        </div>

        <div class="cover-meta">

            <div class="meta-item">
                <span class="meta-label">
                    Projet
                </span>
                <span class="meta-value">
                    {html.escape(str(project_name))}
                </span>
            </div>

            <div class="meta-item">
                <span class="meta-label">
                    Jeu de données
                </span>
                <span class="meta-value">
                    {html.escape(str(dataset_name))}
                </span>
            </div>

            <div class="meta-item">
                <span class="meta-label">
                    Généré le
                </span>
                <span class="meta-value">
                    {html.escape(generated_at)}
                </span>
            </div>

            <div class="meta-item">
                <span class="meta-label">
                    Version
                </span>
                <span class="meta-value">
                    {html.escape(str(report.version or '1.0'))}
                </span>
            </div>

        </div>

    </header>


    <main class="content">

        <section class="executive-summary">

            <h2>
                Synthèse générale
            </h2>

            <p>
                {html.escape(report.summary or '')}
            </p>

            <div class="kpi-grid">

                {_kpi_card(
                    observations,
                    "Observations",
                )}

                {_kpi_card(
                    variables,
                    "Variables",
                )}

                {_kpi_card(
                    missing,
                    "Valeurs manquantes",
                )}

                {_kpi_card(
                    duplicates,
                    "Doublons",
                )}

            </div>

        </section>

        {''.join(sections_html)}

    </main>


    <footer class="report-footer">

        <span>
            {html.escape(organization)}
            — Rapport généré par EMIDAF
        </span>

        <span>
            Auteur : {html.escape(author)}
        </span>

        <span>
            {html.escape(generated_at)}
        </span>

    </footer>

</div>

</body>
</html>
"""

    # =====================================================
    # JSON
    # =====================================================

    @staticmethod
    def json(
        report: ReportResult,
    ) -> str:

        payload = {
            "report_name": report.report_name,
            "report_type": report.report_type,
            "title": report.title,
            "subtitle": report.subtitle,
            "summary": report.summary,
            "author": report.author,
            "organization": report.organization,
            "language": report.language,
            "version": report.version,
            "statistics": report.statistics,
            "sections": report.metadata.get(
                "structured_sections",
                [],
            ),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        )
