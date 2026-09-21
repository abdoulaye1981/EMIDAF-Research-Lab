from dash import html
from dash import dcc

import dash_bootstrap_components as dbc

from emidaf_core.bootstrap import Bootstrap

from emidaf_studio.components.toolbar import Toolbar
from emidaf_studio.components.cards import ProjectCard
from emidaf_studio.pages.projects.modal import (
    project_modal,
    delete_project_modal
)


# ==========================================================
# Initialisation du Core
# ==========================================================

bootstrap = Bootstrap()
bootstrap.initialize()

project_controller = bootstrap.project_controller
dataset_controller = bootstrap.dataset_controller


# ==========================================================
# Récupération des projets depuis SQLite
# ==========================================================

projects = project_controller.get_all()


# ==========================================================
# Page de gestion des projets
# ==========================================================

layout = dbc.Container(
    [
        # ==================================================
        # HERO / COMMAND CENTER
        # ==================================================

        html.Section(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "PROJETS",
                                            className=(
                                                "projects-v2-kicker"
                                            ),
                                        ),
                                        html.Span(
                                            (
                                                "ESPACE DE "
                                                "RECHERCHE"
                                            ),
                                            className=(
                                                "projects-v2-eyebrow"
                                            ),
                                        ),
                                    ],
                                    className=(
                                        "d-flex "
                                        "align-items-center "
                                        "gap-2 mb-3"
                                    ),
                                ),

                                html.H1(
                                    (
                                        "Projets de recherche "
                                        "et d'analyse"
                                    ),
                                    className=(
                                        "projects-v2-title"
                                    ),
                                ),

                                html.P(
                                    (
                                        "Structurez vos jeux de "
                                        "données, analyses, modèles "
                                        "et résultats dans des espaces "
                                        "de travail scientifiques "
                                        "indépendants."
                                    ),
                                    className=(
                                        "projects-v2-subtitle"
                                    ),
                                ),
                            ],
                            lg=8,
                        ),

                        dbc.Col(
                            html.Div(
                                Toolbar.projects(),
                                className=(
                                    "projects-v2-toolbar"
                                ),
                            ),
                            lg=4,
                            className=(
                                "d-flex "
                                "align-items-center "
                                "justify-content-lg-end"
                            ),
                        ),
                    ],
                    className="g-4 align-items-center",
                ),
            ],
            className="projects-v2-hero",
        ),

        # ==================================================
        # APERÇU
        # ==================================================

        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    html.I(
                                        className=(
                                            "bi "
                                            "bi-folder2-open"
                                        )
                                    ),
                                    className=(
                                        "projects-v2-stat-icon"
                                    ),
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            str(len(projects)),
                                            className=(
                                                "projects-v2-stat-value"
                                            ),
                                        ),
                                        html.Div(
                                            (
                                                "Projet"
                                                if len(projects) == 1
                                                else "Projets"
                                            ),
                                            className=(
                                                "projects-v2-stat-label"
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            className=(
                                "projects-v2-stat-card"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    html.I(
                                        className=(
                                            "bi "
                                            "bi-diagram-3"
                                        )
                                    ),
                                    className=(
                                        "projects-v2-stat-icon"
                                    ),
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            "09",
                                            className=(
                                                "projects-v2-stat-value"
                                            ),
                                        ),
                                        html.Div(
                                            "Étapes analytiques",
                                            className=(
                                                "projects-v2-stat-label"
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            className=(
                                "projects-v2-stat-card"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    html.I(
                                        className=(
                                            "bi "
                                            "bi-database-check"
                                        )
                                    ),
                                    className=(
                                        "projects-v2-stat-icon"
                                    ),
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            "Data → IA",
                                            className=(
                                                "projects-v2-stat-value "
                                                "projects-v2-stat-text"
                                            ),
                                        ),
                                        html.Div(
                                            "Cycle scientifique",
                                            className=(
                                                "projects-v2-stat-label"
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            className=(
                                "projects-v2-stat-card"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    html.I(
                                        className=(
                                            "bi "
                                            "bi-file-earmark-"
                                            "bar-graph"
                                        )
                                    ),
                                    className=(
                                        "projects-v2-stat-icon"
                                    ),
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            "Rapports",
                                            className=(
                                                "projects-v2-stat-value "
                                                "projects-v2-stat-text"
                                            ),
                                        ),
                                        html.Div(
                                            "Restitution structurée",
                                            className=(
                                                "projects-v2-stat-label"
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            className=(
                                "projects-v2-stat-card"
                            ),
                        ),
                    ],
                    className="projects-v2-stats",
                ),
            ],
            className="projects-v2-overview",
        ),

        # ==================================================
        # PRINCIPES D'ORGANISATION
        # ==================================================

        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            "ORGANISATION SCIENTIFIQUE",
                            className=(
                                "projects-v2-section-kicker"
                            ),
                        ),

                        html.H2(
                            "Un projet, un cycle analytique complet",
                            className=(
                                "projects-v2-section-title"
                            ),
                        ),

                        html.P(
                            (
                                "Chaque projet constitue un espace "
                                "cohérent regroupant les données, "
                                "les analyses et les résultats."
                            ),
                            className=(
                                "projects-v2-section-subtitle"
                            ),
                        ),
                    ],
                    className=(
                        "projects-v2-section-heading"
                    ),
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "01",
                                    className=(
                                        "projects-v2-principle-number"
                                    ),
                                ),
                                html.I(
                                    className=(
                                        "bi bi-folder2-open "
                                        "projects-v2-principle-icon"
                                    )
                                ),
                                html.H3(
                                    "Organisation",
                                    className=(
                                        "projects-v2-principle-title"
                                    ),
                                ),
                                html.P(
                                    (
                                        "Centralisez jeux de données, "
                                        "analyses et résultats dans "
                                        "un espace de travail unique."
                                    ),
                                    className=(
                                        "projects-v2-principle-text"
                                    ),
                                ),
                            ],
                            className=(
                                "projects-v2-principle-card"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    "02",
                                    className=(
                                        "projects-v2-principle-number"
                                    ),
                                ),
                                html.I(
                                    className=(
                                        "bi bi-bar-chart-line "
                                        "projects-v2-principle-icon"
                                    )
                                ),
                                html.H3(
                                    "Analyse",
                                    className=(
                                        "projects-v2-principle-title"
                                    ),
                                ),
                                html.P(
                                    (
                                        "Progressez de l'inspection "
                                        "jusqu'à la modélisation, "
                                        "l'explicabilité et la décision."
                                    ),
                                    className=(
                                        "projects-v2-principle-text"
                                    ),
                                ),
                            ],
                            className=(
                                "projects-v2-principle-card"
                            ),
                        ),

                        html.Div(
                            [
                                html.Div(
                                    "03",
                                    className=(
                                        "projects-v2-principle-number"
                                    ),
                                ),
                                html.I(
                                    className=(
                                        "bi bi-file-earmark-text "
                                        "projects-v2-principle-icon"
                                    )
                                ),
                                html.H3(
                                    "Restitution",
                                    className=(
                                        "projects-v2-principle-title"
                                    ),
                                ),
                                html.P(
                                    (
                                        "Conservez les résultats "
                                        "analytiques et produisez des "
                                        "rapports structurés."
                                    ),
                                    className=(
                                        "projects-v2-principle-text"
                                    ),
                                ),
                            ],
                            className=(
                                "projects-v2-principle-card"
                            ),
                        ),
                    ],
                    className=(
                        "projects-v2-principles"
                    ),
                ),
            ],
            className="projects-v2-section",
        ),

        # ==================================================
        # LISTE DES PROJETS
        # ==================================================

        html.Section(
            [
                # ------------------------------------------
                # En-tête de la zone projets
                # ------------------------------------------

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "ESPACE DE TRAVAIL",
                                    className=(
                                        "projects-v2-section-kicker"
                                    ),
                                ),

                                html.H2(
                                    "Mes projets",
                                    className=(
                                        "projects-v2-section-title "
                                        "mb-0"
                                    ),
                                ),
                            ]
                        ),

                        html.Div(
                            [
                                html.I(
                                    className=(
                                        "bi bi-grid-3x3-gap me-2"
                                    )
                                ),

                                (
                                    f"{len(projects)} projet"
                                    if len(projects) == 1
                                    else (
                                        f"{len(projects)} "
                                        "projets"
                                    )
                                ),
                            ],
                            className="projects-v2-count",
                        ),
                    ],
                    className="projects-v2-projects-header",
                ),

                # ------------------------------------------
                # Cartes projets
                # ------------------------------------------

                html.Div(
                    [
                        ProjectCard.create(project)
                        for project in projects
                    ],
                    id="projects-container",
                    className="projects-v2-projects-grid",
                ),

                # ------------------------------------------
                # État vide
                # ------------------------------------------

                html.Div(
                    [
                        html.I(
                            className="bi bi-folder-plus"
                        ),

                        html.H3(
                            "Aucun projet",
                        ),

                        html.P(
                            (
                                "Créez votre premier espace "
                                "de recherche pour commencer "
                                "le cycle analytique EMIDAF."
                            )
                        ),
                    ],
                    className=(
                        "projects-v2-empty "
                        + (
                            "d-none"
                            if projects
                            else ""
                        )
                    ),
                ),
            ],
            className="projects-v2-workspace",
        ),

        # ==================================================
        # ÉTAT / CALLBACKS
        # ==================================================

        dbc.Alert(
            id="project-alert",
            is_open=False,
            className="projects-v2-alert",
        ),

        dcc.Store(
            id="selected-project",
            data=None,
        ),

        html.Div(
            id="selected-project-info",
            className="projects-v2-selection",
        ),

        # ==================================================
        # MODALES EXISTANTES
        # ==================================================

        project_modal(),
        delete_project_modal(),
    ],
    fluid=True,
    className="projects-v2-page",
)


