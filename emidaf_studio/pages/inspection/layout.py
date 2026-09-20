from pathlib import Path

import pandas as pd
from dash import html, dcc, Input, Output, State, callback, no_update
import re
import dash_bootstrap_components as dbc
from flask import has_request_context, session

from emidaf_core.bootstrap import Bootstrap
from emidaf_core.dataset.profiler import DatasetProfiler


bootstrap = Bootstrap()
bootstrap.initialize()

project_controller = bootstrap.project_controller
dataset_controller = bootstrap.dataset_controller
workspace_manager = bootstrap.workspace_manager


def _current_user_id():
    """
    Retourne l'identifiant de l'utilisateur connecté.

    Aucun accès aux données n'est autorisé
    en dehors d'une requête utilisateur valide.
    """
    if not has_request_context():
        return None

    value = session.get("user_id")

    if value is None:
        return None

    return int(value)


def load_dataset(project_id, dataset_id):
    """
    Charge un dataset uniquement si :

    1. une session utilisateur valide existe ;
    2. le projet appartient à cet utilisateur ;
    3. le dataset existe ;
    4. le dataset appartient bien à ce projet.
    """
    user_id = _current_user_id()

    if user_id is None:
        return (
            None,
            None,
            "Session utilisateur invalide "
            "ou expirée.",
        )

    try:
        project_id = int(project_id)
        dataset_id = int(dataset_id)

    except (TypeError, ValueError):
        return (
            None,
            None,
            "Identifiant de projet ou de dataset invalide.",
        )

    project = project_controller.get_for_user(
        project_id,
        user_id,
    )

    if project is None:
        return (
            None,
            None,
            (
                "Projet introuvable ou "
                "accès non autorisé."
            ),
        )

    dataset = dataset_controller.get(
        dataset_id
    )

    if dataset is None:
        return (
            project,
            None,
            "Dataset introuvable.",
        )

    if int(dataset.project_id) != project_id:
        return (
            project,
            None,
            (
                "Le dataset n'est pas associé "
                "à ce projet."
            ),
        )

    project_path = (
        workspace_manager
        .get_project_path(
            project.name
        )
    )

    dataset_path = (
        project_path
        / "datasets"
        / dataset.stored_filename
    )

    if not dataset_path.exists():
        return (
            project,
            dataset,
            (
                "Le fichier physique du dataset "
                "est introuvable : "
                f"{dataset_path}"
            ),
        )

    try:
        extension = dataset.extension.lower()

        if extension == ".csv":
            dataframe = pd.read_csv(
                dataset_path,
                sep=dataset.separator,
                encoding=dataset.encoding,
            )

        elif extension in {
            ".xlsx",
            ".xls",
        }:
            dataframe = pd.read_excel(
                dataset_path
            )

        else:
            return (
                project,
                dataset,
                (
                    "Format de fichier non supporté : "
                    f"{dataset.extension}"
                ),
            )

        return (
            project,
            dataset,
            dataframe,
        )

    except Exception as exc:
        return (
            project,
            dataset,
            (
                "Erreur lors de la lecture "
                f"du dataset : {exc}"
            ),
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
                    "Diagnostic des valeurs manquantes",
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
                "Valeurs manquantes par variable",
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
                "Patterns de valeurs manquantes",
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
            "mcar": "MCAR : Missing Completely At Random",
            "mar": "MAR : Missing At Random",
            "mnar": "MNAR : Missing Not At Random",
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
                "Recommandations",
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
                "Diagnostic des valeurs manquantes",
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
                "Mécanisme des données manquantes",
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
                "Résumé du profil",
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
                "Structure et types",
                className="mt-4"
            ),

            dbc.Card(
                [
                    dbc.CardHeader(
                        "Structure du dataset"
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
                "Répartition des types de variables",
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
                "Variables par type",
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
                        title="Variables numériques"
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
                        title="Variables texte"
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
                "Qualité des données",
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
                "Analyse statistique avancée",
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
                        title="Distributions"
                    ),

                    dbc.AccordionItem(
                        _build_normality_view(
                            getattr(
                                profile,
                                "normality",
                                None
                            )
                        ),
                        title="Normalité"
                    ),

                    dbc.AccordionItem(
                        _build_outlier_view(
                            getattr(
                                profile,
                                "outliers",
                                None
                            )
                        ),
                        title="Valeurs aberrantes"
                    ),

                    dbc.AccordionItem(
                        _build_correlation_view(
                            getattr(
                                profile,
                                "correlations",
                                None
                            )
                        ),
                        title="Corrélations"
                    ),

                    dbc.AccordionItem(
                        _build_multicollinearity_view(
                            getattr(
                                profile,
                                "multicollinearity",
                                None
                            )
                        ),
                        title="Multicolinéarité"
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
        dataset_id,
    )

    # ======================================================
    # ÉTAT D'ERREUR
    # ======================================================

    if isinstance(result, str):

        return dbc.Container(
            [
                html.Section(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "INSPECTION",
                                            className=(
                                                "inspection-v2-kicker"
                                            ),
                                        ),
                                        html.Span(
                                            "QUALITÉ DES DONNÉES",
                                            className=(
                                                "inspection-v2-eyebrow"
                                            ),
                                        ),
                                    ],
                                    className=(
                                        "d-flex align-items-center "
                                        "gap-2 mb-3"
                                    ),
                                ),

                                html.H1(
                                    "Inspection du jeu de données",
                                    className=(
                                        "inspection-v2-title"
                                    ),
                                ),

                                html.P(
                                    (
                                        "Le jeu de données ne peut "
                                        "pas être chargé dans son "
                                        "état actuel."
                                    ),
                                    className=(
                                        "inspection-v2-subtitle"
                                    ),
                                ),
                            ]
                        ),
                    ],
                    className="inspection-v2-hero",
                ),

                dbc.Alert(
                    [
                        html.I(
                            className=(
                                "bi bi-exclamation-triangle "
                                "me-2"
                            )
                        ),
                        result,
                    ],
                    color="danger",
                    className="inspection-v2-error",
                ),

                dcc.Link(
                    [
                        html.I(
                            className=(
                                "bi bi-arrow-left me-2"
                            )
                        ),
                        "Retour au projet",
                    ],
                    href=f"/projects/{project_id}",
                    className=(
                        "inspection-v2-secondary-link"
                    ),
                ),
            ],
            fluid=True,
            className="inspection-v2-page",
        )

    # ======================================================
    # DONNÉES
    # ======================================================

    dataframe = result

    rows, columns = dataframe.shape

    size_kb = dataset.size / 1024

    cells = rows * columns

    format_name = {
        ".csv": "CSV",
        ".xlsx": "Excel",
        ".xls": "Excel",
    }.get(
        dataset.extension.lower(),
        dataset.extension.upper(),
    )

    preview = dataframe.head(10)

    preview_table = dbc.Table.from_dataframe(
        preview,
        striped=True,
        bordered=False,
        hover=True,
        responsive=True,
        className="inspection-v2-table",
    )

    profile_summary = html.Div(
        [
            html.Div(
                html.I(
                    className="bi bi-bar-chart-line"
                ),
                className=(
                    "inspection-v2-profile-empty-icon"
                ),
            ),

            html.H3(
                "Profilage scientifique",
                className=(
                    "inspection-v2-profile-empty-title"
                ),
            ),

            html.P(
                (
                    "Lancez le profilage pour analyser "
                    "la structure, la qualité, les valeurs "
                    "manquantes, les valeurs aberrantes, "
                    "les corrélations et les autres "
                    "indicateurs disponibles."
                ),
                className=(
                    "inspection-v2-profile-empty-text"
                ),
            ),
        ],
        className="inspection-v2-profile-empty",
    )

    # ======================================================
    # LAYOUT
    # ======================================================

    return dbc.Container(
        [
            # --------------------------------------------------
            # HERO
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        "INSPECTION",
                                        className=(
                                            "inspection-v2-kicker"
                                        ),
                                    ),

                                    html.Span(
                                        "QUALITÉ DES DONNÉES",
                                        className=(
                                            "inspection-v2-eyebrow"
                                        ),
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                "Inspection du jeu de données",
                                className=(
                                    "inspection-v2-title"
                                ),
                            ),

                            html.P(
                                (
                                    "Examinez la structure du jeu "
                                    "de données, contrôlez sa qualité "
                                    "et lancez le profilage scientifique "
                                    "avant toute transformation."
                                ),
                                className=(
                                    "inspection-v2-subtitle"
                                ),
                            ),
                        ]
                    ),

                    html.Div(
                        html.I(
                            className=(
                                "bi bi-search "
                                "inspection-v2-hero-icon"
                            )
                        ),
                        className=(
                            "inspection-v2-hero-icon-box"
                        ),
                    ),
                ],
                className="inspection-v2-hero",
            ),

            # --------------------------------------------------
            # FIL D'ARIANE
            # --------------------------------------------------

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects",
                    },
                    {
                        "label": project.name,
                        "href": (
                            f"/projects/{project_id}"
                        ),
                    },
                    {
                        "label": dataset.name,
                        "active": True,
                    },
                ],
                className="inspection-v2-breadcrumb",
            ),

            # --------------------------------------------------
            # CONTEXTE DATASET
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                html.I(
                                    className=(
                                        "bi bi-database "
                                        "inspection-v2-context-icon"
                                    )
                                ),
                                className=(
                                    "inspection-v2-context-icon-box"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        "JEU DE DONNÉES ACTIF",
                                        className=(
                                            "inspection-v2-context-label"
                                        ),
                                    ),

                                    html.Div(
                                        dataset.name,
                                        className=(
                                            "inspection-v2-context-title"
                                        ),
                                    ),

                                    html.Div(
                                        dataset.original_filename,
                                        className=(
                                            "inspection-v2-context-file"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                format_name,
                                className=(
                                    "inspection-v2-format-badge"
                                ),
                            ),
                        ],
                        className=(
                            "inspection-v2-context-card"
                        ),
                    ),
                ],
                className=(
                    "inspection-v2-context-section"
                ),
            ),

            # --------------------------------------------------
            # INDICATEURS
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "INFORMATIONS GÉNÉRALES",
                        className=(
                            "inspection-v2-section-kicker"
                        ),
                    ),

                    html.H2(
                        "Structure du jeu de données",
                        className=(
                            "inspection-v2-section-title"
                        ),
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-list-ol"
                                            )
                                        ),
                                        className=(
                                            "inspection-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        f"{rows:,}",
                                        className=(
                                            "inspection-v2-stat-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Lignes",
                                        className=(
                                            "inspection-v2-stat-label"
                                        ),
                                    ),
                                ],
                                className=(
                                    "inspection-v2-stat-card"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-layout-three-columns"
                                            )
                                        ),
                                        className=(
                                            "inspection-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        f"{columns:,}",
                                        className=(
                                            "inspection-v2-stat-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Colonnes",
                                        className=(
                                            "inspection-v2-stat-label"
                                        ),
                                    ),
                                ],
                                className=(
                                    "inspection-v2-stat-card"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-device-ssd"
                                            )
                                        ),
                                        className=(
                                            "inspection-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        f"{size_kb:.2f} Ko",
                                        className=(
                                            "inspection-v2-stat-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Taille",
                                        className=(
                                            "inspection-v2-stat-label"
                                        ),
                                    ),
                                ],
                                className=(
                                    "inspection-v2-stat-card"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-grid-3x3"
                                            )
                                        ),
                                        className=(
                                            "inspection-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        f"{cells:,}",
                                        className=(
                                            "inspection-v2-stat-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Cellules",
                                        className=(
                                            "inspection-v2-stat-label"
                                        ),
                                    ),
                                ],
                                className=(
                                    "inspection-v2-stat-card"
                                ),
                            ),
                        ],
                        className="inspection-v2-stats",
                    ),
                ],
                className="inspection-v2-section",
            ),

            # --------------------------------------------------
            # PROFILAGE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "PROFILAGE",
                                        className=(
                                            "inspection-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Diagnostic scientifique",
                                        className=(
                                            "inspection-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        (
                                            "L'analyse est diagnostique : "
                                            "elle décrit la structure et "
                                            "les problèmes potentiels sans "
                                            "modifier les données."
                                        ),
                                        className=(
                                            "inspection-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            dbc.Button(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-activity me-2"
                                        )
                                    ),
                                    "Profiler le dataset",
                                ],
                                id="btn-profile-dataset",
                                className=(
                                    "inspection-v2-profile-button"
                                ),
                            ),
                        ],
                        className=(
                            "inspection-v2-profile-header"
                        ),
                    ),

                    html.Div(
                        profile_summary,
                        id="profile-result",
                        className=(
                            "inspection-v2-profile-result"
                        ),
                    ),
                ],
                className=(
                    "inspection-v2-profile-section"
                ),
            ),

            # --------------------------------------------------
            # APERÇU
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "APERÇU DES DONNÉES",
                                        className=(
                                            "inspection-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Premières observations",
                                        className=(
                                            "inspection-v2-section-title"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-eye me-2"
                                        )
                                    ),
                                    "10 premières lignes",
                                ],
                                className=(
                                    "inspection-v2-preview-badge"
                                ),
                            ),
                        ],
                        className=(
                            "inspection-v2-preview-header"
                        ),
                    ),

                    html.Div(
                        preview_table,
                        className=(
                            "inspection-v2-preview-table"
                        ),
                    ),
                ],
                className=(
                    "inspection-v2-preview-section"
                ),
            ),

            # --------------------------------------------------
            # SUITE DU CYCLE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "ÉTAPE SUIVANTE",
                                        className=(
                                            "inspection-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Préparer les données",
                                        className=(
                                            "inspection-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        (
                                            "Une fois le diagnostic "
                                            "effectué, poursuivez vers "
                                            "EIDPP pour traiter et préparer "
                                            "le jeu de données."
                                        ),
                                        className=(
                                            "inspection-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                [
                                    dcc.Link(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-left "
                                                    "me-2"
                                                )
                                            ),
                                            "Retour au projet",
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                        ),
                                        className=(
                                            "inspection-v2-secondary-link"
                                        ),
                                    ),

                                    dcc.Link(
                                        [
                                            "Ouvrir EIDPP",
                                            html.I(
                                                className=(
                                                    "bi bi-arrow-right "
                                                    "ms-2"
                                                )
                                            ),
                                        ],
                                        href=(
                                            f"/projects/{project_id}"
                                            f"/datasets/{dataset_id}/eidpp"
                                        ),
                                        className=(
                                            "inspection-v2-primary-link"
                                        ),
                                    ),
                                ],
                                className=(
                                    "inspection-v2-actions"
                                ),
                            ),
                        ],
                        className=(
                            "inspection-v2-next-card"
                        ),
                    ),
                ],
                className="inspection-v2-next-section",
            ),

            # --------------------------------------------------
            # STORES
            # --------------------------------------------------

            dcc.Store(
                id="inspection-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="inspection-dataset-id",
                data=dataset_id,
            ),
        ],
        fluid=True,
        className="inspection-v2-page",
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
