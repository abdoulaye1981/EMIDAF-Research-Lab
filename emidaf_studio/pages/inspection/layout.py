from pathlib import Path

import pandas as pd
from dash import html, dcc, Input, Output, State, callback, no_update
import re
import dash_bootstrap_components as dbc

from emidaf_core.bootstrap import Bootstrap
from emidaf_core.dataset.profiler import DatasetProfiler


bootstrap = Bootstrap()
bootstrap.initialize()

project_controller = bootstrap.project_controller
dataset_controller = bootstrap.dataset_controller
workspace_manager = bootstrap.workspace_manager


def load_dataset(project_id, dataset_id):
    project = project_controller.get(project_id)

    if project is None:
        return None, None, "Projet introuvable."

    dataset = dataset_controller.get(dataset_id)

    if dataset is None:
        return project, None, "Dataset introuvable."

    if dataset.project_id != project_id:
        return project, None, "Le dataset n'est pas associé à ce projet."

    project_path = workspace_manager.get_project_path(project.name)
    dataset_path = project_path / "datasets" / dataset.stored_filename

    if not dataset_path.exists():
        return project, dataset, (
            "Le fichier physique du dataset est introuvable : "
            f"{dataset_path}"
        )

    try:
        extension = dataset.extension.lower()

        if extension == ".csv":
            dataframe = pd.read_csv(
                dataset_path,
                sep=dataset.separator,
                encoding=dataset.encoding
            )

        elif extension in {".xlsx", ".xls"}:
            dataframe = pd.read_excel(dataset_path)

        else:
            return project, dataset, (
                "Format de fichier non supporté : "
                f"{dataset.extension}"
            )

        return project, dataset, dataframe

    except Exception as exc:
        return project, dataset, (
            f"Erreur lors de la lecture du dataset : {exc}"
        )



def _display_value(value):
    """Formate une valeur pour l'affichage dans Studio."""

    if value is None:
        return "—"

    if isinstance(value, float):
        if pd.isna(value):
            return "—"
        return f"{value:.4f}"

    return str(value)


def _mapping_table(mapping, index_label="Variable"):
    """
    Convertit un dictionnaire de dictionnaires
    en tableau Bootstrap.
    """

    if not mapping:
        return html.P(
            "Aucun résultat disponible.",
            className="text-muted"
        )

    rows = []

    # Toutes les métriques disponibles
    metrics = []

    for values in mapping.values():
        if isinstance(values, dict):
            for key in values:
                if key not in metrics:
                    metrics.append(key)

    if not metrics:
        return html.Pre(
            str(mapping),
            className="small"
        )

    header = html.Thead(
        html.Tr(
            [html.Th(index_label)]
            + [
                html.Th(metric)
                for metric in metrics
            ]
        )
    )

    for name, values in mapping.items():

        if not isinstance(values, dict):
            continue

        cells = [
            html.Td(
                html.Strong(str(name))
            )
        ]

        for metric in metrics:
            value = values.get(metric)

            if isinstance(value, (dict, list, tuple)):
                value = str(value)

            cells.append(
                html.Td(
                    _display_value(value)
                )
            )

        rows.append(
            html.Tr(cells)
        )

    return dbc.Table(
        [
            header,
            html.Tbody(rows)
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-3"
    )


def _render_analysis_result(data):
    """
    Rend les résultats d'un analyseur EMIDAF
    sans dépendre d'une structure trop rigide.
    """

    if not data:
        return dbc.Alert(
            "Aucun résultat disponible pour cette analyse.",
            color="light"
        )

    if not isinstance(data, dict):
        return html.Pre(
            str(data),
            className="small"
        )

    components = []

    for key, value in data.items():

        # -----------------------------
        # Dictionnaire de dictionnaires
        # -----------------------------
        if isinstance(value, dict):

            if value and all(
                isinstance(item, dict)
                for item in value.values()
            ):
                title = (
                    "Résultats par variable"
                    if key == "columns"
                    else key.replace("_", " ").title()
                )

                components.extend(
                    [
                        html.H6(
                            title,
                            className="mt-3"
                        ),
                        _mapping_table(
                            value
                        )
                    ]
                )

            else:
                components.append(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Strong(
                                    key.replace(
                                        "_",
                                        " "
                                    ).title()
                                ),
                                html.Pre(
                                    str(value),
                                    className="small mb-0 mt-2"
                                )
                            ]
                        ),
                        className="mb-2"
                    )
                )

        # -----------------------------
        # Liste
        # -----------------------------
        elif isinstance(value, (list, tuple)):

            if value:
                components.append(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Strong(
                                    key.replace(
                                        "_",
                                        " "
                                    ).title()
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            _display_value(item)
                                        )
                                        for item in value
                                    ],
                                    className="mb-0 mt-2"
                                )
                            ]
                        ),
                        className="mb-2"
                    )
                )

        # -----------------------------
        # Métadonnée simple
        # -----------------------------
        else:
            components.append(
                html.P(
                    [
                        html.Strong(
                            f"{key.replace('_', ' ').title()} : "
                        ),
                        _display_value(value)
                    ],
                    className="mb-1"
                )
            )

    return html.Div(components)





