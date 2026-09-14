from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from emidaf_core.bootstrap import Bootstrap

from emidaf_studio.components.toolbar import Toolbar
from emidaf_studio.components.cards import ProjectCard
from emidaf_studio.pages.projects.modal import (project_modal,delete_project_modal)


# ==========================================================
# Initialisation du Core
# ==========================================================

bootstrap = Bootstrap()
bootstrap.initialize()

project_controller = bootstrap.project_controller


# ==========================================================
# Récupération des projets depuis SQLite
# ==========================================================

projects = project_controller.get_all()


# ==========================================================
# Layout de la page
# ==========================================================

# ==========================================================
# Layout de la page
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

    project = project_controller.get(project_id)

    if project is None:

        return dbc.Container(
            [
                html.H2("Projet introuvable"),

                html.P(
                    f"Aucun projet ne correspond à l'identifiant {project_id}."
                )
            ],
            fluid=True
        )

    return dbc.Container(
        [
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

            html.H4("Espace de travail"),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("📥 Importation"),

                                        html.P(
                                            "Importer et gérer les datasets."
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("🔎 Inspection"),

                                        html.P(
                                            "Explorer et inspecter les données."
                                        )
                                    ]
                                )
                            ]
                        ),
                        width=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("📊 Analyses"),

                                        html.P(
                                            "Accéder aux modules d'analyse."
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

            dbc.Alert(
                "Les modules seront activés progressivement.",
                color="info"
            )
        ],
        fluid=True
    )
