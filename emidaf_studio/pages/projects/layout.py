from dash import html

import dash_bootstrap_components as dbc

from emidaf_core.entities.project import Project

from emidaf_studio.components.toolbar import Toolbar
from emidaf_studio.components.cards import ProjectCard
from emidaf_studio.pages.projects.modal import project_modal


# ==========================================================
# Données fictives (Sprint 2.1)
# Elles seront remplacées plus tard par SQLite
# ==========================================================

projects = [

    Project(
        name="Doctorat",
        author="Pr. Abdoulaye Wakhab DIOP",
        description="Framework EMIDAF"
    ),

    Project(
        name="IFADEM",
        author="Pr. Abdoulaye Wakhab DIOP",
        description="Projet Learning Analytics"
    )

]


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

        # ==================================================
        # Modal Nouveau Projet
        # ==================================================

        project_modal()

    ],

    fluid=True

)