def _build_missing_columns_table(column_statistics):
    """
    Tableau compact des variables contenant des valeurs
    manquantes. Les variables complètes ne sont pas affichées.
    """

    if not isinstance(column_statistics, dict):
        return html.P(
            "Aucune statistique par variable disponible.",
            className="text-muted",
        )

    rows = []

    for column, stats in column_statistics.items():

        if not isinstance(stats, dict):
            continue

        missing_count = int(
            stats.get("missing_count", 0) or 0
        )

        if missing_count <= 0:
            continue

        missing_percentage = float(
            stats.get("missing_percentage", 0.0) or 0.0
        )

        non_missing_percentage = float(
            stats.get(
                "non_missing_percentage",
                100.0 - missing_percentage,
            )
            or 0.0
        )

        dtype = stats.get("dtype", "—")

        rows.append(
            html.Tr(
                [
                    html.Td(
                        html.Strong(str(column))
                    ),
                    html.Td(str(dtype)),
                    html.Td(
                        f"{missing_count:,}"
                    ),
                    html.Td(
                        f"{missing_percentage:.2f} %"
                    ),
                    html.Td(
                        f"{non_missing_percentage:.2f} %"
                    ),
                ]
            )
        )

    if not rows:
        return dbc.Alert(
            "Aucune variable ne contient de valeur manquante.",
            color="success",
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Variable"),
                        html.Th("Type"),
                        html.Th("Manquants"),
                        html.Th("Taux"),
                        html.Th("Complétude"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
        className="mb-3",
    )


def _build_missing_patterns_table(patterns, columns):
    """
    Transforme les patterns binaires de missingness
    en représentation lisible.
    """

    if not patterns:
        return html.P(
            "Aucun pattern de valeurs manquantes détecté.",
            className="text-muted",
        )

    rows = []

    for item in patterns:

        if not isinstance(item, dict):
            continue

        pattern = item.get("pattern", [])
        count = item.get("count", 0)
        percentage = item.get("percentage", 0.0)

        missing_columns = []

        if isinstance(pattern, (list, tuple)):
            for index, flag in enumerate(pattern):

                if (
                    bool(flag)
                    and index < len(columns)
                ):
                    missing_columns.append(
                        str(columns[index])
                    )

        if missing_columns:
            description = ", ".join(
                missing_columns
            ) + " manquant(s)"
        else:
            description = "Aucune valeur manquante"

        rows.append(
            html.Tr(
                [
                    html.Td(description),
                    html.Td(f"{int(count):,}"),
                    html.Td(
                        f"{float(percentage):.2f} %"
                    ),
                ]
            )
        )

    if not rows:
        return html.P(
            "Aucun pattern exploitable.",
            className="text-muted",
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Pattern"),
                        html.Th("Lignes"),
                        html.Th("Pourcentage"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _missing_mechanism_explanation(mechanism):
    """
    Produit une interprétation française et scientifiquement
    prudente du diagnostic MCAR / MAR / MNAR.
    """

    candidate = str(
        mechanism.get("candidate", "")
    ).upper()

    pvalue = mechanism.get("pvalue")

    if candidate == "MCAR":

        if isinstance(pvalue, (int, float)):
            return (
                "Le test de Little ne rejette pas "
                "l'hypothèse d'un mécanisme MCAR "
                f"(p = {pvalue:.4f}). "
                "Les données observées sont donc compatibles "
                "avec un mécanisme MCAR. "
                "Ce résultat ne constitue pas une preuve "
                "formelle de MCAR et n'exclut pas totalement "
                "des mécanismes MAR ou MNAR."
            )

        return (
            "Les résultats disponibles sont compatibles "
            "avec un mécanisme MCAR. Cette conclusion doit "
            "être interprétée avec prudence."
        )

    if candidate == "MAR":
        return (
            "Des associations ont été détectées entre "
            "l'absence de certaines valeurs et des variables "
            "observées. Les données sont donc compatibles "
            "avec un mécanisme MAR. Cette analyse apporte "
            "des indices statistiques mais ne constitue pas "
            "une preuve définitive du mécanisme MAR."
        )

    if candidate == "MNAR":
        return (
            "Le diagnostic signale un risque de mécanisme "
            "MNAR. Un mécanisme MNAR ne peut généralement "
            "pas être confirmé uniquement à partir des "
            "données observées. Une analyse de sensibilité "
            "et une justification métier sont recommandées."
        )

    return (
        "Le mécanisme des valeurs manquantes ne peut pas "
        "être déterminé avec suffisamment de confiance à "
        "partir des informations disponibles."
    )


def _build_missing_diagnostics(profile):
    """
    Affiche le diagnostic des valeurs manquantes
    produit par MissingAnalyzer / MechanismAnalyzer.
    """

    missing = getattr(profile, "missing", None) or {}

    if not isinstance(missing, dict):
        return dbc.Alert(
            "Le diagnostic des valeurs manquantes est indisponible.",
            color="warning",
            className="mt-3",
        )

    summary = missing.get("summary", {}) or {}

    total_missing = int(
        missing.get("total_missing", 0) or 0
    )

    missing_rate = float(
        missing.get("missing_rate", 0.0) or 0.0
    )

    columns_with_missing = int(
        summary.get("columns_with_missing", 0) or 0
    )

    pattern_count = int(
        summary.get(
            "pattern_count",
            len(missing.get("patterns", []) or []),
        )
        or 0
    )

    # =====================================================
    # Aucun manquant
    # =====================================================

    if total_missing == 0:
        return html.Div(
            [
                html.H5(
                    "🧩 Diagnostic des valeurs manquantes",
                    className="mt-4",
                ),
                dbc.Alert(
                    [
                        html.Strong(
                            "✅ Aucune valeur manquante détectée. "
                        ),
                        html.Span(
                            (
                                "Le diagnostic MCAR / MAR / MNAR "
                                "n'est pas requis pour ce dataset."
                            )
                        ),
                    ],
                    color="success",
                ),
            ]
        )

    # =====================================================
    # Vue d'ensemble
    # =====================================================

    overview = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Valeurs manquantes"),
                            html.H4(f"{total_missing:,}"),
                        ]
                    )
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Taux global"),
                            html.H4(f"{missing_rate:.2f} %"),
                        ]
                    )
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Variables affectées"),
                            html.H4(str(columns_with_missing)),
                        ]
                    )
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Patterns détectés"),
                            html.H4(str(pattern_count)),
                        ]
                    )
                ),
                width=3,
            ),
        ],
        className="mb-3",
    )

    # =====================================================
    # Manquants par variable
    # =====================================================

    column_statistics = (
        missing.get("column_statistics", {}) or {}
    )

    column_section = []

    if isinstance(column_statistics, dict) and column_statistics:
        column_section = [
            html.H6(
                "📊 Valeurs manquantes par variable",
                className="mt-3",
            ),
            _build_missing_columns_table(
                column_statistics
            ),
        ]

    # =====================================================
    # Patterns
    # =====================================================

    patterns = missing.get("patterns", []) or []

    pattern_section = []

    if patterns:
        pattern_section = [
            html.H6(
                "🧬 Patterns de valeurs manquantes",
                className="mt-3",
            ),
            _build_missing_patterns_table(
                patterns,
                list(column_statistics.keys()),
            ),
        ]

    # =====================================================
    # Diagnostic MCAR / MAR / MNAR
    # =====================================================

    mechanism = (
        missing.get("missing_mechanism", {}) or {}
    )

    mechanism_components = []

    if not mechanism:
        mechanism_components.append(
            dbc.Alert(
                (
                    "Le mécanisme des valeurs manquantes "
                    "n'a pas pu être évalué."
                ),
                color="warning",
            )
        )

    else:
        status = mechanism.get(
            "status",
            "Indéterminé",
        )

        candidate = mechanism.get(
            "candidate",
            "Indéterminé",
        )

        confidence = mechanism.get(
            "confidence"
        )

        test_name = mechanism.get(
            "test_name"
        )

        statistic = mechanism.get(
            "statistic"
        )

        pvalue = mechanism.get(
            "pvalue"
        )

        explanation = mechanism.get(
            "explanation"
        )

        mechanism_components.append(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Statut"),
                                    html.H4(str(status)),
                                ]
                            )
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Mécanisme candidat"
                                    ),
                                    html.H4(
                                        str(candidate)
                                    ),
                                ]
                            )
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Confiance"
                                    ),
                                    html.H4(
                                        (
                                            f"{confidence:.2f}"
                                            if isinstance(
                                                confidence,
                                                (int, float),
                                            )
                                            else "—"
                                        )
                                    ),
                                ]
                            )
                        ),
                        width=4,
                    ),
                ],
                className="mb-3",
            )
        )

        if test_name:
            mechanism_components.append(
                html.P(
                    [
                        html.Strong("Méthode : "),
                        str(test_name),
                    ]
                )
            )

        if statistic is not None:
            mechanism_components.append(
                html.P(
                    [
                        html.Strong("Statistique : "),
                        _display_value(statistic),
                    ]
                )
            )

        if pvalue is not None:
            mechanism_components.append(
                html.P(
                    [
                        html.Strong("p-value : "),
                        _display_value(pvalue),
                    ]
                )
            )

        mechanism_components.append(
            dbc.Alert(
                _missing_mechanism_explanation(
                    mechanism
                ),
                color="info",
                className="mt-2",
            )
        )

        tests = mechanism.get("tests", {}) or {}

        test_items = []

        labels = {
            "mcar": "MCAR — Missing Completely At Random",
            "mar": "MAR — Missing At Random",
            "mnar": "MNAR — Missing Not At Random",
        }

        for key in ("mcar", "mar", "mnar"):
            if key in tests:
                test_items.append(
                    dbc.AccordionItem(
                        _render_analysis_result(
                            tests[key]
                        ),
                        title=labels[key],
                    )
                )

        if test_items:
            mechanism_components.append(
                dbc.Accordion(
                    test_items,
                    start_collapsed=True,
                    always_open=True,
                    className="mb-3",
                )
            )

    # =====================================================
    # Recommandations
    # =====================================================

    recommendations = (
        missing.get("recommendations", []) or []
    )

    recommendation_section = []

    if recommendations:
        recommendation_section = [
            html.H6(
                "💡 Recommandations",
                className="mt-3",
            ),
            dbc.Alert(
                html.Ul(
                    [
                        html.Li(str(item))
                        for item in recommendations
                    ],
                    className="mb-0",
                ),
                color="light",
            ),
        ]

    scientific_note = dbc.Alert(
        [
            html.Strong(
                "Interprétation scientifique : "
            ),
            html.Span(
                (
                    "MCAR signifie que l'absence est indépendante "
                    "des variables observées et non observées. "
                    "MAR indique une dépendance compatible avec "
                    "des variables observées. MNAR reste difficile "
                    "à établir uniquement à partir des données "
                    "observées et doit être interprété comme un "
                    "risque nécessitant une analyse de sensibilité."
                )
            ),
        ],
        color="secondary",
        className="mt-3",
    )

    return html.Div(
        [
            html.H5(
                "🧩 Diagnostic des valeurs manquantes",
                className="mt-4",
            ),
            html.P(
                (
                    "Analyse des quantités manquantes, des patterns "
                    "et du mécanisme probable MCAR / MAR / MNAR."
                ),
                className="text-muted",
            ),
            overview,
            *column_section,
            *pattern_section,
            html.H6(
                "🧠 Mécanisme des données manquantes",
                className="mt-4",
            ),
            *mechanism_components,
            *recommendation_section,
            scientific_note,
        ]
    )



