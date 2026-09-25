from __future__ import annotations

from dash import dcc, html
import dash_bootstrap_components as dbc

from emidaf_studio.pages.inspection.layout import load_dataset
from emidaf_studio.services.model_registry import has_analysis


REPORT_STAGES = [
    {
        "label": "Projet et jeu de données",
        "value": "project",
    },
    {
        "label": "Inspection des données",
        "value": "inspection",
    },
    {
        "label": "Prétraitement des données",
        "value": "preprocessing",
    },
    {
        "label": "Analyse exploratoire",
        "value": "elae",
    },
    {
        "label": "Analyse textuelle",
        "value": "etae",
    },
    {
        "label": "Découverte de connaissances",
        "value": "ekde",
    },
    {
        "label": "Modélisation prédictive",
        "value": "eaie",
    },
    {
        "label": "Explicabilité des modèles",
        "value": "exaie",
    },
    {
        "label": "Aide à la décision",
        "value": "edse",
    },
]


def _status_badge(available: bool):

    if available:
        return html.Span(
            [
                html.I(
                    className="bi bi-check-circle-fill me-1"
                ),
                "Disponible",
            ],
            className=(
                "reports-v2-status-badge "
                "reports-v2-status-available"
            ),
        )

    return html.Span(
        [
            html.I(
                className="bi bi-circle me-1"
            ),
            "Non exécuté",
        ],
        className=(
            "reports-v2-status-badge "
            "reports-v2-status-missing"
        ),
    )


