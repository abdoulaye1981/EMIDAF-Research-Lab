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
        html.H2(
            "Gestion des projets"
        ),

        html.Hr(),

        Toolbar.projects(),

        html.Br(),

        html.Div(
            [
                ProjectCard.create(project)
                for project in projects
            ],
            id="projects-container"
        ),

        # ==================================================
        # Alerte utilisateur
        # ==================================================

        dbc.Alert(
            id="project-alert",
            is_open=False
        ),

        dcc.Store(
            id="selected-project",
            data=None
        ),

        html.Div(
            id="selected-project-info",
            className="mt-3"
        ),

        # ==================================================
        # Modal Nouveau Projet
        # ==================================================

        project_modal(),

        delete_project_modal()
    ],
    fluid=True
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
    # Construction des cartes datasets
    # ------------------------------------------------------

    if datasets:

        dataset_cards = [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5(
                                f"📄 {dataset.name}"
                            ),

                            html.P(
                                f"Fichier : "
                                f"{dataset.original_filename}"
                            ),

                            html.P(
                                f"Dimensions : "
                                f"{dataset.rows} lignes × "
                                f"{dataset.columns} colonnes"
                            ),

                            html.P(
                                f"Extension : "
                                f"{dataset.extension}"
                            ),

                            html.P(
                                f"Taille : "
                                f"{dataset.size / 1024:.2f} Ko"
                            ),

                            # ==================================
                            # Action Inspection
                            # ==================================

                            dcc.Link(
                                dbc.Button(
                                    "🔎 Inspecter",
                                    color="primary",
                                    size="sm"
                                ),
                                href=(
                                    f"/projects/"
                                    f"{project_id}/datasets/"
                                    f"{dataset.id}"
                                )
                            )
                        ]
                    )
                ],
                className="mb-3"
            )
            for dataset in datasets
        ]

    else:

        dataset_cards = dbc.Alert(
            "Aucun dataset n'est encore associé à ce projet.",
            color="secondary"
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
                f"📁 {project.name}"
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

            dbc.Row(
                [
                    # ========================================
                    # Importation
                    # ========================================

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "📥 Importation"
                                        ),

                                        html.P(
                                            "Importer et gérer "
                                            "les datasets."
                                        ),

                                        dcc.Link(
                                            dbc.Button(
                                                "Ouvrir",
                                                color="primary",
                                                size="sm"
                                            ),
                                            href=(
                                                f"/projects/"
                                                f"{project_id}/import"
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=4
                    ),

                    # ========================================
                    # Inspection
                    # ========================================

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "🔎 Inspection"
                                        ),

                                        html.P(
                                            "Explorer et inspecter "
                                            "les données."
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=4
                    ),

                    # ========================================
                    # Analyses
                    # ========================================

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5(
                                            "📊 Analyses"
                                        ),

                                        html.P(
                                            "Accéder aux modules "
                                            "d'analyse."
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=4
                    )
                ],
                className="mb-4"
            ),

            # ------------------------------------------------
            # Datasets du projet
            # ------------------------------------------------

            html.Hr(),

            html.H4(
                "📊 Datasets du projet"
            ),

            html.Div(
                dataset_cards,
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