def _result_payload(value):
    """
    Normalise les résultats venant éventuellement
    d'un AnalyzerResult.
    """

    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    result = getattr(value, "result", None)

    if isinstance(result, dict):
        return result

    return {}


def _build_distribution_view(data):
    data = _result_payload(data)

    columns = data.get("columns", {}) or {}

    if not columns:
        return dbc.Alert(
            "Aucune distribution numérique disponible.",
            color="light",
        )

    rows = []

    for variable, stats in columns.items():
        rows.append(
            html.Tr(
                [
                    html.Td(html.Strong(variable)),
                    html.Td(_display_value(stats.get("count"))),
                    html.Td(_display_value(stats.get("mean"))),
                    html.Td(_display_value(stats.get("median"))),
                    html.Td(_display_value(stats.get("std"))),
                    html.Td(_display_value(stats.get("variance"))),
                    html.Td(_display_value(stats.get("minimum"))),
                    html.Td(_display_value(stats.get("maximum"))),
                ]
            )
        )

    return html.Div(
        [
            dbc.Alert(
                (
                    f"{len(columns)} variable(s) numérique(s) "
                    "analysée(s)."
                ),
                color="info",
            ),

            dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Variable"),
                                html.Th("n"),
                                html.Th("Moyenne"),
                                html.Th("Médiane"),
                                html.Th("Écart-type"),
                                html.Th("Variance"),
                                html.Th("Minimum"),
                                html.Th("Maximum"),
                            ]
                        )
                    ),
                    html.Tbody(rows),
                ],
                bordered=True,
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),
        ]
    )