def reports_layout(project_id, dataset_id):

    project, dataset, dataframe = load_dataset(
        project_id,
        dataset_id,
    )

    # ======================================================
    # ERREUR DE CHARGEMENT
    # ======================================================

    if isinstance(dataframe, str):

        return dbc.Container(
            [
                html.Section(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "REPORTS",
                                    className="reports-v2-kicker",
                                ),
                                html.Span(
                                    "RESTITUTION",
                                    className="reports-v2-eyebrow",
                                ),
                            ],
                            className=(
                                "d-flex align-items-center "
                                "gap-2 mb-3"
                            ),
                        ),

                        html.H1(
                            "Rapports analytiques",
                            className="reports-v2-title",
                        ),

                        html.P(
                            (
                                "Le jeu de données ne peut pas "
                                "être chargé dans son état actuel."
                            ),
                            className="reports-v2-subtitle",
                        ),
                    ],
                    className="reports-v2-hero",
                ),

                dbc.Alert(
                    dataframe,
                    color="danger",
                    className="mt-4",
                ),
            ],
            fluid=True,
            className="reports-v2-page",
        )

    # ======================================================
    # INDICATEURS
    # ======================================================

    rows = len(dataframe)
    columns = len(dataframe.columns)

    missing_total = int(
        dataframe.isna().sum().sum()
    )

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    # ======================================================
    # DISPONIBILITÉ DES ÉTAPES
    # ======================================================

    availability = {
        "project": True,
        "inspection": True,
        "preprocessing": has_analysis(
            project_id,
            dataset_id,
            "eidpp",
        ),
        "elae": has_analysis(
            project_id,
            dataset_id,
            "elae",
        ),
        "etae": has_analysis(
            project_id,
            dataset_id,
            "etae",
        ),
        "ekde": has_analysis(
            project_id,
            dataset_id,
            "ekde",
        ),
        "eaie": has_analysis(
            project_id,
            dataset_id,
            "eaie",
        ),
        "exaie": has_analysis(
            project_id,
            dataset_id,
            "exaie",
        ),
        "edse": has_analysis(
            project_id,
            dataset_id,
            "edse",
        ),
    }

    selected_default = [
        key
        for key, available
        in availability.items()
        if available
    ]

    completed_count = sum(
        1
        for available
        in availability.values()
        if available
    )

    total_count = len(availability)

    completion_rate = round(
        100 * completed_count / total_count
    )

    availability_rows = []

    for index, stage in enumerate(
        REPORT_STAGES,
        start=1,
    ):

        key = stage["value"]

        availability_rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                f"{index:02d}",
                                className=(
                                    "reports-v2-stage-number"
                                ),
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        stage["label"],
                                        className=(
                                            "reports-v2-stage-name"
                                        ),
                                    ),
                                    html.Div(
                                        key.upper(),
                                        className=(
                                            "reports-v2-stage-code"
                                        ),
                                    ),
                                ]
                            ),
                        ],
                        className=(
                            "reports-v2-stage-identity"
                        ),
                    ),

                    _status_badge(
                        availability[key]
                    ),
                ],
                className="reports-v2-stage-row",
            )
        )

    # ======================================================
    # PAGE
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
                                        "REPORTS",
                                        className="reports-v2-kicker",
                                    ),

                                    html.Span(
                                        "RESTITUTION ANALYTIQUE",
                                        className="reports-v2-eyebrow",
                                    ),
                                ],
                                className=(
                                    "d-flex align-items-center "
                                    "gap-2 mb-3"
                                ),
                            ),

                            html.H1(
                                "Rapports analytiques",
                                className="reports-v2-title",
                            ),

                            html.P(
                                (
                                    "Consolidez les résultats produits "
                                    "tout au long du pipeline EMIDAF "
                                    "dans un document structuré, "
                                    "traçable et adapté à la restitution "
                                    "scientifique et professionnelle."
                                ),
                                className="reports-v2-subtitle",
                            ),
                        ]
                    ),

                    html.Div(
                        html.I(
                            className=(
                                "bi bi-file-earmark-text "
                                "reports-v2-hero-icon"
                            )
                        ),
                        className="reports-v2-hero-icon-box",
                    ),
                ],
                className="reports-v2-hero",
            ),

            # --------------------------------------------------
            # BREADCRUMB
            # --------------------------------------------------

            dbc.Breadcrumb(
                items=[
                    {
                        "label": "Projets",
                        "href": "/projects",
                    },
                    {
                        "label": project.name,
                        "href": f"/projects/{project_id}",
                    },
                    {
                        "label": dataset.name,
                        "href": (
                            f"/projects/{project_id}"
                            f"/datasets/{dataset_id}"
                        ),
                    },
                    {
                        "label": "Rapports",
                        "active": True,
                    },
                ],
                className="reports-v2-breadcrumb",
            ),

            # --------------------------------------------------
            # PRINCIPE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        html.I(
                            className="bi bi-info-circle"
                        ),
                        className="reports-v2-method-icon",
                    ),

                    html.Div(
                        [
                            html.Div(
                                "PRINCIPE MÉTHODOLOGIQUE",
                                className=(
                                    "reports-v2-method-label"
                                ),
                            ),

                            html.P(
                                (
                                    "Le module Rapports consolide "
                                    "les résultats déjà produits et "
                                    "persistés par EMIDAF. Il ne "
                                    "recalcule pas silencieusement les "
                                    "analyses précédemment réalisées."
                                ),
                                className=(
                                    "reports-v2-method-text"
                                ),
                            ),
                        ]
                    ),
                ],
                className="reports-v2-method-card",
            ),

            # --------------------------------------------------
            # CONTEXTE
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "CONTEXTE DE RESTITUTION",
                        className="reports-v2-section-kicker",
                    ),

                    html.H2(
                        "Projet et jeu de données",
                        className="reports-v2-section-title",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-folder2-open"
                                            )
                                        ),
                                        className=(
                                            "reports-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Projet",
                                        className=(
                                            "reports-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        project.name,
                                        className=(
                                            "reports-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="reports-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-database"
                                            )
                                        ),
                                        className=(
                                            "reports-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Jeu de données",
                                        className=(
                                            "reports-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        dataset.name,
                                        className=(
                                            "reports-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="reports-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-list-ol"
                                            )
                                        ),
                                        className=(
                                            "reports-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Observations",
                                        className=(
                                            "reports-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        f"{rows:,}".replace(",", " "),
                                        className=(
                                            "reports-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="reports-v2-stat-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        html.I(
                                            className=(
                                                "bi bi-columns-gap"
                                            )
                                        ),
                                        className=(
                                            "reports-v2-stat-icon"
                                        ),
                                    ),
                                    html.Div(
                                        "Variables",
                                        className=(
                                            "reports-v2-stat-label"
                                        ),
                                    ),
                                    html.Div(
                                        str(columns),
                                        className=(
                                            "reports-v2-stat-value"
                                        ),
                                    ),
                                ],
                                className="reports-v2-stat-card",
                            ),
                        ],
                        className="reports-v2-stats",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        str(missing_total),
                                        className=(
                                            "reports-v2-quality-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Valeurs manquantes",
                                        className=(
                                            "reports-v2-quality-label"
                                        ),
                                    ),
                                ],
                                className="reports-v2-quality-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        str(duplicate_rows),
                                        className=(
                                            "reports-v2-quality-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Doublons",
                                        className=(
                                            "reports-v2-quality-label"
                                        ),
                                    ),
                                ],
                                className="reports-v2-quality-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        f"{completed_count}/{total_count}",
                                        className=(
                                            "reports-v2-quality-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Étapes disponibles",
                                        className=(
                                            "reports-v2-quality-label"
                                        ),
                                    ),
                                ],
                                className="reports-v2-quality-card",
                            ),

                            html.Div(
                                [
                                    html.Div(
                                        f"{completion_rate} %",
                                        className=(
                                            "reports-v2-quality-value"
                                        ),
                                    ),
                                    html.Div(
                                        "Progression analytique",
                                        className=(
                                            "reports-v2-quality-label"
                                        ),
                                    ),
                                ],
                                className="reports-v2-quality-card",
                            ),
                        ],
                        className="reports-v2-quality-grid",
                    ),
                ],
                className="reports-v2-section",
            ),

            # --------------------------------------------------
            # CONSTRUCTION DU RAPPORT
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        "GÉNÉRATION",
                        className="reports-v2-section-kicker",
                    ),

                    html.H2(
                        "Construire le rapport",
                        className="reports-v2-section-title",
                    ),

                    html.P(
                        (
                            "Sélectionnez les résultats disponibles "
                            "à intégrer et choisissez le format "
                            "de restitution."
                        ),
                        className="reports-v2-section-subtitle",
                    ),

                    html.Div(
                        [
                            # ----------------------------------
                            # PIPELINE
                            # ----------------------------------

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                "ÉTAT DU PIPELINE",
                                                className=(
                                                    "reports-v2-panel-kicker"
                                                ),
                                            ),

                                            html.H3(
                                                "Disponibilité des résultats",
                                                className=(
                                                    "reports-v2-panel-title"
                                                ),
                                            ),

                                            html.P(
                                                (
                                                    "Seules les analyses "
                                                    "déjà disponibles sont "
                                                    "sélectionnées par défaut."
                                                ),
                                                className=(
                                                    "reports-v2-panel-text"
                                                ),
                                            ),
                                        ]
                                    ),

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Span(
                                                        "Progression",
                                                        className=(
                                                            "reports-v2-"
                                                            "progress-label"
                                                        ),
                                                    ),

                                                    html.Span(
                                                        (
                                                            f"{completed_count}"
                                                            f"/{total_count}"
                                                        ),
                                                        className=(
                                                            "reports-v2-"
                                                            "progress-count"
                                                        ),
                                                    ),
                                                ],
                                                className=(
                                                    "reports-v2-"
                                                    "progress-head"
                                                ),
                                            ),

                                            dbc.Progress(
                                                value=completion_rate,
                                                label=(
                                                    f"{completion_rate} %"
                                                ),
                                                className=(
                                                    "reports-v2-progress"
                                                ),
                                            ),
                                        ],
                                        className=(
                                            "reports-v2-progress-box"
                                        ),
                                    ),

                                    html.Div(
                                        availability_rows,
                                        className=(
                                            "reports-v2-stage-list"
                                        ),
                                    ),
                                ],
                                className="reports-v2-pipeline-panel",
                            ),

                            # ----------------------------------
                            # CONFIGURATION
                            # ----------------------------------

                            html.Div(
                                [
                                    html.Div(
                                        "CONFIGURATION",
                                        className=(
                                            "reports-v2-panel-kicker"
                                        ),
                                    ),

                                    html.H3(
                                        "Paramètres du rapport",
                                        className=(
                                            "reports-v2-panel-title"
                                        ),
                                    ),

                                    html.Div(
                                        [
                                            dbc.Label(
                                                "Titre du rapport",
                                                html_for="reports-title",
                                                className=(
                                                    "reports-v2-label"
                                                ),
                                            ),

                                            dbc.Input(
                                                id="reports-title",
                                                value=(
                                                    "Rapport d'analyse "
                                                    "EMIDAF"
                                                ),
                                                type="text",
                                                className=(
                                                    "reports-v2-input"
                                                ),
                                            ),
                                        ],
                                        className="reports-v2-field",
                                    ),

                                    html.Div(
                                        [
                                            dbc.Label(
                                                "Sections à intégrer",
                                                className=(
                                                    "reports-v2-label"
                                                ),
                                            ),

                                            dcc.Checklist(
                                                id="reports-sections",
                                                options=REPORT_STAGES,
                                                value=selected_default,
                                                className=(
                                                    "reports-v2-checklist"
                                                ),
                                                labelClassName=(
                                                    "reports-v2-"
                                                    "check-option"
                                                ),
                                                inputClassName=(
                                                    "reports-v2-"
                                                    "check-input"
                                                ),
                                            ),
                                        ],
                                        className="reports-v2-field",
                                    ),

                                    html.Div(
                                        [
                                            dbc.Label(
                                                "Format d'export",
                                                html_for="reports-format",
                                                className=(
                                                    "reports-v2-label"
                                                ),
                                            ),

                                            dcc.Dropdown(
                                                id="reports-format",
                                                options=[
                                                    {
                                                        "label": "Markdown",
                                                        "value": "markdown",
                                                    },
                                                    {
                                                        "label": "HTML",
                                                        "value": "html",
                                                    },
                                                    {
                                                        "label": "JSON",
                                                        "value": "json",
                                                    },
                                                ],
                                                value="html",
                                                clearable=False,
                                                className=(
                                                    "reports-v2-dropdown"
                                                ),
                                            ),
                                        ],
                                        className="reports-v2-field",
                                    ),

                                    html.Div(
                                        [
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className=(
                                                            "bi bi-file-"
                                                            "earmark-plus "
                                                            "me-2"
                                                        )
                                                    ),
                                                    "Générer le rapport",
                                                ],
                                                id="reports-generate",
                                                className=(
                                                    "reports-v2-"
                                                    "generate-button"
                                                ),
                                            ),

                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className=(
                                                            "bi bi-download "
                                                            "me-2"
                                                        )
                                                    ),
                                                    "Télécharger",
                                                ],
                                                id=(
                                                    "reports-download-button"
                                                ),
                                                disabled=True,
                                                className=(
                                                    "reports-v2-"
                                                    "download-button"
                                                ),
                                            ),
                                        ],
                                        className=(
                                            "reports-v2-form-actions"
                                        ),
                                    ),
                                ],
                                className="reports-v2-config-panel",
                            ),
                        ],
                        className="reports-v2-builder-grid",
                    ),

                    html.Div(
                        id="reports-status",
                        className="reports-v2-status",
                    ),
                ],
                className="reports-v2-builder-section",
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
                                        "APERÇU",
                                        className=(
                                            "reports-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Prévisualisation du rapport",
                                        className=(
                                            "reports-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        (
                                            "Le contenu généré apparaît "
                                            "ici avant téléchargement."
                                        ),
                                        className=(
                                            "reports-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            html.Div(
                                html.I(
                                    className=(
                                        "bi bi-file-earmark-richtext"
                                    )
                                ),
                                className=(
                                    "reports-v2-preview-icon"
                                ),
                            ),
                        ],
                        className="reports-v2-preview-head",
                    ),

                    html.Div(
                        id="reports-preview",
                        className="reports-v2-preview",
                    ),
                ],
                className="reports-v2-preview-section",
            ),

            # --------------------------------------------------
            # NAVIGATION
            # --------------------------------------------------

            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "CYCLE ANALYTIQUE",
                                        className=(
                                            "reports-v2-section-kicker"
                                        ),
                                    ),

                                    html.H2(
                                        "Restitution finale",
                                        className=(
                                            "reports-v2-section-title"
                                        ),
                                    ),

                                    html.P(
                                        (
                                            "Le rapport constitue la "
                                            "restitution des résultats "
                                            "disponibles du pipeline "
                                            "analytique."
                                        ),
                                        className=(
                                            "reports-v2-section-subtitle"
                                        ),
                                    ),
                                ]
                            ),

                            dcc.Link(
                                [
                                    html.I(
                                        className=(
                                            "bi bi-arrow-left me-2"
                                        )
                                    ),
                                    "Aide à la décision",
                                ],
                                href=(
                                    f"/projects/{project_id}"
                                    f"/datasets/{dataset_id}/edse"
                                ),
                                className=(
                                    "reports-v2-secondary-link"
                                ),
                            ),
                        ],
                        className="reports-v2-next-card",
                    ),
                ],
                className="reports-v2-next-section",
            ),

            # --------------------------------------------------
            # STORES / DOWNLOAD
            # --------------------------------------------------

            dcc.Store(
                id="reports-project-id",
                data=project_id,
            ),

            dcc.Store(
                id="reports-dataset-id",
                data=dataset_id,
            ),

            dcc.Store(
                id="reports-generated-content",
            ),

            dcc.Store(
                id="reports-generated-filename",
            ),

            dcc.Download(
                id="reports-download",
            ),
        ],
        fluid=True,
        className="reports-v2-page",
    )