# ==========================================================
# Page détaillée d'un projet
# ==========================================================

def project_detail_layout(project_id):

    # ------------------------------------------------------
    # Récupération du projet
    # ------------------------------------------------------

    project = project_controller.get(project_id)

    if project is None:

        return dbc.Container(
            [
                html.H2(
                    "Projet introuvable"
                ),

                html.P(
                    f"Aucun projet ne correspond "
                    f"à l'identifiant {project_id}."
                )
            ],
            fluid=True
        )

    # ------------------------------------------------------
    # Récupération des datasets du projet
    # ------------------------------------------------------

    datasets = [
        dataset
        for dataset in dataset_controller.get_all()
        if dataset.project_id == project_id
    ]

    # ------------------------------------------------------
    # Tableau compact des jeux de données
    # ------------------------------------------------------

    if datasets:

        dataset_rows = []

        for dataset in datasets:

            inspect_href = (
                f"/projects/{project_id}"
                f"/datasets/{dataset.id}"
            )

            actions = dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        "Inspection",
                        href=inspect_href,
                    ),

                    dbc.DropdownMenuItem(
                        "Prétraitement",
                        href=(
                            inspect_href
                            + "/eidpp"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Analyse exploratoire",
                        href=(
                            inspect_href
                            + "/elae"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Découverte de connaissances",
                        href=(
                            inspect_href
                            + "/ekde"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Modélisation prédictive",
                        href=(
                            inspect_href
                            + "/eaie"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Explicabilité des modèles",
                        href=(
                            inspect_href
                            + "/exaie"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Aide à la décision",
                        href=(
                            inspect_href
                            + "/edse"
                        ),
                    ),

                    dbc.DropdownMenuItem(
                        "Rapports",
                        href=(
                            inspect_href
                            + "/reports"
                        ),
                    ),
                ],
                label="Actions",
                size="sm",
                color="primary",
            )

            dataset_rows.append(
                html.Tr(
                    [
                        html.Td(
                            dataset.name
                        ),

                        html.Td(
                            dataset.original_filename
                        ),

                        html.Td(
                            (
                                f"{dataset.rows} × "
                                f"{dataset.columns}"
                            )
                        ),

                        html.Td(
                            dataset.extension.upper()
                        ),

                        html.Td(
                            (
                                f"{dataset.size / 1024:.2f} Ko"
                            )
                        ),

                        html.Td(
                            actions
                        ),
                    ]
                )
            )

        dataset_view = dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Nom"),
                            html.Th("Fichier"),
                            html.Th("Dimensions"),
                            html.Th("Format"),
                            html.Th("Taille"),
                            html.Th("Actions"),
                        ]
                    )
                ),

                html.Tbody(
                    dataset_rows
                ),
            ],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            size="sm",
        )

    else:

        dataset_view = dbc.Alert(
            (
                "Aucun jeu de données n'est encore "
                "associé à ce projet."
            ),
            color="secondary",
        )

    # ======================================================
    # Sélection du dataset de travail
    # ======================================================

    dataset_options = [
        {
            "label": (
                f"{dataset.name} "
                f"({dataset.rows} × {dataset.columns})"
            ),
            "value": int(dataset.id),
        }
        for dataset in datasets
    ]

    default_dataset_id = (
        int(datasets[0].id)
        if datasets
        else None
    )

    # ======================================================
    # Layout détaillé
    # ======================================================

    return dbc.Container(
        [
            # ------------------------------------------------
            # Informations du projet
            # ------------------------------------------------

            html.H2(
                project.name
            ),

            html.Hr(),

            html.P(
                f"Workspace ID : {project.workspace_id}"
            ),

            html.P(
                project.description
            ),

            html.Hr(),

            # ------------------------------------------------
            # Espace de travail
            # ------------------------------------------------

            html.H4(
                "Espace de travail"
            ),

            html.P(
                (
                    "Sélectionnez le jeu de données sur lequel "
                    "vous souhaitez travailler, puis ouvrez "
                    "le module correspondant."
                ),
                className="text-muted",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Jeu de données"
                                        ),
                                        dcc.Dropdown(
                                            id=(
                                                "project-detail-"
                                                "dataset-selector"
                                            ),
                                            options=(
                                                dataset_options
                                            ),
                                            value=(
                                                default_dataset_id
                                            ),
                                            clearable=False,
                                            placeholder=(
                                                "Sélectionner "
                                                "un dataset"
                                            ),
                                            disabled=(
                                                not bool(
                                                    datasets
                                                )
                                            ),
                                        ),
                                    ],
                                    md=12,
                                ),
                            ],
                            className="mb-4",
                        ),

                        html.Div(
                            [
                                dcc.Link(
                                    dbc.Button(
                                        [
                                            html.I(
                                                className=(
                                                    "bi bi-search "
                                                    "me-2"
                                                )
                                            ),
                                            "Inspection",
                                        ],
                                        color="primary",
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "inspection-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Prétraitement EIDPP",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "eidpp-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Analyse ELAE",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "elae-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Découverte EKDE",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "ekde-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Modélisation EAIE",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "eaie-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Explicabilité EXAIE",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "exaie-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Décision EDSE",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "edse-link"
                                    ),
                                    href="#",
                                ),

                                dcc.Link(
                                    dbc.Button(
                                        "Rapports",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    id=(
                                        "project-detail-"
                                        "reports-link"
                                    ),
                                    href="#",
                                ),
                            ],
                            style={
                                "display": "grid",
                                "gridTemplateColumns": (
                                    "repeat("
                                    "auto-fit, "
                                    "minmax(190px, 1fr)"
                                    ")"
                                ),
                                "gap": "12px",
                            },
                        ),

                        (
                            dbc.Alert(
                                (
                                    "Aucun jeu de données n'est "
                                    "encore disponible. Utilisez "
                                    "l'importation pour ajouter "
                                    "un dataset à ce projet."
                                ),
                                color="warning",
                                className="mt-4 mb-0",
                            )
                            if not datasets
                            else html.Div()
                        ),

                        dcc.Store(
                            id=(
                                "project-detail-project-id"
                            ),
                            data=int(project_id),
                        ),
                    ]
                ),
                className="mb-4",
            ),

            # ------------------------------------------------
            # Datasets du projet
            # ------------------------------------------------

            html.Hr(),

            html.H4(
                "Jeux de données du projet"
            ),

            html.Div(
                dataset_view,
                className="mt-3"
            ),

            # ------------------------------------------------
            # Information générale
            # ------------------------------------------------

            html.Hr(),

            dbc.Alert(
                "Les modules seront activés progressivement.",
                color="info"
            )
        ],
        fluid=True
    )