def _build_normality_view(data):
    data = _result_payload(data)

    columns = data.get("columns", {}) or {}
    test = data.get("test", "—")
    alpha = data.get("alpha")

    if not columns:
        return dbc.Alert(
            "Aucun test de normalité disponible.",
            color="light",
        )

    rows = []

    for variable, stats in columns.items():

        normal = bool(stats.get("normal", False))

        verdict = (
            "Compatible avec la normalité"
            if normal
            else "Normalité rejetée"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(html.Strong(variable)),
                    html.Td(_display_value(stats.get("n"))),
                    html.Td(
                        _display_value(stats.get("statistic"))
                    ),
                    html.Td(
                        _display_value(stats.get("p_value"))
                    ),
                    html.Td(verdict),
                ]
            )
        )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Test"),
                                    html.H5(str(test)),
                                ]
                            )
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Seuil α"),
                                    html.H5(
                                        _display_value(alpha)
                                    ),
                                ]
                            )
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),

            dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Variable"),
                                html.Th("n"),
                                html.Th("Statistique"),
                                html.Th("p-value"),
                                html.Th("Conclusion"),
                            ]
                        )
                    ),
                    html.Tbody(rows),
                ],
                bordered=True,
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Alert(
                (
                    "Une p-value ≤ α conduit à rejeter "
                    "l'hypothèse de normalité."
                ),
                color="secondary",
            ),
        ]
    )


