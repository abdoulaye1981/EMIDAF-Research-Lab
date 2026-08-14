from dash import html
from dash import dcc

import dash_bootstrap_components as dbc


def project_modal():

    return dbc.Modal(

        [

            dbc.ModalHeader(

                dbc.ModalTitle(

                    "Nouveau Projet"

                )

            ),

            dbc.ModalBody(

                [

                    dbc.Label(

                        "Nom du projet"

                    ),

                    dbc.Input(

                        id="project-name",

                        placeholder="Nom du projet",

                        type="text"

                    ),

                    html.Br(),

                    dbc.Label(

                        "Auteur"

                    ),

                    dbc.Input(

                        id="project-author",

                        placeholder="Auteur",

                        type="text"

                    ),

                    html.Br(),

                    dbc.Label(

                        "Description"

                    ),

                    dbc.Textarea(

                        id="project-description",

                        placeholder="Description du projet"

                    ),

                    html.Br(),

                    dbc.Label(

                        "Type de projet"

                    ),

                    dcc.Dropdown(

                        id="project-type",

                        options=[

                            {

                                "label": "Recherche",

                                "value": "research"

                            },

                            {

                                "label": "Enseignement",

                                "value": "teaching"

                            },

                            {

                                "label": "Démonstration",

                                "value": "demo"

                            }

                        ],

                        value="research",

                        clearable=False

                    ),

                    html.Br(),

                    dbc.Label(

                        "Workspace"

                    ),

                    dbc.Input(

                        id="project-workspace",

                        value="workspace/projects",

                        type="text"

                    )

                ]

            ),

            dbc.ModalFooter(

                [

                    dbc.Button(

                        "Créer",

                        id="btn-create-project",

                        color="primary"

                    ),

                    dbc.Button(

                        "Annuler",

                        id="btn-close-project",

                        color="secondary"

                    )

                ]

            )

        ],

        id="project-modal",

        size="lg",

        centered=True,

        backdrop="static",

        is_open=False

    )