# ==========================================================
# MULTI-USER LAYOUT
# ==========================================================

def user_projects_layout(user_id: int):
    """
    Construit la page Projets pour un utilisateur donné.

    Toutes les données affichées sont limitées aux projets
    appartenant à cet utilisateur.
    """

    from copy import deepcopy

    user_projects = (
        project_controller
        .get_all_for_user(
            int(user_id)
        )
    )

    page = deepcopy(layout)

    project_cards = [
        ProjectCard.create(project)
        for project in user_projects
    ]

    global_count = len(projects)
    user_count = len(user_projects)

    old_label = (
        f"{global_count} projet"
        if global_count == 1
        else f"{global_count} projets"
    )

    new_label = (
        f"{user_count} projet"
        if user_count == 1
        else f"{user_count} projets"
    )

    old_label_capitalized = (
        f"{global_count} Projet"
        if global_count == 1
        else f"{global_count} Projets"
    )

    new_label_capitalized = (
        f"{user_count} Projet"
        if user_count == 1
        else f"{user_count} Projets"
    )

    def update_component(component):
        if component is None:
            return

        # ----------------------------------------------
        # Container des cartes projets
        # ----------------------------------------------

        if (
            getattr(
                component,
                "id",
                None,
            )
            == "projects-container"
        ):
            component.children = project_cards
            return

        children = getattr(
            component,
            "children",
            None,
        )

        if children is None:
            return

        # ----------------------------------------------
        # Texte simple
        # ----------------------------------------------

        if isinstance(
            children,
            str,
        ):
            if children == str(global_count):
                component.children = str(
                    user_count
                )

            elif children == old_label:
                component.children = new_label

            elif children == old_label_capitalized:
                component.children = (
                    new_label_capitalized
                )

            return

        # ----------------------------------------------
        # Descente récursive
        # ----------------------------------------------

        if isinstance(
            children,
            (list, tuple),
        ):
            for child in children:
                update_component(child)

        else:
            update_component(children)

    update_component(page)

    return page