def _build_outlier_view(data):
    data = _result_payload(data)

    columns = data.get("columns", {}) or {}
    method = data.get("method", "—")
    warnings = data.get("warnings", []) or []
    recommendations = data.get("recommendations", []) or []

    if not columns:
        return dbc.Alert(
            "Aucune analyse de valeurs aberrantes disponible.",
            color="light",
        )

    rows = []

    total_outliers = 0

    for variable, stats in columns.items():

        count = int(stats.get("outliers", 0) or 0)
        total_outliers += count

        rows.append(
            html.Tr(
                [
                    html.Td(html.Strong(variable)),
                    html.Td(
                        _display_value(stats.get("count"))
                    ),
                    html.Td(str(count)),
                    html.Td(
                        f"{float(stats.get('outlier_rate', 0) or 0):.2f} %"
                    ),
                    html.Td(
                        _display_value(stats.get("lower_bound"))
                    ),
                    html.Td(
                        _display_value(stats.get("upper_bound"))
                    ),
                ]
            )
        )

    components = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Méthode"),
                                html.H5(str(method)),
                            ]
                        )
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Valeurs aberrantes détectées"
                                ),
                                html.H5(
                                    str(total_outliers)
                                ),
                            ]
                        )
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Variable"),
                            html.Th("n"),
                            html.Th("Outliers"),
                            html.Th("Taux"),
                            html.Th("Borne inf."),
                            html.Th("Borne sup."),
                        ]
                    )
                ),
                html.Tbody(rows),
            ],
            bordered=True,
            striped=True,
            hover=True,
            responsive=True,
            size="sm",
        ),
    ]

    if warnings:
        components.append(
            dbc.Alert(
                html.Ul(
                    [
                        html.Li(str(item))
                        for item in warnings
                    ],
                    className="mb-0",
                ),
                color="warning",
            )
        )

    if recommendations:
        components.append(
            dbc.Alert(
                [
                    html.Strong("Recommandations"),
                    html.Ul(
                        [
                            html.Li(str(item))
                            for item in recommendations
                        ],
                        className="mb-0 mt-2",
                    ),
                ],
                color="light",
            )
        )

    return html.Div(components)


def _matrix_table(matrix):
    if not isinstance(matrix, dict) or not matrix:
        return html.P(
            "Matrice indisponible.",
            className="text-muted",
        )

    variables = list(matrix.keys())

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [html.Th("Variable")]
                    + [
                        html.Th(variable)
                        for variable in variables
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(html.Strong(row))
                        ]
                        + [
                            html.Td(
                                _display_value(
                                    matrix.get(row, {}).get(col)
                                )
                            )
                            for col in variables
                        ]
                    )
                    for row in variables
                ]
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size="sm",
    )


def _build_correlation_view(data):
    data = _result_payload(data)

    matrix = (
        data.get("correlation_matrix")
        or data.get("matrix")
        or {}
    )

    pairs = data.get("pairs", []) or []

    components = [
        html.H6(
            "Matrice de corrélation",
            className="mb-2",
        ),
        _matrix_table(matrix),
    ]

    if pairs:
        pair_rows = []

        for item in pairs:
            if not isinstance(item, dict):
                continue

            pair_rows.append(
                html.Tr(
                    [
                        html.Td(
                            item.get("variable_1", "—")
                        ),
                        html.Td(
                            item.get("variable_2", "—")
                        ),
                        html.Td(
                            _display_value(
                                item.get("correlation")
                            )
                        ),
                    ]
                )
            )

        components.extend(
            [
                html.H6(
                    "Paires de variables",
                    className="mt-3",
                ),
                dbc.Table(
                    [
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("Variable 1"),
                                    html.Th("Variable 2"),
                                    html.Th("Corrélation"),
                                ]
                            )
                        ),
                        html.Tbody(pair_rows),
                    ],
                    bordered=True,
                    striped=True,
                    hover=True,
                    responsive=True,
                    size="sm",
                ),
                dbc.Alert(
                    (
                        "La corrélation mesure une association "
                        "linéaire ; elle n'implique pas une "
                        "relation de causalité."
                    ),
                    color="secondary",
                ),
            ]
        )

    return html.Div(components)


def _build_multicollinearity_view(data):
    data = _result_payload(data)

    vif = data.get("vif", {}) or {}
    interpretation = (
        data.get("vif_interpretation", {}) or {}
    )

    detected = bool(
        data.get("multicollinearity_detected", False)
    )

    status = data.get("status", "—")

    rows = []

    for variable, value in vif.items():
        rows.append(
            html.Tr(
                [
                    html.Td(html.Strong(variable)),
                    html.Td(_display_value(value)),
                    html.Td(
                        interpretation.get(
                            variable,
                            "—",
                        )
                    ),
                ]
            )
        )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Statut"),
                                    html.H5(str(status)),
                                ]
                            )
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6(
                                        "Multicolinéarité détectée"
                                    ),
                                    html.H5(
                                        "Oui"
                                        if detected
                                        else "Non"
                                    ),
                                ]
                            )
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),

            html.H6("Variance Inflation Factor (VIF)"),

            dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Variable"),
                                html.Th("VIF"),
                                html.Th("Interprétation"),
                            ]
                        )
                    ),
                    html.Tbody(rows),
                ],
                bordered=True,
                striped=True,
                hover=True,
                responsive=True,
                size="sm",
            ),

            dbc.Alert(
                (
                    "En pratique, un VIF proche de 1 indique "
                    "une faible multicolinéarité. Des valeurs "
                    "élevées nécessitent une investigation "
                    "avant la modélisation."
                ),
                color="secondary",
            ),
        ]
    )


def build_profile_summary(profile):
    summary = profile.summary

    # Résultats détaillés du DatatypeAnalyzer
    datatypes = profile.datatypes or {}
    structure = profile.structure or {}

    numeric_columns = datatypes.get("numeric", [])
    categorical_columns = datatypes.get("categorical", [])
    datetime_columns = datatypes.get("datetime", [])
    boolean_columns = datatypes.get("boolean", [])
    text_columns = datatypes.get("text", [])
    unknown_columns = datatypes.get("unknown", [])

    # Mémoire
    memory_usage = structure.get("memory_usage", summary.memory_usage)

    if memory_usage < 1024:
        memory_display = f"{memory_usage} octets"
    elif memory_usage < 1024 ** 2:
        memory_display = f"{memory_usage / 1024:.2f} Ko"
    else:
        memory_display = f"{memory_usage / (1024 ** 2):.2f} Mo"

    return dbc.Container(
        [
            html.H4(
                "📊 Résumé du profil",
                className="mt-4"
            ),

            # -------------------------------------------------
            # Indicateurs généraux
            # -------------------------------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Lignes"),
                                    html.H4(f"{summary.rows:,}")
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes"),
                                    html.H4(f"{summary.columns:,}")
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Cellules"),
                                    html.H4(f"{summary.cells:,}")
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score global"),
                                    html.H4(
                                        f"{summary.overall_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-3"
            ),

            dbc.Alert(
                [
                    html.Strong("Statut du profil : "),
                    summary.profile_status
                ],
                color="success"
            ),

            # -------------------------------------------------
            # NOUVEAU : Structure et types
            # -------------------------------------------------
            html.H5(
                "🧬 Structure et types",
                className="mt-4"
            ),

            dbc.Card(
                [
                    dbc.CardHeader(
                        "📐 Structure du dataset"
                    ),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H6("Lignes"),
                                            html.H4(
                                                f"{structure.get('rows', summary.rows):,}"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6("Colonnes"),
                                            html.H4(
                                                f"{structure.get('columns', summary.columns):,}"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6("Cellules"),
                                            html.H4(
                                                f"{summary.cells:,}"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            html.H6("Mémoire"),
                                            html.H4(memory_display)
                                        ],
                                        width=3
                                    )
                                ]
                            )
                        ]
                    )
                ],
                className="mb-3"
            ),

            html.H6(
                "🔢 Répartition des types de variables",
                className="mt-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Numériques"),
                                    html.H4(
                                        len(numeric_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Catégorielles"),
                                    html.H4(
                                        len(categorical_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Datetimes"),
                                    html.H4(
                                        len(datetime_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Booléennes"),
                                    html.H4(
                                        len(boolean_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Texte"),
                                    html.H4(
                                        len(text_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Inconnues"),
                                    html.H4(
                                        len(unknown_columns)
                                    )
                                ]
                            )
                        ),
                        width=2
                    )
                ],
                className="mb-3"
            ),

            # -------------------------------------------------
            # Variables par type
            # -------------------------------------------------
            html.H6(
                "📋 Variables par type",
                className="mt-4"
            ),

            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(numeric_columns)
                                if numeric_columns
                                else "Aucune"
                            )
                        ],
                        title="🔢 Variables numériques"
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(categorical_columns)
                                if categorical_columns
                                else "Aucune"
                            )
                        ],
                        title="🏷️ Variables catégorielles"
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(datetime_columns)
                                if datetime_columns
                                else "Aucune"
                            )
                        ],
                        title="📅 Variables datetime"
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(boolean_columns)
                                if boolean_columns
                                else "Aucune"
                            )
                        ],
                        title="☑️ Variables booléennes"
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(text_columns)
                                if text_columns
                                else "Aucune"
                            )
                        ],
                        title="🔤 Variables texte"
                    ),

                    dbc.AccordionItem(
                        [
                            html.P(
                                ", ".join(unknown_columns)
                                if unknown_columns
                                else "Aucune"
                            )
                        ],
                        title="❓ Variables inconnues"
                    )
                ],
                start_collapsed=True,
                className="mb-3"
            ),

            # -------------------------------------------------
            # Qualité des données
            # -------------------------------------------------
            html.H5(
                "🧹 Qualité des données",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Valeurs manquantes"),
                                    html.H4(
                                        f"{summary.missing_values:,}"
                                    ),
                                    html.P(
                                        f"{summary.missing_percentage:.2f} %"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Doublons"),
                                    html.H4(
                                        f"{summary.duplicate_rows:,}"
                                    ),
                                    html.P(
                                        f"{summary.duplicate_percentage:.2f} %"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes constantes"),
                                    html.H4(
                                        summary.constant_columns
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes vides"),
                                    html.H4(
                                        summary.empty_columns
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score de qualité"),
                                    html.H4(
                                        f"{summary.quality_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Score de complétude"),
                                    html.H4(
                                        f"{summary.completeness_score:.1f}/100"
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Niveau de qualité"),
                                    html.H4(
                                        summary.quality_level
                                    )
                                ]
                            )
                        ),
                        width=4
                    )
                ],
                className="mb-3"
            )
            ,

            _build_missing_diagnostics(
                profile
            ),


            # -------------------------------------------------
            # Analyse statistique avancée
            # -------------------------------------------------

            html.H5(
                "📈 Analyse statistique avancée",
                className="mt-4"
            ),

            html.P(
                (
                    "Exploration des distributions, de la normalité, "
                    "des valeurs aberrantes, des corrélations et "
                    "de la multicolinéarité."
                ),
                className="text-muted"
            ),

            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        _build_distribution_view(
                            getattr(
                                profile,
                                "distributions",
                                None
                            )
                        ),
                        title="📊 Distributions"
                    ),

                    dbc.AccordionItem(
                        _build_normality_view(
                            getattr(
                                profile,
                                "normality",
                                None
                            )
                        ),
                        title="🔔 Normalité"
                    ),

                    dbc.AccordionItem(
                        _build_outlier_view(
                            getattr(
                                profile,
                                "outliers",
                                None
                            )
                        ),
                        title="⚠️ Valeurs aberrantes"
                    ),

                    dbc.AccordionItem(
                        _build_correlation_view(
                            getattr(
                                profile,
                                "correlations",
                                None
                            )
                        ),
                        title="🔗 Corrélations"
                    ),

                    dbc.AccordionItem(
                        _build_multicollinearity_view(
                            getattr(
                                profile,
                                "multicollinearity",
                                None
                            )
                        ),
                        title="🧮 Multicolinéarité"
                    ),
                ],
                start_collapsed=True,
                always_open=True,
                className="mb-4"
            )

        ],
        fluid=True
    )

def inspection_layout(project_id, dataset_id):

    project, dataset, result = load_dataset(
        project_id,
        dataset_id
    )

    if isinstance(result, str):
        return dbc.Container(
            [
                html.H2("🔎 Inspection du dataset"),
                html.Hr(),

                dbc.Alert(
                    result,
                    color="danger"
                ),

                dcc.Link(
                    dbc.Button(
                        "← Retour au projet",
                        color="secondary"
                    ),
                    href=f"/projects/{project_id}"
                )
            ],
            fluid=True
        )

    dataframe = result

    rows, columns = dataframe.shape
    size_kb = dataset.size / 1024

    format_name = {
        ".csv": "CSV",
        ".xlsx": "Excel",
        ".xls": "Excel"
    }.get(
        dataset.extension.lower(),
        dataset.extension.upper()
    )

    preview = dataframe.head(10)

    preview_table = dbc.Table.from_dataframe(
        preview,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True
    )

    # Profilage automatique du dataset
    profile_summary = html.Div(
        [
            html.P(
                "Cliquez sur « Profiler le dataset » pour lancer "
                "l'analyse complète.",
                className="text-muted"
            )
        ]
    )
    return dbc.Container(
        [
            html.H2("🔎 Inspection du dataset"),
            html.Hr(),

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects"
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}"
                    },
                    {
                        "label": dataset.name,
                        "active": True
                    }
                ]
            ),

            html.H4(
                "📋 Informations générales",
                className="mt-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Nom du dataset"),
                                    html.H5(dataset.name)
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Fichier"),
                                    html.H5(
                                        dataset.original_filename
                                    )
                                ]
                            )
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Format"),
                                    html.H5(format_name)
                                ]
                            )
                        ),
                        width=4
                    )
                ],
                className="mb-3"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Lignes"),
                                    html.H4(f"{rows:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Colonnes"),
                                    html.H4(f"{columns:,}")
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Taille"),
                                    html.H4(
                                        f"{size_kb:.2f} Ko"
                                    )
                                ]
                            )
                        ),
                        width=3
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Cellules"),
                                    html.H4(
                                        f"{rows * columns:,}"
                                    )
                                ]
                            )
                        ),
                        width=3
                    )
                ],
                className="mb-4"
            ),

            # ---------------------------------------------------------
            # Profilage du dataset
            # ---------------------------------------------------------
            dbc.Card(
              [
                dbc.CardHeader("Profilage du dataset"),
                dbc.CardBody(
                  [
                      dbc.Button(
                         "Profiler le dataset",
                         id="btn-profile-dataset",
                         color="primary",
                         className="mb-3",
                      ),
                      html.Div(
                         profile_summary,
                         id="profile-result",
                      ),
                  ]
                ),
              ],
              className="mb-4",
            ),
            html.H4(
                "👁️ Aperçu des données",
                className="mt-4"
            ),

            dbc.Alert(
                "Affichage des 10 premières lignes.",
                color="info"
            ),

            preview_table,

            html.Hr(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "🧹 Ouvrir EIDPP",
                                color="primary",
                                className="w-100",
                            ),
                            href=(
                                f"/projects/{project_id}"
                                f"/datasets/{dataset_id}/eidpp"
                            ),
                        ),
                        md=6,
                    ),

                    dbc.Col(
                        dcc.Link(
                            dbc.Button(
                                "← Retour au projet",
                                color="secondary",
                                className="w-100",
                            ),
                            href=f"/projects/{project_id}",
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
            ),

            dcc.Store(
                id="inspection-project-id",
                data=project_id,
            ),
            dcc.Store(
                id="inspection-dataset-id",
                data=dataset_id,
            ),
        ],
        fluid=True
    )

@callback(
    Output("profile-result", "children"),
    Input("btn-profile-dataset", "n_clicks"),
    State("inspection-project-id", "data"),
    State("inspection-dataset-id", "data"),
    prevent_initial_call=True,
)
def run_dataset_profile(n_clicks, project_id, dataset_id):
    """Lance le profilage complet du dataset à la demande."""

    if not n_clicks:
        return no_update

    project, dataset, result = load_dataset(
        project_id,
        dataset_id,
    )

    if isinstance(result, str):
        return dbc.Alert(
            result,
            color="danger",
            className="mt-3",
        )

    try:
        profiler = DatasetProfiler()
        profile = profiler.profile(result)

        return build_profile_summary(profile)

    except Exception as exc:
        return dbc.Alert(
            [
                html.Strong("Erreur lors du profilage : "),
                html.Span(str(exc)),
            ],
            color="danger",
            className="mt-3",
        )
